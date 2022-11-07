import click
import psycopg2
import psycopg2.extras
from flask import g

from config import Config


def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.cursor.close()
        db.connection.close()


def init_db(script_path):
    db = get_db()
    with open(script_path, encoding='utf-8') as file:
        db.create(file.read())


@click.command('init-db')
def init_db_command(script_path='database.sql'):
    init_db(script_path)
    click.echo('База данных инициализирована')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def db_dict_to_list(column_name, data):
    return [row[column_name] for row in data]


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

    def select(self, query, values=None):
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        if len(data) == 1:
            data = data[0]
        return data

    def insert(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    delete = insert
    update = insert
