import os
import pytest
import psycopg2
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'), 
    'user': os.environ.get('DB_USER'), 
    'password': os.environ.get('DB_PASSWORD'), 
    'host': os.environ.get('DB_HOST'), 
    'port': os.environ.get('DB_PORT'),
}

database_names = [
    'film_work',
    'genre',
    'genre_film_work',
    'person_film_work',
    'person',
]


def fetch_pg_table_row_numbers(pg_conn: _connection, table_name: str):
    conn = pg_conn
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM content.{0};'.format(table_name))
    return cursor.fetchone()[0] 


def fetch_sql_table_row_numbers(sqlite_conn: sqlite3.Connection, table_name: str):
    conn = sqlite_conn
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM {0};'.format(table_name))
    return cursor.fetchone()[0]


def if_raws_equal(pg_conn: _connection, sqlite_conn: sqlite3.Connection, table_name: str):
    conn_postgres = pg_conn
    cursor_postgres = conn_postgres.cursor()
    cursor_postgres.execute('SELECT * FROM content.{0} ORDER BY id;'.format(table_name))
    res_postgres = cursor_postgres.fetchall()

    conn_sqlite = sqlite_conn
    conn_sqlite.row_factory = sqlite3.Row
    cursor_sqlite = conn_sqlite.cursor()
    cursor_sqlite.execute('SELECT * FROM {0} ORDER BY id;'.format(table_name))
    res_sql = cursor_sqlite.fetchall()

    for i in range(len(res_sql)):
        sql_raw = dict(res_sql[i])
        pg_raw = dict(res_postgres[i])
        for k in sql_raw.keys():
            if k == 'created_at':
                datetime_object_sql = sql_raw[k].split('.')[0] 
                assert datetime_object_sql == pg_raw['created'].strftime('%Y-%m-%d %H:%M:%S')
                continue
            if k == 'updated_at':
                datetime_object_sql = sql_raw[k].split('.')[0] 
                assert datetime_object_sql == pg_raw['modified'].strftime('%Y-%m-%d %H:%M:%S')
                continue
            assert sql_raw.get(k) == pg_raw.get(k)


@pytest.mark.parametrize('database_name', database_names)
def test_inserted_numbers(database_name):
    with sqlite3.connect('../db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        assert fetch_pg_table_row_numbers(pg_conn, database_name) == fetch_sql_table_row_numbers(sqlite_conn, database_name)


@pytest.mark.parametrize('database_name', database_names)
def test_equal_raws(database_name):
    with sqlite3.connect('../db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        if_raws_equal(pg_conn, sqlite_conn, database_name)
