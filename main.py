import time
import random
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PredictInput(BaseModel):
    input: str

class PredictOutput(BaseModel):
    input: str
    result: str

def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(8, 15))  # Simulate processing delay
    result = str(random.randint(100, 10000))
    output = {"input": input, "result": result}
    return output

@app.post("/predict", response_model=PredictOutput)
def predict(input_data: PredictInput):
    try:
        output = mock_model_predict(input_data.input)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
