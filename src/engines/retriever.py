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
        

    def retrieve(self, query):
        lexic_docs = self.__lexic_retrieval(query=query)
        semantic_docs = self.__sementic_retrieve(query=query)
        
        return lexic_docs

    def __sementic_retrieve(self, query: str) -> List[Document]:
        docs = self.vectorstore.chroma.similarity_search(query=query)
        return docs
    
    def __lexic_retrieval(self, query) -> List[Document]:
        # print(self.sqlite)
        rows = self.sqlite.query("SELECT * FROM articles")

        data = [{
            "title":        row[0],
            "author":       row[1], 
            "source":       row[2], 
            "description":  row[3], 
            "content":      row[4], 
            "url":          row[5], 
            "published_at": row[6], 
            "requested_at": row[7] 
        } for row in rows]
        
        documents = []

        for row in data:
            row_text = " ".join([f"{key}: {value}" for key, value in row.items()])
            documents.append(Document(page_content=row_text))

        retriever = BM25Retriever.from_documents(
            documents,
            k=8,
            preprocess_func=word_tokenize,
        )

        relevant_docs = retriever.invoke(query)

        return relevant_docs
    
    def __rerank(self):
        pass
                

class MultiQueryRetriever():
    def __init(self, query):
        self.query
    
    def retrieve(self):
        pass


# retriever = SelfRetriver()
retriever = HybridRetriever()
docs = retriever.retrieve(query="Qual a relação bitcoin e da petrobras")
print(len(docs))