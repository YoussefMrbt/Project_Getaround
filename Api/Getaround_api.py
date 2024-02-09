from flask import Flask, request, jsonify
import pandas as pd
import random
import joblib
import pickle

app = Flask(__name__)

# Define the home page
@app.route('/')
def home():
    return 'Hello World!'

# Offer choice of loading a model from mlflow or from a pickle file
choice = input('Do you want to load a model from mlflow? (y/n) ')

if choice == 'y':
    # Load model from mlflow
    import mlflow
    import mlflow.sklearn
    import os

    # Set tracking URI to your Heroku application
    mlflow.set_tracking_uri("http://localhost:8501")
    #mlflow.set_tracking_uri(os.environ["APP_URI"])
    
# Offer choice of providing a model or using a default model
choice = input('Do you want to provide a model? (y/n) ')
if choice == 'y':
    # Load model from pickle file
    model_path = input('Enter the model path: ')
    model = pickle.load(open(model_path, 'rb'))

else:
    # Load default model pickle
    model = pickle.load(open('model.pkl', 'rb'))


# Preprocess the input features
def preprocess(features):
    columns = ['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color',
        'car_type', 'private_parking_available', 'has_gps',
        'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
        'has_speed_regulator', 'winter_tires']
    print(columns)
    # X dataframe
    X = pd.DataFrame(columns=columns)
    print(X)
    id = random.randint(0, 1000000)
    X.loc[id] = features
    print(X)
    
    # Features into a dataframe
    features = pd.DataFrame([features], columns=X.columns)
    
    # Identify categorical and numerical columns
    categorical_cols = [col for col in features.columns if features[col].dtype == 'object']
    numerical_cols = [col for col in features.columns if features[col].dtype in ['int64', 'float64']]
    print(categorical_cols)
    print(numerical_cols)
    
    return features



@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.get_json()
    features = data['features']
    features = preprocess(features)
    
    # Predict using the loaded model
    prediction = model.predict(features)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction.tolist()})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)
