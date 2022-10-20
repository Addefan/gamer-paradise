import psycopg2
import psycopg2.extras

from config import Config


def create_database(script_path):
    db = Database()
    with open(script_path, encoding='utf-8') as file:
        db.create(file.read())


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASS,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT
        )
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def select(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if len(data) == 1:
            data = data[0]
        return data

    def insert(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()


if __name__ == "__main__":
    create_database('database.sql')
