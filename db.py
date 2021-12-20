import sqlite3
import pandas as pd
from config import config

class ArticleDb():

    def __init__(self, db_name):
        self.db_name = db_name
        self.create()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create(self):
        with self.connect() as conn:
            create_sql = """
            create table if not exists articles (article_content text not null,topic text not null);
            """
            conn.execute(create_sql)

    def insert(self, content, topic):
        with self.connect() as conn:
            cursor = conn.cursor()
            insert_sql = """
            insert into articles (article_content, topic) values (?, ?)
            """
            cursor.execute(insert_sql, (content, topic))

    def read(self):
        with self.connect() as conn:
            df = pd.read_sql_query("select * from articles", conn)
        return df

    def drop(self, table:str = 'articles'):
        with self.connect() as conn:
            conn.execute("DROP TABLE if exists {}.{}".format(self.db_name, table))
        print("Dropped table {}".format(table))



db = ArticleDb(config.database)