from src.engines.embeddings import VectorIndex

class SelfRetriver():
    def __init__(self, query):
        self.vectorstore = VectorIndex()
        self.query = query 

    def retrieve(self):
        pass

class HybridRetriever():
    def __init(self, query):
        self.query

    def retrieve(self):
        pass 

class MultiQueryRetriever():
    def __init(self, query):
        self.query
    
    def retrieve(self):
        pass