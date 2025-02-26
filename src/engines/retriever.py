from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever
from typing import List

from src.engines.embeddings import VectorIndex
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
        self.sqlite = SQLite()
        

    def retrieve(self, query: str) -> List[dict]:
        lexic_docs = self.__lexic_retrieval(query=query)
        semantic_docs = self.__sementic_retrieve(query=query)

        print(f"[INFO] {len(lexic_docs)} lexic docs retrieved")
        print(f"[INFO] {len(semantic_docs)} semantic docs retrieved")

        unique_relevant_docs = self.__merge_and_deduplicate(lexic_docs, semantic_docs)

        print(f"[INFO] {len(unique_relevant_docs)} unique docs merged")

        return unique_relevant_docs

    def __sementic_retrieve(self, query: str) -> List[Document]:
        docs = self.vectorstore.chroma.similarity_search(query=query)
        return docs
    
    def __lexic_retrieval(self, query) -> List[Document]:
        # print(self.sqlite)
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
        
        unique_docs = {}
    
        for doc in lexic_docs + semantic_docs:
            if doc.id not in unique_docs:  # Acessando diretamente doc.id
                unique_docs[doc.id] = {
                    "id": doc.id,
                    "page_content": doc.page_content
                }
        
        return list(unique_docs.values())
    
    def __rerank(self):
        pass
                

class MultiQueryRetriever():
    def __init(self, query):
        self.query
    
    def retrieve(self):
        pass


# retriever = SelfRetriver()
# retriever = HybridRetriever()
# docs = retriever.retrieve(query="Qual a relação bitcoin e da petrobras")
# print(len(docs))