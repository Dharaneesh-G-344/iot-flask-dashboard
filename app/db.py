import sqlite3

DB_name = "iot_data.db"

def get_connections():
    connect = sqlite3.connect(DB_name)
    connect.row_factory = sqlite3.Row
    return connect

def init_db():
    connect = get_connections()
    connect.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    humidity REAL,
                    received_at TEXT)
                    """)
    connect.commit()
    connect.close()