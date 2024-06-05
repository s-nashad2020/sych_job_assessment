from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
import time
import random
import uuid
from typing import Dict
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = FastAPI()

# Define the input model
class PredictRequest(BaseModel):
    input: str

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

# Asynchronous function to handle the prediction process
async def handle_async_prediction(input: str, prediction_id: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, mock_model_predict, input)
    predictions[prediction_id] = result

# Define the /predict endpoint
@app.post("/predict", response_model=Dict[str, str])
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
