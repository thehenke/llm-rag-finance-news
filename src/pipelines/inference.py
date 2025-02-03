from langchain_core.prompts import PromptTemplate
from src.engines.embeddings import VectorIndex

class RAGInference():
    def __init__(self):
        template = "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        self.retriever = VectorIndex().retriever
        print(self.retriever)

rag = RAGInference()