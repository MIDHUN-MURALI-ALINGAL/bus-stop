from database import db

cursor = db.cursor
conn = db.conn


def create_bus_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bus_name TEXT,

        bus_number TEXT,

        owner TEXT,

        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bus_id INTEGER,

        source TEXT,

        destination TEXT,

        fare INTEGER,

        travel_time TEXT
    )
    """)

    conn.commit()


create_bus_tables()