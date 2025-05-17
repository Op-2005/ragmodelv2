import pandas as pd
import sqlite3
import os
import logging
import re

logger = logging.getLogger(__name__)

def load_ucla_wbb_to_dataframe(file_path):
    """Load UCLA Women's Basketball CSV file to pandas DataFrame with specific processing."""
    logger.info(f"Loading UCLA WBB data from {file_path}")
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Handle unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    
    # Process player names - remove quotes and commas
    if 'Name' in df.columns:
        df['Name'] = df['Name'].str.replace('"', '').str.strip()
        # Split name into first and last name
        df['first_name'] = df['Name'].apply(lambda x: x.split(',')[1].strip() if ',' in str(x) else '')
        df['last_name'] = df['Name'].apply(lambda x: x.split(',')[0].strip() if ',' in str(x) else x)
    
    # Process shooting stats to extract made and attempted values
    shooting_cols = ['FG', '3PT', 'FT']
    for col in shooting_cols:
        if col in df.columns:
            # These columns already exist as separate FGM, FGA, etc.
            continue
    
    logger.info(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    return df

def create_sqlite_database(df, db_path='data/ucla_wbb.db', table_name='ucla_player_stats'):
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
    
    # Create indices for UCLA women's basketball data
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_player_name ON {table_name} (Name)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_player_number ON {table_name} (No)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_opponent ON {table_name} (Opponent)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_date ON {table_name} (game_date)")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    logger.info(f"Database created successfully with table '{table_name}'")
    return db_path

def create_ucla_wbb_database(csv_path, db_path='data/ucla_wbb.db'):
    """Create SQLite database for UCLA women's basketball data."""
    # Load the CSV data
    df = load_ucla_wbb_to_dataframe(csv_path)
    
    # Create the database
    return create_sqlite_database(df, db_path=db_path, table_name='ucla_player_stats')