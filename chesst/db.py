import os
import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(current_dir, 'database')

    db_init_files = sorted(os.listdir(db_dir))

    for filename in db_init_files:
        file_path = os.path.join(db_dir, filename)
        execute_sql_script(db, file_path)


def execute_sql_script(db, path):
    if not os.path.isfile(path):
        click.echo('File: ' + path + ' cannot be found.')
        return

    with current_app.open_resource(path) as f:
        db.executescript(f.read().decode('utf8'))
        click.echo('File: ' + path + ' executed.')


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
