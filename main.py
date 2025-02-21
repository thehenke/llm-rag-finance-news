from fastapi import FastAPI
from src.routes import inference_router, ingestion_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

app.include_router(inference_router, prefix="/v1")
app.include_router(ingestion_router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
