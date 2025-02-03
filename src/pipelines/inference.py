from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.engines.embeddings import VectorIndex

class RAGInference():
    def __init__(self):
        template = "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        self.retriever = VectorIndex().retriever
        self.llm = Ollama(model="llama3.2:latest")

    def __format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def run(self, query=None):
        rag_chain = (
            {"context": self.retriever | self.__format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(query)
        print(response)

rag = RAGInference().run(query='O que você sabe sobre bitcoin ?')