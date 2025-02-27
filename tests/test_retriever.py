import pytest
from src.engines.retriever import HybridRetriever, SelfRetriver

@pytest.mark.asyncio
async def test_hybrid_retriever():
    retriever = HybridRetriever()  # instanciando normalmente se a classe for síncrona
    result = await retriever.retrieve("Bitcoin")  # chamando de forma assíncrona se o método for assíncrono
    assert isinstance(result, list)

def test_self_retriever():
    retriever = SelfRetriver()
    result = retriever.retrieve("Bitcoin")
    assert isinstance(result, list)