from fastapi import APIRouter
from pipelines.ingestion import DataIngestion

router = APIRouter()


@router.post("/ingestion")
async def ingestion():

    DataIngestion().run(get_data_from_api=True)

    return {"message": "Ingestion was successfuly concluded."}