from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever
from typing import List, Dict
import asyncio 
import numpy as np
from src.engines.embeddings import VectorIndex, GoogleEmbeddingFunction
from src.engines.sqlite import SQLite
from src.utils.tonkenizer import word_tokenize

class SelfRetriver():
    def __init__(self):
        self.vectorstore = VectorIndex()

    def retrieve(self, query: str) -> List[Document]:
        docs = self.vectorstore.chroma.similarity_search(query=query)
        return docs


class HybridRetriever():
    def __init__(self):
        self.vectorstore = VectorIndex()
        self.embedder = GoogleEmbeddingFunction()
        self.sqlite = SQLite()
        

    async def retrieve(self, query: str) -> List[Dict]:
        """
        Realiza a recuperação de documentos combinando abordagens léxica e semântica de forma assíncrona.

        Args:
            query (str): A consulta de pesquisa.

        Returns:
            List[Dict]: Lista de documentos relevantes após fusão e remoção de duplicatas.
        """

        lexic_task = asyncio.create_task(self.__lexic_retrieval(query))
        semantic_task = asyncio.create_task(self.__semantic_retrieve(query))

        lexic_docs, semantic_docs = await asyncio.gather(lexic_task, semantic_task)

        print(f"[INFO] {len(lexic_docs)} lexic docs retrieved")
        print(f"[INFO] {len(semantic_docs)} semantic docs retrieved")

        unique_relevant_docs = self.__merge_and_deduplicate(lexic_docs, semantic_docs)
        unique_reranked_docs = self.__rerank(query=query, docs=unique_relevant_docs, top_k=8)

        print(f"[INFO] {len(unique_relevant_docs)} unique docs merged")
        print(f"[INFO] {len(unique_reranked_docs)} unique docs reranked")

        return unique_reranked_docs

    async def __semantic_retrieve(self, query: str) -> List[Document]:
        """
        Realiza a recuperação semântica de documentos.

        Args:
            query (str): A consulta de pesquisa.

        Returns:
            List[Dict]: Lista de documentos recuperados.
        """

        docs = self.vectorstore.chroma.similarity_search(query=query)
        return docs
    
    async def __lexic_retrieval(self, query) -> List[Document]:
        """
        Realiza a recuperação léxica de documentos.

        Args:
            query (str): A consulta de pesquisa.

        Returns:
            List[Dict]: Lista de documentos recuperados.
        """
        rows = self.sqlite.query("SELECT DISTINCT * FROM articles")

        data = [{
            "id":           row[0],
            "title":        row[1],
            "author":       row[2], 
            "source":       row[3], 
            "description":  row[4], 
            "content":      row[5], 
            "url":          row[6], 
            "published_at": row[7], 
            "requested_at": row[8] 
        } for row in rows]
        
        documents = []

        for row in data:
            row_text = " ".join([f"{key}: {value}" for key, value in row.items()])
            documents.append(Document(page_content=row_text, id=row['id']))

        retriever = BM25Retriever.from_documents(
            documents,
            k=8,
            preprocess_func=word_tokenize,
        )

        relevant_docs = retriever.invoke(query)

        return relevant_docs
    
    def __merge_and_deduplicate(
            self, 
            lexic_docs: List[Document], 
            semantic_docs: List[Document]
        ) -> List[dict]:

        """
        Mescla e remove duplicatas dos documentos recuperados.

        Args:
            lexic_docs (List[Dict]): Documentos recuperados por busca léxica.
            semantic_docs (List[Dict]): Documentos recuperados por busca semântica.

        Returns:
            List[Dict]: Lista de documentos únicos após a fusão.
        """
        
        unique_docs = {}
    
        for doc in lexic_docs + semantic_docs:
            if doc.id not in unique_docs:  # Acessando diretamente doc.id
                unique_docs[doc.id] = {
                    "id": doc.id,
                    "page_content": doc.page_content
                }
        
        return list(unique_docs.values())
    
    def __rerank(self, query: str, docs: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Reordena os documentos com base na similaridade semântica com a consulta.

        Args:
            query (str): A consulta de pesquisa.
            docs (List[Dict]): Lista de documentos a serem rerankeados.
            top_k (int): Número máximo de documentos rerankeados a serem retornados.

        Returns:
            List[Dict]: Lista de documentos rerankeados.
        """
        if not docs:
            return []

        query_embedding = self.embedder.embed_query(query)
        doc_embeddings = [self.embedder.embed_query(doc["page_content"]) for doc in docs]
        
        similarities = [self.__cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
        
        ranked_docs = sorted(zip(docs, similarities), key=lambda x: x[1], reverse=True)
        
        return [doc for doc, _ in ranked_docs[:top_k]]
                
    def __cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula a similaridade do cosseno entre dois vetores."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
class MultiQueryRetriever():
    def __init(self, query):
        self.query
    
    def retrieve(self):
        pass
