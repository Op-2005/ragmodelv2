import sqlite3
import pandas as pd
from langchain_community.utilities import SQLDatabase

class DatabaseConnector:
    """Handles database connections and operations."""
    
    def __init__(self, db_path='data/nba_stats.db'):
        """Initialize with path to SQLite database."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.langchain_db = None
        
    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.langchain_db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
            return True
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute_query(self, query):
        """Execute SQL query and return results."""
        if not self.conn:
            self.connect()
        
        try:
            result = self.cursor.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None
    
    def get_table_schema(self, table_name="player_game_stats"):
        """Get schema for a table."""
        if not self.conn:
            self.connect()
            
        query = f"PRAGMA table_info({table_name})"
        result = self.execute_query(query)
        
        if result:
            # Format as readable schema
            schema = []
            for col in result:
                schema.append({
                    "name": col[1],
                    "type": col[2],
                    "notnull": col[3],
                    "pk": col[5]
                })
            return schema
        return None
    
    def get_distinct_values(self, column, table="player_game_stats", limit=1000):
        """Get distinct values for a column."""
        if not self.conn:
            self.connect()
            
        query = f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL LIMIT {limit}"
        result = self.execute_query(query)
        
        if result:
            return [item[0] for item in result]
        return []