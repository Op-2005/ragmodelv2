import os
import logging
import argparse
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
        logging.FileHandler('rag_system.log'),
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
    table_name = "ucla_player_stats"
    
    # Initialize LLM
    llm_manager = LLMManager(model_name=model_name)
    
    # Initialize database connector
    db_connector = DatabaseConnector(db_path)
    
    # Initialize RAG pipeline with dataset info
    rag_pipeline = RAGPipeline(llm_manager, db_connector, table_name=table_name, dataset_type="ucla")
    
    return rag_pipeline

def interactive_mode(pipeline):
    """Run in interactive command-line mode."""
    print("\n" + "="*50)
    print("UCLA WOMEN'S BASKETBALL Statistics RAG System")
    print("Type 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        # Get user query
        user_input = input("Enter your question: ")
        
        # Check for exit command
        if user_input.lower() in ('exit', 'quit'):
            break
        
        # Process query
        print("Processing query...")
        result = pipeline.process_query(user_input)
        
        # Display response
        print("\nAnswer:")
        print(result['response'])
        
        # Display details if available
        if 'sql_query' in result:
            print("\nSQL Query:")
            print(result['sql_query'])
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Run UCLA Women\'s Basketball Statistics RAG System')
    parser.add_argument('--model', type=str, default='claude-3-5-sonnet-20241022',
                        help='LLM model to use (default: claude-3-5-sonnet-20241022)')
    
    args = parser.parse_args()
    
    # Initialize pipeline with selected model
    pipeline = initialize_pipeline(model_name=args.model)
    
    # Run in interactive mode
    interactive_mode(pipeline)