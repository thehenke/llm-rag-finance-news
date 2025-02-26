from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from src.engines.embeddings import VectorIndex, GoogleEmbeddingFunction
from src.prompt.rag import template
from src.engines.retriever import  HybridRetriever, SelfRetriver

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
        self.retriever = HybridRetriever()

    def __format_docs(self, docs):
        return "\n\n".join(doc['page_content'] for doc in docs)

    def run(self, query=None):
        docs = self.retriever.retrieve(query=query)
        
        formatted_docs = self.__format_docs(docs)
        print(formatted_docs)
        
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

query = 'Fale sobre a petrobras e mineração de bitcoins'
# embedder = GoogleEmbeddingFunction()
# query_embedded = embedder.embed_query(query)
rag = RAGInference().run(query=query)
print(rag)
