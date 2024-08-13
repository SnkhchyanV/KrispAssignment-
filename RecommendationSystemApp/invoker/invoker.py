from fastapi import FastAPI, Query
import httpx
import redis
import uvicorn
from cachetools import TTLCache
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json


if __name__ == "__main__":
    # for manual tests
    uvicorn.run("invoker:app", host="0.0.0.0", port=5001, reload=False, log_level="debug")


app = FastAPI()

# Local cache with TTL
local_cache = TTLCache(maxsize=3, ttl=10)
# Redis cache setup 
# ! edit host parameter if ran on local machine, set localhost(or any other local host)   
redis_cache = redis.StrictRedis(host='redis', port=6379, db=0)
executor = ThreadPoolExecutor(max_workers=5)

GENERATOR_SERVICE_URL = 'http://generator:5000/generate'

async def fetch_from_generator(model_name: str, viewer_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(GENERATOR_SERVICE_URL, json={"model_name": model_name, "viewerid": viewer_id})
        return response.json()

async def runcascade(viewer_id: int) -> dict:
    models = ['model1', 'model2', 'model3', 'model4', 'model5']
    tasks = [fetch_from_generator(model, viewer_id) for model in models]
    results = await asyncio.gather(*tasks)
    return {"viewer_id": viewer_id, "results": results}

@app.get("/recommend")
async def recommend(viewer_id: int):
    # Firstly check if data is in the local cache
    
    print('Checking local cache')
    if viewer_id in local_cache: 
        return local_cache[viewer_id]
    

    # Then check Redis cache
    print('Checking Redis cache')
    redis_result = redis_cache.get(viewer_id)
    if redis_result:
        return json.loads(redis_result)
    
    # If not in cache, run cascade and cache result
    print('Cashing')
    result = await runcascade(viewer_id)
    local_cache[viewer_id] = result
    redis_cache.set(viewer_id, json.dumps(result), ex=25)  # Redis TTL is 25 seconds for demonstration
    return result
