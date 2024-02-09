import os
import mlflow
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

#Load dataset
pathfile2 = 'Data/get_around_pricing_project.csv' 
data = pd.read_csv(pathfile2)
drop_col = 'Unnamed: 0'
data = data.drop(columns= drop_col)

# Replace rare model_key by 'other'
print("Replacing rare model_key by 'other'...")
model_counts = data.model_key.value_counts()
rare_model = model_counts[model_counts < 15].index

# Mapping rare model to 'other'
data.model_key = data.model_key.replace(rare_model, 'Other')
print("...Done.")

# Drop rows where mileage is negative
print("Dropping rows where mileage is negative...and an extreme outlier")
data = data[(data.mileage > 0) & (data.mileage < 1e6)]
print("...Done.")

# Copy data into data_cleaned
print("Copying data into data_cleaned...")
data_cleaned = data.copy()

# Separate target variable Y from features X
print("Separating target variable Y from features X...")
target_variable = "rental_price_per_day"
features = data_cleaned.drop(columns=target_variable).columns.tolist()

X = data_cleaned.loc[:,features]
Y = data_cleaned.loc[:,target_variable]

# Split our training set and our test set 
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0, stratify=X['model_key'])

# Identify categorical and numerical columns
categorical_cols = [col for col in X_train.columns if X_train[col].dtype == 'object']
numerical_cols = [col for col in X_train.columns if X_train[col].dtype in ['int64', 'float64']]

# Create a column transformer with One-Hot Encoding for categorical data and scaling for numerical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# Set tracking URI to your Heroku application
mlflow.set_tracking_uri("http://localhost:8501")
#mlflow.set_tracking_uri(os.environ["APP_URI"])

# Set your variables for your environment
EXPERIMENT_NAME="Lasso_Regression_Exp"

# Create experiment id
if mlflow.get_experiment_by_name(EXPERIMENT_NAME) is None:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)

# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.sklearn.autolog()

with mlflow.start_run(experiment_id = experiment.experiment_id):
    # Create a Lasso regression pipeline
    lasso_alpha = 1.0  # Adjust this based on your model tuning
    lasso_regressor = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', Lasso(alpha=lasso_alpha))
    ])

    # Fit the model
    lasso_regressor.fit(X_train, Y_train)
    
    # Store metrics
    predicted_qualities = lasso_regressor.predict(X_test)
    RMSE = np.sqrt(mean_squared_error(Y_test, predicted_qualities))
    R2_train = lasso_regressor.score(X_train, Y_train)
    R2_test = lasso_regressor.score(X_test, Y_test)
    
    
    # Print results
    print("RMSE: ", RMSE)
    print("R2_train: ", R2_train)
    print("R2_test: ", R2_test)

    # Log Metric 
    mlflow.log_metric("RMSE", RMSE)
    mlflow.log_metric("R2_train", R2_train)
    mlflow.log_metric("R2_test", R2_test)