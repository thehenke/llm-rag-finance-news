import os 
import json 
import requests
from datetime import datetime

from src.database.management import DatabaseManager

with open('env.json', 'r') as env:
    env = json.load(env)

API_KEY = env["API_NEWS_KEY"]



# keys = ["bitcoin"]

# response = requests.get(f'https://newsapi.org/v2/everything?q={",".join(keys)}&apiKey={API_KEY}')

# articles = response.json()['articles']

# data = [
#     {
#         "title": article["title"],
#         "author": article["author"],
#         "source": article["source"],
#         "description": article["description"],
#         "content": article["content"],
#         "url": article["url"],
#         "published_at": article["publishedAt"],
#         "request_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     } for article in articles
# ]

# print(len(data))

