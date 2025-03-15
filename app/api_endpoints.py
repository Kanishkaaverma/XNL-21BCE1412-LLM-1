from fastapi import FastAPI, HTTPException # type: ignore
import redis # type: ignore
from transformers import pipeline
import os
import logging
import time

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Load the sentiment analysis model
model_path = os.path.abspath("./models/sentiment_model")  # Ensure this path is correct
sentiment_analyzer = pipeline("sentiment-analysis", model=model_path)

# Set up logging
logging.basicConfig(level=logging.INFO)

async def analyze_sentiment(prompt):
    start_time = time.time()
    response = sentiment_analyzer(prompt)
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    return response, elapsed_time

@app.post("/query")
async def query_llm(prompt: str):
    cached_response = redis_client.get(prompt)
    if cached_response:
        return {"response": cached_response.decode("utf-8")}

    try:
        response, elapsed_time = await analyze_sentiment(prompt)
        
        # Check if response time is acceptable
        if elapsed_time <= 10:  # 10 ms threshold
            # Cache the response
            redis_client.set(prompt, str(response[0]), ex=60)  # Cache for 60 seconds
            return {"response": response[0]['label']}
        else:
            return {"response": "The model took too long to respond. Please try again."}
    
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"response": "An error occurred while processing your request."}