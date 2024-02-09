FROM continuumio/miniconda3

# Set working directory
WORKDIR /home/app

# Copy requirements file and install dependencies
COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Copy the entire project directory
COPY . .

# Set environment variables
ENV PORT_MLFLOW=8501 \
    BACKEND_STORE_URI=sqlite:///mlflow.db \
    ARTIFACT_STORE_URI=/home/app/artifacts

# Expose ports
EXPOSE $PORT_MLFLOW

# Command to run MLflow server
CMD mlflow server -p $PORT_MLFLOW \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI ; \
    --default-artifact-root $ARTIFACT_STORE_URI ; \