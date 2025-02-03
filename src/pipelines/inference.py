from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from src.engines.embeddings import VectorIndex

class RAGInference():
    def __init__(self):
        template = "Contexto:\n{context}\n\n Pergunta: {question}"
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        self.retriever = VectorIndex().retriever
        self.llm = OllamaLLM(model="llama3.2:latest")

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

        # rag_chain_from_docs = (
        #     RunnablePassthrough.assign(context=(lambda x: self.__format_docs(x["context"])))
        #     | self.prompt
        #     | self.llm
        #     | StrOutputParser()
        # )

        # rag_chain_with_source = RunnableParallel(
        #     {"context": self.retriever, "question": RunnablePassthrough()}
        # ).assign(answer=rag_chain_from_docs)

        # for chunk in rag_chain_with_source.stream(query):
        #     print(chunk)

        # docs = self.retriever.get_relevant_documents(query)
        # formatted_prompt = self.prompt.format(context=self.__format_docs(docs), question=query)
        # print("------------------Prompt final:")
        # print(formatted_prompt)
        # print("------------ DOCS ")
        # print(docs)



rag = RAGInference().run(query='O que a InfoMoney está dizendo sobre o bitcoin? Faça um resumo e de insights em topicos, considerando as datas. Faça um resumo de contexto destacando os principais pontos.')