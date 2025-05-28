import sqlite3
import pandas as pd
import logging
from langchain_community.utilities import SQLDatabase

logger = logging.getLogger(__name__)

class DatabaseConnector:
    """Handles database connections and operations for UCLA women's basketball data."""
    
    def __init__(self, db_path='data/ucla_wbb.db'):
        """Initialize with path to SQLite database (default: ucla_wbb.db)."""
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
            logger.info(f"Connected to database at {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            logger.info("Database connection closed")
    
    def execute_query(self, query, return_error=False):
        """Execute SQL query and return results. If return_error=True, return (results, error_message)."""
        if not self.conn:
            self.connect()
        try:
            logger.debug(f"Executing query: {query}")
            result = self.cursor.execute(query)
            data = result.fetchall()
            if return_error:
                return data, None
            return data
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}\nQuery: {query}")
            if return_error:
                return None, str(e)
            return None
    
    def get_table_schema(self, table_name="ucla_player_stats"):
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
            logger.info(f"Retrieved schema for table '{table_name}' with {len(schema)} columns")
            return schema
        logger.warning(f"Could not retrieve schema for table '{table_name}'")
        return None
    
    def get_distinct_values(self, column, table="ucla_player_stats", limit=1000):
        """Get distinct values for a column."""
        if not self.conn:
            self.connect()
            
        query = f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL LIMIT {limit}"
        result = self.execute_query(query)
        
        if result:
            values = [item[0] for item in result]
            logger.debug(f"Retrieved {len(values)} distinct values for '{column}' in table '{table}'")
            return values
        logger.warning(f"No distinct values found for '{column}' in table '{table}'")
        return []
    
    def get_table_names(self):
        """Get all table names in the database."""
        if not self.conn:
            self.connect()
            
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = self.execute_query(query)
        
        if result:
            tables = [item[0] for item in result]
            logger.info(f"Database contains {len(tables)} tables: {', '.join(tables)}")
            return tables
        return []
    
    def get_row_count(self, table_name):
        """Get the number of rows in a table."""
        if not self.conn:
            self.connect()
            
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        
        if result and result[0]:
            count = result[0][0]
            logger.info(f"Table '{table_name}' contains {count} rows")
            return count
        return 0