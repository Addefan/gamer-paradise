import click

from database import db


@click.command()
def create_db():
    db.create_all()


@click.command()
def drop_db():
    if click.confirm('Вы действительно хотите удалить базу данных со всеми её данными?', abort=True):
        db.drop_all()
