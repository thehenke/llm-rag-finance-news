import sqlite3

class SQLite:
    def __init__(self):
        self.con = sqlite3.connect("src/database/articles.db")
        self.ddl = open('src/database/create_articles.sql', 'r').read()

    def __create_table(self):
        try: 
            if self.ddl:
                self.con.execute(self.ddl)
        except Exception as error:
            print(f"Erro ao tentar criar tabela: {error}")

    def insert_rows(self, rows):
        try:
            self.__create_table()
            self.con.executemany("INSERT INTO articles(title, author, source, description, content, url, published_at, request_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", rows)
            self.con.commit()
            print(f'[INFO] - {len(rows)} linhas inseridas na tabela!')
        except Exception as error:
            print(f"Erro ao tentar inserir dados {error}")

    def query(self, query):
        try: 
            res = self.con.cursor().execute(query)
            return res.fetchall()
        except Exception as error: 
            print(f"Erro ao tentar executar a query: {error}")
            return None