#!/usr/bin/env python
"""
UCLA Women's Basketball RAG System Test Script
This script tests the UCLA women's basketball RAG system with a variety of query types.
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Import RAG components
from src.llm_utils import LLMManager
from src.data_loader import create_ucla_wbb_database
from src.db_connector import DatabaseConnector
from src.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_queries.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Test queries organized by category
TEST_QUERIES = {
    "basic_stats": [
        "Who scored the most points in a single game this season?",
        "What was Lauren Betts' average points per game?",
        "How many three-pointers did Kiki Rice make against Richmond?",
        "Which player had the most rebounds in the LSU game?",
        "How many assists did Gabriela Jaquez have this season?"
    ],
    "player_info": [
        "Who is player number 51?",
        "What position does Londynn Jones play?",
        "List all players who scored over 20 points in a game",
        "Which player had the highest field goal percentage?",
        "Who is the best three-point shooter on the team?"
    ],
    "game_specific": [
        "What was the team's total score against South Carolina?",
        "Did UCLA beat Rutgers?",
        "How many points did UCLA score against Maryland?",
        "Which game did Lauren Betts score her season high?",
        "What was the team's shooting percentage against LSU?"
    ],
    "aggregation": [
        "What was the team's average points per game?",
        "Who had the most total rebounds for the season?",
        "Calculate the team's overall three-point percentage",
        "Which player had the most consistent scoring across all games?",
        "What was the team's assist-to-turnover ratio?"
    ],
    "comparison": [
        "Who is better at rebounding, Lauren Betts or Angela Dugalić?",
        "Compare the scoring efficiency of Kiki Rice and Londynn Jones",
        "Which player should get more minutes, Gabriela Jaquez or Timea Gardiner?",
        "Is Lauren Betts more effective against stronger or weaker opponents?",
        "Who performs better in close games, Kiki Rice or Londynn Jones?"
    ],
    "multi_entity": [
        "How did Lauren Betts and Kiki Rice perform against South Carolina?",
        "What's the combined scoring average of Londynn Jones and Gabriela Jaquez?",
        "Compare the performances of UCLA's starters and bench players",
        "How many points did Lauren Betts, Kiki Rice, and Londynn Jones score against Rutgers?",
        "Which players improved the most from the beginning to the end of the season?"
    ]
}

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
    # Debug environment variables
    print("Checking for API key...")
    print(f"Environment variables loaded: {os.environ.keys()}")
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print(f"API key found: {bool(api_key)}")
    
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        print("Error: ANTHROPIC_API_KEY not set in .env file")
        print("Please check that your .env file contains: ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)
    
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

def process_query(pipeline, query):
    """Process a single query and return the results."""
    logger.info(f"Processing query: '{query}'")
    
    try:
        # Process query
        result = pipeline.process_query(query)
        
        return {
            "query": query,
            "answer": result.get('response', 'No response generated'),
            "sql_query": result.get('sql_query', 'No SQL query generated'),
            "entities": result.get('extracted_entities', {})
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {
            "query": query,
            "answer": f"Error: {str(e)}",
            "sql_query": "Error",
            "entities": {}
        }

def run_category_tests(category=None, output_file=None):
    """Run tests for a specific category or all categories."""
    # Initialize pipeline
    logger.info("Initializing UCLA WBB RAG pipeline...")
    pipeline = initialize_pipeline()
    
    results = []
    
    if category and category in TEST_QUERIES:
        # Run tests for specific category
        logger.info(f"Running tests for category: {category}")
        queries = TEST_QUERIES[category]
        
        for i, query in enumerate(queries, 1):
            logger.info(f"Query {i}/{len(queries)}: {query}")
            result = process_query(pipeline, query)
            results.append(result)
            print(f"\nQuery: {query}")
            print(f"Answer: {result['answer']}\n")
            
            # Add a small delay between queries
            if i < len(queries):
                time.sleep(1)
    else:
        # Run all tests
        logger.info("Running all test queries")
        all_queries = []
        for cat_queries in TEST_QUERIES.values():
            all_queries.extend(cat_queries)
        
        for i, query in enumerate(all_queries, 1):
            logger.info(f"Query {i}/{len(all_queries)}: {query}")
            result = process_query(pipeline, query)
            results.append(result)
            print(f"\nQuery: {query}")
            print(f"Answer: {result['answer']}\n")
            
            # Add a small delay between queries
            if i < len(all_queries):
                time.sleep(1)
    
    # Save results if output file specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
    
    return results

def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description='Test UCLA Women\'s Basketball RAG System')
    parser.add_argument('--category', '-c', choices=TEST_QUERIES.keys(),
                        help='Test category to run (default: run all)')
    parser.add_argument('--output', '-o', help='Output file for results (JSON format)')
    parser.add_argument('--single', '-s', help='Run a single query')
    
    args = parser.parse_args()
    
    if args.single:
        # Run a single query
        pipeline = initialize_pipeline()
        result = process_query(pipeline, args.single)
        print(f"\nQuery: {args.single}")
        print(f"Answer: {result['answer']}")
        print(f"\nSQL Query: {result['sql_query']}")
        print(f"\nExtracted Entities: {result['entities']}")
    else:
        # Run category tests
        run_category_tests(args.category, args.output)

if __name__ == "__main__":
    main()
