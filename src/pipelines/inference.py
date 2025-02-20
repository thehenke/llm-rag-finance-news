from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from engines.embeddings import VectorIndex
from prompt.rag import template

load_dotenv()

class RAGInference():
    def __init__(self):
        self.template = template()
        self.prompt = PromptTemplate(template=self.template, input_variables=["context", "question"])
        self.vectorstore = VectorIndex()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=1.0,
            max_tokens=1000,
            timeout=None,
            max_retries=2,
        )

    def __format_docs(self, docs):
        return "\n\n".join(doc['page_content'] for doc in docs)

    def run(self, query=None):
        retrieved_docs = self.vectorstore.retrieve_documents(query)
        
        formatted_docs = self.__format_docs(retrieved_docs)
        # print(formatted_docs)
        context = {"context": formatted_docs, "question": query}
        
        rag_chain = (
            RunnableLambda(lambda _: context)
            | self.prompt
            # | RunnableLambda(lambda result: print(f"Prompt: {result}"))
            | self.llm
            | StrOutputParser()
        )
        
        response = rag_chain.invoke(context)
        return response

# rag = RAGInference().run(query='Tem algo falando sobre Central bank digital currency ou CBDC ? Cite quem foram os autores e as noticias')
# print(rag)
