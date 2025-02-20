from fastapi import APIRouter
from pipelines.inference import RAGInference

router = APIRouter()
rag = RAGInference()

@router.post("/inference")
async def inference():
    result = rag.run(query='Faça um resumo em topicos sobre o bitcoin e também outras criptomoedas relacionadas.')
    return {"result": result}