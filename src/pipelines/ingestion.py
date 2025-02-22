import os 
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain.docstore.document import Document
from src.engines.sqlite import SQLite
from src.engines.embeddings import VectorIndex

load_dotenv()
API_KEY = os.getenv('API_NEWS_KEY')

class DataIngestion():
    def __init__(self):
        self.api_words_search = ["bitcoin"]
        self.len_data = None
        self.db = SQLite()
    
    def run(self, get_data_from_api=False):
        if get_data_from_api:
            self.__get_data_from_api()
        
        self.__create_vector_index()

    def __get_data_from_api(self):
        print(f"[INFO] - Buscando dados na API...")
        self.response = requests.get(f'https://newsapi.org/v2/everything?q={",".join(self.api_words_search)}&apiKey={API_KEY}&language=pt&sortBy=popularity')
        articles = self.response.json()['articles']

        data = [
            (
                str(article["title"]),
                str(article["author"]),
                str(article["source"]),
                str(article["description"]),
                str(article["content"]),
                str(article["url"]),
                str(article["publishedAt"]),
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ) for article in articles
        ]
    
        if len(data) > 0:
            self.db.insert_rows(data)

    
    def __create_vector_index(self):
        rows = self.db.query("SELECT * FROM articles")

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
            # Criar uma string no formato "coluna: valor"
            row_text = " ".join([f"{key}: {value}" for key, value in row.items()])
            # print(len(row_text))
            documents.append(Document(page_content=row_text))
            
        print(f"[INFO] - {len(documents)} recuperados")
        vs = VectorIndex()
        vs.store(documents)


# DataIngestion().run(get_data_from_api=True)