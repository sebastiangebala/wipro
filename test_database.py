import unittest
from unittest.mock import patch
from database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Setup an in-memory database for testing."""
        self.db_manager = DatabaseManager(":memory:")
        self.db_manager.init_db()  # Initialize the database schema for tests

    def test_insert_instrument_modifier(self):
        """Test inserting an instrument modifier into the database."""
        instrument_name = "TEST_INSTRUMENT"
        multiplier = 1.5
        self.db_manager.insert_instrument_modifier((instrument_name, multiplier))
        
        # Directly fetch from database to verify insertion
        cur = self.db_manager.conn.cursor()
        cur.execute("SELECT MULTIPLIER FROM INSTRUMENT_PRICE_MODIFIER WHERE NAME=?", (instrument_name,))
        fetched_multiplier = cur.fetchone()[0]
        
        self.assertEqual(multiplier, fetched_multiplier)

    def test_get_instrument_modifier_with_caching(self):
        """Test getting an instrument modifier with caching mechanism."""
        instrument_name = "CACHED_INSTRUMENT"
        multiplier = 1.25
        # Insert directly to database to simulate existing entry
        self.db_manager.insert_instrument_modifier((instrument_name, multiplier))
        
        # First retrieval should cache the multiplier
        retrieved_multiplier = self.db_manager.get_instrument_modifier(instrument_name)
        self.assertEqual(multiplier, retrieved_multiplier)
        
        # Update the database outside of the cache to simulate change
        new_multiplier = 1.75
        cur = self.db_manager.conn.cursor()
        cur.execute("UPDATE INSTRUMENT_PRICE_MODIFIER SET MULTIPLIER=? WHERE NAME=?", (new_multiplier, instrument_name))
        self.db_manager.conn.commit()

        # Ensure the cached value is returned instead of the updated database value
        cached_multiplier = self.db_manager.get_instrument_modifier(instrument_name)
        self.assertEqual(multiplier, cached_multiplier)

    def test_create_table(self):
        """Test the creation of the table."""
        # This test ensures the table exists by attempting to insert a record
        try:
            self.db_manager.create_table("""CREATE TABLE IF NOT EXISTS TEMP_TABLE (ID INTEGER PRIMARY KEY);""")
            self.db_manager.conn.execute("INSERT INTO TEMP_TABLE (ID) VALUES (1);")
        except Exception as e:
            self.fail(f"Table creation failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
