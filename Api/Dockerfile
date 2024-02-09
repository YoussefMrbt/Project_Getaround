FROM continuumio/miniconda3

# Set working directory
WORKDIR /home/app

# Copy requirements file and install dependencies
COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Copy the entire project directory
COPY . .

# Set environment variables
ENV PORT_API=8502 \
    BACKEND_STORE_URI=sqlite:///mlflow.db

# Expose the API port
EXPOSE $PORT_API

# Command to run the API
CMD flask Api/Getaround_api:app --host 0.0.0.0 --port $PORT_API