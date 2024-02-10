
# Rental Price Prediction Project

## Overview

This project is designed to predict the daily rental price for vehicles listed on a platform similar to Getaround. It encompasses a complete workflow from exploratory data analysis (EDA) to model training and deployment of a prediction API. The goal is to leverage historical rental data to forecast prices, enhancing pricing strategies and user experience.

The repository is organized into several directories, each serving a specific purpose within the project:

/api/: Contains the Flask application files for deploying the trained model as a web service. This API serves predictions on rental price per day based on input features.

/EDA_streamlit/: This directory houses both the Jupyter notebook with detailed EDA and a Python script for a Streamlit application. The notebook provides insights into the data, while the Streamlit app offers an interactive way to explore these insights visually.

/Train_model/: Includes scripts used for training machine learning models. These scripts detail the process of model selection, training, validation, and evaluation, leading to the final model used for the prediction API.

/ML/: Contains a comprehensive Jupyter notebook that outlines the entire machine learning pipeline, from data preprocessing to model training and evaluation.

requirements.txt: Lists all the Python dependencies required for the project.

Dockerfile: Provides the setup for containerizing the application, ensuring it can run in any environment with Docker.

## Deployment on Heroku

On this repository:
https://github.com/YoussefMrbt/Getaround_api

## Contributing

Contributions to improve the project are welcome. Please follow the standard fork-and-pull request workflow. If you have suggestions or encounter issues, please file them via GitHub issues.
