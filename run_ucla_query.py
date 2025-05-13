#!/usr/bin/env python
import os
import sys
import logging
from src.llm_utils import LLMManager
from src.data_loader import create_ucla_wbb_database
from src.db_connector import DatabaseConnector
from src.rag_pipeline import RAGPipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ucla_query.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_ucla_database():
    """Set up UCLA women's basketball database if it doesn't exist."""
    db_path = 'data/ucla_wbb.db'
    
    # Check if database already exists
    if not os.path.exists(db_path):
        logger.info("UCLA WBB database not found. Creating new database...")
        
        # Load CSV data
        csv_path = 'data/uclawbb_season.csv'
        db_path = create_ucla_wbb_database(csv_path, db_path)
    else:
        logger.info(f"Using existing UCLA WBB database at {db_path}")
    
    return db_path

def initialize_pipeline(model_name="claude-3-5-sonnet-20241022"):
    """Initialize the RAG pipeline for UCLA women's basketball data."""
    # Set up database
    db_path = setup_ucla_database()
    
    # Initialize LLM
    llm_manager = LLMManager(model_name=model_name)
    
    # Initialize database connector
    db_connector = DatabaseConnector(db_path)
    
    # Initialize RAG pipeline with dataset info
    rag_pipeline = RAGPipeline(
        llm_manager, 
        db_connector, 
        table_name="ucla_player_stats", 
        dataset_type="ucla"
    )
    
    return rag_pipeline

def process_query(query):
    """Process a single query and print the results."""
    # Initialize pipeline
    print(f"Initializing UCLA WBB RAG pipeline...")
    pipeline = initialize_pipeline()
    
    # Process query
    print(f"\nProcessing query: '{query}'")
    
    # Modify the query to exclude the 'Totals' row
    if "most" in query.lower() and "points" in query.lower():
        # Add a hint to exclude the Totals row
        query = query + " (exclude team totals)"
    
    result = pipeline.process_query(query)
    
    # Display response
    print("\nAnswer:")
    print(result['response'])
    
    # Display details if available
    if 'sql_query' in result:
        print("\nSQL Query:")
        print(result['sql_query'])
    
    if 'extracted_entities' in result:
        print("\nExtracted Entities:")
        print(result['extracted_entities'])
    
    return result

if __name__ == "__main__":
    # Get query from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python run_ucla_query.py 'your question about UCLA women's basketball'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    process_query(query)
