from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from engines.embeddings import VectorIndex
from prompt.rag import template


load_dotenv()

class RAGInference():
    def __init__(self):
        self.template = template()
        self.prompt = PromptTemplate(template=self.template, input_variables=["context", "question"])
        self.retriever = VectorIndex().retriever
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=1.0,
            max_tokens=1000,
            timeout=None,
            max_retries=2,
        )

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
        yield response

# rag = RAGInference().run(query='Faça um resumo em topicos sobre o bitcoin e também outras criptomoedas relacionadas.')