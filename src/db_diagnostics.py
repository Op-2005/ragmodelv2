import sqlite3
import sys
import pandas as pd

DB_PATH = '../data/ucla_wbb.db'


def print_table_names(conn):
    print('--- TABLES ---')
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    for t in tables:
        print(t[0])
    print()

def print_table_schema(conn, table):
    print(f'--- SCHEMA FOR {table} ---')
    schema = conn.execute(f'PRAGMA table_info({table})').fetchall()
    for col in schema:
        print(f'{col[1]} ({col[2]})')
    print()

def print_sample_data(conn, table, n=5):
    print(f'--- SAMPLE DATA FROM {table} ---')
    df = pd.read_sql_query(f'SELECT * FROM {table} LIMIT {n}', conn)
    print(df)
    print()

def run_query(conn, query):
    print(f'--- QUERY: {query} ---')
    try:
        df = pd.read_sql_query(query, conn)
        print(df)
    except Exception as e:
        print(f'Error: {e}')
    print()

def main():
    conn = sqlite3.connect(DB_PATH)
    print_table_names(conn)
    tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    for table in tables:
        print_table_schema(conn, table)
        print_sample_data(conn, table)
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        run_query(conn, query)
    conn.close()

if __name__ == '__main__':
    main() 