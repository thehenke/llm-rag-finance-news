from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

from src.engines.embeddings import VectorIndex, GoogleEmbeddingFunction
from src.prompt.rag import template
from src.engines.retriever import  HybridRetriever, SelfRetriver

load_dotenv()

class RAGInference():
    """
    Classe responsável por executar inferência em um sistema de Recuperação Aumentada por Geração (RAG).
    """
    def __init__(self):
        """
        Inicializa a classe RAGInference, configurando os componentes necessários para a recuperação e geração de respostas.
        """
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
        """
        Formata a lista de documentos em um único texto concatenado.

        Args:
            docs (list): Lista de dicionários contendo os documentos recuperados.

        Returns:
            str: Texto formatado contendo o conteúdo dos documentos recuperados.
        """
        return "\n\n".join(doc['page_content'] for doc in docs)

    async def run(self, query=None):
        """
        Executa o fluxo completo de recuperação e geração de resposta para uma consulta dada.

        Args:
            query (str, optional): A consulta do usuário. Defaults to None.

        Returns:
            str: A resposta gerada pelo modelo de linguagem.
        """
        docs = await self.retriever.retrieve(query=query)
        
        formatted_docs = self.__format_docs(docs)

        
        context = {"context": formatted_docs, "question": query}
        
        rag_chain = (
            RunnableLambda(lambda _: context)
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        response = rag_chain.invoke(context)
        return response

