import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer

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
    
    
class VectorIndex():
    def __init__(
            self, 
            chuk_size=200, 
            chunk_overlap=50, 
            persist_directory='src/database/store'
        ):
        self.PERSIST_DIRECTORY=persist_directory
        self.CHUNK_SIZE=chuk_size 
        self.CHUNK_OVERLAP=chunk_overlap

    def retrieval():
        pass
    
    def store(self, docs):
        print('[INFO] - Iniciando storage no vector store')

        embedding_function = SBERTEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, chunk_overlap=self.CHUNK_OVERLAP, add_start_index=True
        )

        all_splits = text_splitter.split_documents(docs)

        print('[INFO] - Splits de documento gerados')

        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=embedding_function,
            persist_directory=self.PERSIST_DIRECTORY
        )

        print(f'[INFO] - Concluído storage no vector store {vectorstore}')
