from fastapi import FastAPI
from pydantic import BaseModel
import random
import uvicorn

if __name__ == "__main__":
    uvicorn.run("generator:app", host="0.0.0.0", port=5000, reload=False, log_level="debug")


app = FastAPI()

class GenerateRequest(BaseModel):
    model_name: str
    viewerid: int

@app.post("/generate")
def generate(request: GenerateRequest):
    model_name = request.model_name
    viewer_id = request.viewerid
    random_number = random.randint(1, viewer_id)
    return {"reason": model_name, "result": random_number}
