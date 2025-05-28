import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from db_connector import DatabaseConnector
from query_generator import SQLQueryGenerator
from entity_extractor import EntityExtractor
from llm_utils import LLMManager

# Setup logging
logging.basicConfig(filename='ucla_regression_results.log', level=logging.INFO)

# Load queries
with open('queries_to_rerun.txt', 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

db = DatabaseConnector(db_path='../data/ucla_wbb.db')
db.connect()
llm_manager = LLMManager(model_name="claude-3-5-sonnet-20241022")
entity_extractor = EntityExtractor(db, llm_manager)
query_generator = SQLQueryGenerator(llm_manager, db)

results = []
for user_query in queries:
    try:
        entities = entity_extractor.extract_entities(user_query)
        sql = query_generator.generate_sql_query(user_query, entities)
        valid, err = query_generator.validate_sql(sql)
        if not valid:
            logging.error(f'Query: {user_query}\nSQL: {sql}\nError: {err}')
            results.append({'query': user_query, 'sql': sql, 'error': err, 'results': None})
            continue
        data, sql_error = db.execute_query(sql, return_error=True)
        if sql_error:
            logging.error(f'Query: {user_query}\nSQL: {sql}\nSQL Error: {sql_error}')
            results.append({'query': user_query, 'sql': sql, 'error': sql_error, 'results': None})
        else:
            logging.info(f'Query: {user_query}\nSQL: {sql}\nResults: {data}')
            results.append({'query': user_query, 'sql': sql, 'error': None, 'results': data})
    except Exception as e:
        logging.error(f'Query: {user_query}\nException: {e}')
        results.append({'query': user_query, 'sql': None, 'error': str(e), 'results': None})

db.close()

# Save results as a summary
import json
with open('ucla_regression_results.json', 'w') as f:
    json.dump(results, f, indent=2) 