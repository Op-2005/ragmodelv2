#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from db_connector import DatabaseConnector
from llm_utils import LLMManager
from rag_pipeline import RAGPipeline

# Initialize components
db = DatabaseConnector(db_path='../data/ucla_wbb.db')
db.connect()
llm_manager = LLMManager(model_name="claude-3-5-sonnet-20241022")
rag_pipeline = RAGPipeline(llm_manager, db)

# Test a few queries with full pipeline
test_queries = [
    "Who scored the most points in a single game this season?",
    "What was Lauren Betts' average points per game?",
    "How many three-pointers did Kiki Rice make against Richmond?",
    "Who is the best three-point shooter on the team?"
]

print("=== FULL RAG PIPELINE TEST ===")
print("Showing natural language responses (not just SQL results)\n")

for i, query in enumerate(test_queries, 1):
    print(f"{i}. USER: {query}")
    print("-" * 60)
    
    result = rag_pipeline.process_query(query)
    
    if result['success']:
        print(f"BOT: {result['response']}")
        print(f"\n(Generated SQL: {result['sql_query'].replace(chr(10), ' ').strip()})")
        print(f"(Raw results: {result['query_results']})")
    else:
        print(f"ERROR: {result['error_message']}")
    
    print("\n" + "="*80 + "\n")

db.close() 