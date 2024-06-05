# FastAPI Model Prediction Service

This is a lightweight web service built with FastAPI, allowing users to run machine learning model predictions synchronously and asynchronously.

## Features

- **Synchronous and Asynchronous Prediction**: This service supports both synchronous and asynchronous modes of prediction, giving users flexibility based on their requirements.
- **Status Checking**: Users can check the status of their prediction requests using dedicated endpoints.
- **Result Retrieval**: Once predictions are processed, users can retrieve the results by prediction ID.
- **In-Memory Storage**: The service utilizes in-memory storage for prediction results, ensuring fast access and retrieval.

## Endpoints

- **POST /predict**: Submit prediction requests using this endpoint. Users can include JSON input with an optional Async-Mode header to specify asynchronous processing.
- **GET /status/{prediction_id}**: Check the status of a prediction request by providing its unique prediction ID.
- **GET /predict/{prediction_id}**: Retrieve prediction results by specifying the prediction ID.

## Running the Service

1. **Install Dependencies**: Ensure you have FastAPI and Uvicorn installed. If not, you can install them using pip:

  pip install fastapi uvicorn


2. **Run the FastAPI Server**: Use the following command to start the FastAPI server:

  uvicorn main --host 0.0.0.0 --port 8080


3. **Send Requests**: Once the server is running, you can send requests to the service using tools like cURL or Postman.

## Dockerfile

The Dockerfile included in this project is used to containerize the FastAPI application. It sets up a Python environment, installs dependencies, and runs the FastAPI server.

### Building the Docker Image

1. **Build the Docker Image**: Execute the following command to build the Docker image:

  docker build -t fastapi-prediction-service .


2. **Run the Docker Container**: Once the Docker image is built, you can run the Docker container with the following command:

  docker run -d -p 8080:8080 fastapi-prediction-service


## Contributors

- [Shaheer Nashad](https://github.com/s-nashad2020)
