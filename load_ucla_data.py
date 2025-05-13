#!/usr/bin/env python
import os
import logging
from src.data_loader import create_ucla_wbb_database

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Get the absolute path to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    csv_path = os.path.join(project_dir, 'data', 'uclawbb_season.csv')
    db_path = os.path.join(project_dir, 'data', 'ucla_wbb.db')
    
    # Create the database
    logger.info(f"Creating UCLA WBB database from {csv_path}")
    db_path = create_ucla_wbb_database(csv_path, db_path)
    logger.info(f"Database created at {db_path}")
    
    # Print success message
    logger.info("UCLA Women's Basketball data loaded successfully!")

if __name__ == "__main__":
    main()
