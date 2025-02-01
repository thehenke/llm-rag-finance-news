import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
# from langchain_community.embeddings.sentence_transformer import (
#     SentenceTransformerEmbeddings,
# )
# from src.config import config

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
print(HUGGINGFACE_TOKEN)


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
    PERSIST_DIRECTORY='src/database/store'
    CHUNK_SIZE=200 
    CHUNK_OVERLAP=50

    def retrieval():
        pass
    
    def store(self, docs):
        print('[INFO] - Iniciando storage no vector store')

        embedding_function = SBERTEmbeddingFunction("sentence-transformers/all-MiniLM-L6-v2")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, chunk_overlap=self.CHUNK_OVERLAP, add_start_index=True
        )

        all_splits = text_splitter.split_documents(docs)
        print('[INFO] - Splits gerados')

        # Crie o Chroma vectorstore usando os embeddings do SBERT

        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=embedding_function,
            persist_directory=self.PERSIST_DIRECTORY
        )

        print(f'[INFO] - Concluído storage no vector store {vectorstore}')

    @staticmethod
    def test():
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=HUGGINGFACE_TOKEN)

        sentences = [
            "That is a happy person",
            "That is a happy dog",
            "That is a very happy person",
            "Today is a sunny day"
        ]
        embeddings = model.encode(sentences)

        similarities = model.similarity(embeddings, embeddings)
        print(similarities)
        # [4, 4]