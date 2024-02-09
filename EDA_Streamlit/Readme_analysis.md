#   Getaround Rental Timing Optimization Analysis

##  Project Overview

This project aims to analyze and optimize the minimum delay between consecutive rentals on Getaround, a platform facilitating peer-to-peer car rentals. Through comprehensive Exploratory Data Analysis (EDA), we assess the impact of introducing a minimum delay on user satisfaction and owner revenue, and propose actionable insights to balance operational efficiency with customer experience.

##  Repository Structure
This repository is organized into several key components to facilitate easy navigation and understanding of the analysis:

/data/: Contains the dataset used for analysis, stored as a CSV file. The dataset includes information on rental timings, car types, and more, crucial for understanding the dynamics of rental delays and their impacts.
Getaround_Analysis.ipynb: A Jupyter notebook containing detailed exploratory data analysis. This notebook explores various aspects of the rental data, evaluates the potential impact of implementing minimum delays between rentals, and suggests optimal strategies for deployment.
Getaround_analysis.py: A Python script designed to run a Streamlit application, which presents the analysis findings in a more interactive and visually appealing format. This application allows users to explore the data and insights through graphical representations and interactive widgets.

##  Using the Streamlit Application
The Streamlit application provides an interactive way to explore the data analysis. To run the Streamlit application, follow these steps:

docker build . -t streamlit_eda

docker run -p 8503:8503 -e PORT_STREAMLIT=8503 -e BACKEND_STORE_URI=sqlite:///mlflow.db streamlit_eda

If not using Docker:
Run the Streamlit Application: Execute the Streamlit application by running the following command in your terminal:

streamlit run Getaround_analysis.py

Explore the Application: Once the application is running, your default web browser should automatically open a new tab directed to the local server hosting the Streamlit application (typically http://localhost:8503). 
You can interact with the visualizations and explore the analysis findings through the web interface.

##  Dataset
The dataset in the /data/ directory is pivotal to our analysis. It includes detailed records of car rentals, including start and end times, car types, and user interactions. Note that this data is used under the assumption of compliance with privacy and data protection regulations.

##  Contributing
We welcome contributions and suggestions to improve the analysis and the Streamlit application. Please feel free to fork the repository, make changes, and submit pull requests. For major changes or questions, please open an issue first to discuss what you would like to change.