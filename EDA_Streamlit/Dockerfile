FROM continuumio/miniconda3

# Set working directory
WORKDIR /home/app

# Copy requirements file and install dependencies
COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Copy the entire project directory
COPY . .

# Set environment variables
ENV PORT_STREAMLIT=8503 \
    BACKEND_STORE_URI=sqlite:///mlflow.db \
    ARTIFACT_STORE_URI=/home/app/artifacts

# Expose port
EXPOSE $PORT_STREAMLIT

# Command to run Streamlit app
CMD streamlit run Getaround_analysis.py --server.port $PORT_STREAMLIT
