from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter, Histogram
import time
import random

app = FastAPI()

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Define metrics
request_counter = Counter('agent_requests_total', 'Total number of requests')
request_latency = Histogram('agent_request_latency_seconds', 'Request latency in seconds')

@app.get("/")
async def root():
    with request_latency.time():
        request_counter.inc()
        # Simulate some processing time
        time.sleep(random.uniform(0.1, 0.3))
        return {"message": "ML Agent Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 