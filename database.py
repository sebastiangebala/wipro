import sqlite3
import time
from sqlite3 import Error

class DatabaseManager:
    """
    Manages all database operations for the instrument price modifier application.

    Attributes:
        db_file (str): Path to the SQLite database file.
        conn (sqlite3.Connection): SQLite connection object.
    """
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.multiplier_cache = {}  # Cache to store multipliers: {instrument_name: (multiplier, timestamp)}
    

    def create_connection(self):
        """Create a database connection to a SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def create_table(self, create_table_sql):
        """Create a table from the create_table_sql statement."""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_instrument_modifier(self, instrument_modifier):
        """Create a new instrument_modifier record."""
        sql = '''INSERT INTO INSTRUMENT_PRICE_MODIFIER(NAME, MULTIPLIER) VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, instrument_modifier)
        self.conn.commit()
        return cur.lastrowid

    def get_instrument_modifier(self, name):
        current_time = time.time()
        cache_entry = self.multiplier_cache.get(name)
        
        # Check if the entry exists and is less than 5 seconds old
        if cache_entry and (current_time - cache_entry[1]) < 5:
            return cache_entry[0]  # Return the cached multiplier
        
        # If not cached or cache is old, query the database and update the cache
        cur = self.conn.cursor()
        cur.execute("SELECT MULTIPLIER FROM INSTRUMENT_PRICE_MODIFIER WHERE NAME=?", (name,))
        row = cur.fetchone()
        multiplier = row[0] if row else None
        
        # Update the cache with the new value and current timestamp
        self.multiplier_cache[name] = (multiplier, current_time)
        
        return multiplier

    def init_db(self):
        """Initialize the database with the required table."""
        sql_create_table = """CREATE TABLE IF NOT EXISTS INSTRUMENT_PRICE_MODIFIER (
                              ID INTEGER PRIMARY KEY,
                              NAME TEXT NOT NULL,
                              MULTIPLIER REAL NOT NULL
                          );"""
        self.create_table(sql_create_table)
        print("Table created successfully.")

if __name__ == "__main__":
    db_manager = DatabaseManager("instrument_data.db")
    db_manager.init_db()
