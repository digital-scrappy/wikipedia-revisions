import sqlite3
import json

def write_occupation_to_db(occupation, content, sucess, cursor: sqlite3.Cursor, con, table):

    value = (occupation, json.dumps(content), '', sucess, 0)
    cursor.execute(f"INSERT INTO {table} Values (NULL, ?,?,?,?,?)", value)
    con.commit()

