import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

class SBERTEmbeddingFunction:
    """Classe para adaptar o SentenceTransformer ao formato esperado pelo LangChain."""
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name, token=HUGGINGFACE_TOKEN)

    def embed_documents(self, texts):
        """Gera embeddings para múltiplos documentos."""
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        """Gera embeddings para uma única consulta."""
        return self.model.encode([text], convert_to_numpy=True).tolist()[0]


class GoogleEmbeddingFunction:
    """Classe para adaptar GoogleGenerativeAIEmbeddings ao formato esperado pelo LangChain."""
    def __init__(self, model_name="models/text-embedding-004"):
        self.model = GoogleGenerativeAIEmbeddings(model=model_name, region='us-central1')

    def embed_documents(self, texts):
        """Gera embeddings para múltiplos documentos."""
        return [self.model.embed_query(text) for text in texts]

    def embed_query(self, text):
        """Gera embeddings para uma única consulta."""
        return self.model.embed_query(text)
    
    
class VectorIndex():
    def __init__(
            self, 
            chuk_size=1000, 
            chunk_overlap=50, 
            persist_directory='database/store',
            collection_name='articles'
        ):
        self.PERSIST_DIRECTORY=persist_directory
        self.CHUNK_SIZE=chuk_size 
        self.CHUNK_OVERLAP=chunk_overlap
        self.embedding_function = GoogleEmbeddingFunction()
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_function,
            persist_directory=self.PERSIST_DIRECTORY
        )
        self.__retriever = self.__set_retriever()

    def retrieve_documents(self, query, k=6, score_threshold=0.5):
        print(f'[INFO] - Buscando documentos para a query: "{query}"')
        results = self.__retriever.invoke(query)
        
        relevant_docs = []
        for doc in results:
            relevant_docs.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return relevant_docs

    def get_vectorstore(self):
        return self.vectorstore
    
    def __set_retriever(self):
        retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 6,
                "score_threshold": 0.5,
            }
        )

        return retriever
    
    def store(self, docs):

        print('[INFO] - Iniciando storage no vector store')

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, 
            chunk_overlap=self.CHUNK_OVERLAP, 
            add_start_index=True
        )

        all_splits = text_splitter.split_documents(docs)
        print('[INFO] - Splits de documento gerados')

        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=self.embedding_function,
            persist_directory=self.PERSIST_DIRECTORY
        )

        print(f'[INFO] - Concluído storage no vector store {vectorstore}')

    def __multiquery_retrieval_augmented(self):
        pass

# teste = VectorIndex().retrieve_documents(query="o que fazer com as noticias de bitcoin")
# print(teste)