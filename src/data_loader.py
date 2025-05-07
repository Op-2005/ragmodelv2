import pandas as pd
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

def load_csv_to_dataframe(file_path):
    """Load CSV file to pandas DataFrame."""
    logger.info(f"Loading CSV from {file_path}")
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Handle unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    
    logger.info(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    return df

def create_sqlite_database(df, db_path='data/nba_stats.db', table_name='player_game_stats'):
    """Create SQLite database from DataFrame."""
    logger.info(f"Creating SQLite database at {db_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Write DataFrame to SQLite
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Create indices for faster querying
    cursor = conn.cursor()
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_player_id ON {table_name} (personId)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_player_name ON {table_name} (personName)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_team ON {table_name} (teamName)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_game ON {table_name} (gameId)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_opponent ON {table_name} (opponent)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_date ON {table_name} (game_date)")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    logger.info(f"Database created successfully with table '{table_name}'")
    return db_path