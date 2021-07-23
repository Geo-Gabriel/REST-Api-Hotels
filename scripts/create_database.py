import sqlite3

conn = sqlite3.connect('hotels.db')
cursor = conn.cursor()

def execute_sql_command(connection, cursor, query: str):
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        raise(e)


query_hoteis_table = """CREATE TABLE IF NOT EXISTS hoteis (
    hotel_id text PRIMARY KEY,
    name text,
    stars real,
    daily real,
    location text)"""

insert_hotel_query = """INSERT INTO hoteis values ('alpha', 'Alpha Hotel', 4.3, 456.43, 'Mumbai')"""

# execute_sql_command(connection=conn, cursor=cursor, query=query_hoteis_table)
execute_sql_command(connection=conn, cursor=cursor, query=insert_hotel_query)
