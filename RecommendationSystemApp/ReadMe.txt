# Recommendation System #

## Overview

This recommendation system consists of two services: `Generator` and `Invoker`. 

### Services

- **Generator Service**: Generates random recommendations based on the model name and viewer's id.
- **Invoker Service**: Manages recommendation requests, caching, and fetching recommendations from the `Generator` service.

### Local and Redis Caching

- **Local Cache**: TTL of 10 seconds, limited to 3 keys.
- **Redis Cache**: Stores data with a TTL of 25 seconds.

### Setup

1. Clone the repository.
2. Navigate to the repository directory.
3. Run `docker-compose up --build` to start the services.

### Endpoints

- **Generator Service**
  - `POST /generate`
    - **Parameters**: `model_name`, `viewerid`
    - **Response**: `{"reason": <MODELNAME>, "result": <RANDOMNUMBER>}` 
- **Invoker Service**
  - `GET /recommend`
    - **Parameters**: `viewer_id`
    - **Response**: Recommendations data or cached data.

ATTENTION 1: RANDOMNUMBER is randomly generated number between 1-viewerid (hardcoded)
ATTENTION 2: MODELNAME in this implementation is any string between model1-model5 (if you use invoker) or any other string (if you use generator).

