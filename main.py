import time
import random
import uuid
import asyncio
from typing import Dict, Union
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()


# Define the input model
class PredictRequest(BaseModel):
    input: str


# Define the synchronous response model
class PredictResponse(BaseModel):
    input: str
    result: str


# Define the asynchronous response model
class AsyncPredictResponse(BaseModel):
    message: str
    prediction_id: str


# Define the result response model
class ResultResponse(BaseModel):
    prediction_id: str
    output: Dict[str, str]


# Define the mock prediction function
def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(8, 15))  # Simulate processing delay
    result = str(random.randint(100, 10000))
    output = {"input": input, "result": result}
    return output


# In-memory storage for prediction results
predictions = {}
executor = ThreadPoolExecutor()


# Endpoint to check prediction status
@app.get("/status/{prediction_id}", response_model=Dict[str, str])
async def get_status(prediction_id: str):
    if prediction_id not in predictions:
        raise HTTPException(status_code=404, detail="Prediction ID not found")
    return predictions[prediction_id]


# Endpoint to retrieve prediction results
@app.get("/predict/{prediction_id}", response_model=ResultResponse)
async def get_prediction(prediction_id: str):
    if prediction_id not in predictions:
        raise HTTPException(status_code=404, detail="Prediction ID not found.")

    prediction = predictions[prediction_id]
    if prediction.get("status") == "Processing":
        raise HTTPException(status_code=400, detail="Prediction is still being processed.")

    return {"prediction_id": prediction_id, "output": prediction}


# Asynchronous function to handle the prediction process
async def handle_async_prediction(input: str, prediction_id: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, mock_model_predict, input)
    predictions[prediction_id] = result


# Define the /predict endpoint
@app.post("/predict", response_model=Union[PredictResponse, AsyncPredictResponse])
async def predict(request: PredictRequest, async_mode: bool = Header(None)):
    if async_mode:
        # Asynchronous mode
        prediction_id = str(uuid.uuid4())
        predictions[prediction_id] = {"status": "Processing"}
        asyncio.create_task(handle_async_prediction(request.input, prediction_id))
        return {"message": "Request received. Processing asynchronously.", "prediction_id": prediction_id}
    else:
        # Synchronous mode
        response = mock_model_predict(request.input)
        return response


# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
