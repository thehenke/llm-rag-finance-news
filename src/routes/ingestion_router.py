from fastapi import APIRouter

router = APIRouter()

@router.post("/ingestion")
async def ingestion():
    return {"message": "Ingestion endpoint"}