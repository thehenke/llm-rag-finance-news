import json
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from src.pipelines.inference import RAGInference

router = APIRouter()
rag = RAGInference()

class InferenceRequest(BaseModel):
    query: str = Field(..., description="The query parameter is required")

@router.post("/inference")
async def inference(request: Request):
    try:
        body = await request.body()

        if not body:
            raise HTTPException(
                status_code=400, 
                detail={"error": "Request body is required in JSON format"}
            )
        
        body_json = json.loads(body)

        query = body_json.get("query")

        if not query:
            raise HTTPException(
                status_code=400, 
                detail={"error": "'query' string parameter is required in JSON"}
            )
        
        result = await rag.run(query=query)

        return result
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail={"error": "Invalid JSON format", "hint": "Ensure the request body is a valid JSON."})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "detail": str(e)})