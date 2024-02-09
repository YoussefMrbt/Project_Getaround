#   Flask API for Vehicle Price Prediction

This Flask API provides an interface for predicting vehicle prices based on various features including make, mileage, engine power, and more. 
The API is built using a machine learning model trained on historical vehicle data.

##  Requirements

Docker (if running via Docker container)
Python 3.7 or later (if running locally without Docker)
Flask
Other Python libraries as specified in requirements.txt

##  Running the API

###  Using Docker

- Build the Docker image:
docker build -t vehicle-price-prediction-api .

- Run the Docker container:
docker run -p 8502:8502 -e PORT_API=8502 -e BACKEND_STORE_URI=sqlite:///mlflow.db vehicle-price-prediction-api

###  Running Locally

- Install dependencies:
pip install -r requirements.txt

- Start the Flask application:
python Getaround_api.py

## Making Predictions

To make a prediction, you need to send a POST request with a JSON payload that contains the input features. The expected format and value ranges for each feature are detailed below:

## Request Format

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"features\": [\"Brand\", Mileage, EnginePower, \"Fuel\", \"Paint\", \"Type\", Parking, GPS, AC, Automatic, Connected, SpeedRegulator, WinterTires]}" http://localhost:8501/predict
```

- Brand: String. Allowed values include: 'Citroën', 'Peugeot', 'PGO', 'Renault', 'Audi', 'BMW', 'Ford', 'Mercedes', 'Opel', 'Porsche', 'Volkswagen', 'KIA Motors', 'Alfa Romeo', 'Ferrari', 'Fiat', 'Lamborghini', 'Maserati', 'Lexus', 'Honda', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan', 'SEAT', 'Subaru', 'Suzuki', 'Toyota', 'Yamaha'.
- Mileage: Integer. Range: [0, 1000376].
- EnginePower: Integer. Range: [0, 423].
- Fuel: String. Allowed values: 'diesel', 'petrol', 'hybrid_petrol', 'electro'.
- Paint: String. Allowed colors: 'black', 'grey', 'white', 'red', 'silver', 'blue', 'orange', 'beige', 'brown', 'green'.
- Type: String. Allowed types: 'convertible', 'coupe', 'estate', 'hatchback', 'sedan', 'subcompact', 'suv', 'van'.
- Parking: Binary (0 or 1).
- GPS: Binary (0 or 1).
- AC: Binary (0 or 1).
- Automatic: Binary (0 or 1).
- Connected: Binary (0 or 1).
- SpeedRegulator: Binary (0 or 1).
- WinterTires: Binary (0 or 1).

##  Response
The API responds with the predicted vehicle price, in a JSON format like:
{
  "predicted_price": VALUE
}

##  Note
This API is for demonstration purposes and runs in a development server. For production use, consider deploying with a WSGI server such as Gunicorn.

##  License
Specify your license or state that the project is unlicensed.