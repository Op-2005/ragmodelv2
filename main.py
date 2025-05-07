import os
import logging
from src.llm_utils import LLMManager
from src.data_loader import load_csv_to_dataframe, create_sqlite_database
from src.db_connector import DatabaseConnector
from src.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nba_rag.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_database():
    """Set up database if it doesn't exist."""
    db_path = 'data/nba_stats.db'
    
    # Check if database already exists
    if not os.path.exists(db_path):
        logger.info("Database not found. Creating new database...")
        
        # Load CSV data
        csv_path = 'data/nba_stats.csv'
        df = load_csv_to_dataframe(csv_path)
        
        # Create database
        create_sqlite_database(df, db_path)
    else:
        logger.info(f"Using existing database at {db_path}")
    
    return db_path

def initialize_pipeline(model_name="claude-3-5-sonnet-20241022"):
    """Initialize the RAG pipeline."""
    # Set up database
    db_path = setup_database()
    
    # Initialize LLM
    llm_manager = LLMManager(model_name=model_name)
    
    # Initialize database connector
    db_connector = DatabaseConnector(db_path)
    
    # Initialize RAG pipeline
    rag_pipeline = RAGPipeline(llm_manager, db_connector)
    
    return rag_pipeline

def interactive_mode(pipeline):
    """Run in interactive command-line mode."""
    print("NBA Statistics RAG System")
    print("Type 'exit' to quit\n")
    
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
    # Initialize pipeline with model name
    model_name = "claude-3-5-sonnet-20241022"  # Use Anthropic Claude model
    
    print(f"Initializing RAG pipeline with {model_name}...")
    pipeline = initialize_pipeline(model_name)
    
    # Run in interactive mode
    interactive_mode(pipeline)