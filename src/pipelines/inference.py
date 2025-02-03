from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.engines.embeddings import VectorIndex

class RAGInference():
    def __init__(self):
        template = "Contexto:\n{context}\n\n Pergunta: {question}"
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        self.retriever = VectorIndex().retriever
        self.llm = OllamaLLM(model="dk:latest")

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


        docs = self.retriever.get_relevant_documents(query)
        formatted_prompt = self.prompt.format(context=self.__format_docs(docs), question=query)
        print("------------------Prompt final:")
        print(formatted_prompt)
        print("------------ DOCS ")
        print(docs)

        # response = rag_chain.invoke(query)
        # print(response)


rag = RAGInference().run(query='O que estão falando do bitcoin nas noticias ?')