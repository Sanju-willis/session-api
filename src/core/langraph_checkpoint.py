# src\core\langraph_checkpoint.py
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

def open_langraph_sqlite(path: str):
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn, SqliteSaver(conn)

def close_langraph_sqlite(conn):
    conn.close()
