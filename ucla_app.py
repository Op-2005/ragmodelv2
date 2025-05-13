#!/usr/bin/env python
import os
import logging
from src.llm_utils import LLMManager
from src.data_loader import load_ucla_wbb_to_dataframe, create_sqlite_database
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
        logging.FileHandler('ucla_wbb_rag.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_database():
    """Set up database if it doesn't exist."""
    db_path = 'data/ucla_wbb.db'
    
    # Check if database already exists
    if not os.path.exists(db_path):
        logger.info("Database not found. Creating new database...")
        
        # Load CSV data
        csv_path = 'data/uclawbb_season.csv'
        df = load_ucla_wbb_to_dataframe(csv_path)
        
        # Create database
        create_sqlite_database(df, db_path=db_path, table_name='ucla_player_stats')
    else:
        logger.info(f"Using existing database at {db_path}")
    
    return db_path

class UCLAEntityExtractor:
    """Custom entity extractor for UCLA women's basketball data."""
    
    def __init__(self, db_connector, llm_manager):
        """Initialize with database connector and LLM manager."""
        self.db = db_connector
        self.llm = llm_manager
        self.entity_cache = {}  # Cache for entity resolution results
        
        # Pre-load common entities for faster matching
        self._load_common_entities()
    
    def _load_common_entities(self):
        """Load common entities like player names and opponents from database."""
        # Connect to database if not already connected
        if self.db.conn is None:
            self.db.connect()
            
        # Load players
        self.players = self.db.get_distinct_values("Name", table="ucla_player_stats")
        
        # Load player numbers
        self.player_numbers = self.db.get_distinct_values("No", table="ucla_player_stats")
        
        # Load opponents
        self.opponents = self.db.get_distinct_values("Opponent", table="ucla_player_stats")
    
    def extract_entities(self, query):
        """Extract entities from query using LLM."""
        # Create prompt template for UCLA WBB data
        prompt = f"""
        Extract entities from this UCLA women's basketball statistics query.
        Return a JSON object with these fields:
        - player_name: Full name of player mentioned (if any)
        - player_number: Jersey number mentioned (if any)
        - opponent: Opponent team mentioned (if any)
        - statistic: Specific statistic mentioned (points, rebounds, assists, etc.)
        - comparison: Any comparison operators (>, <, =, etc.)
        - value: Any numeric value mentioned for comparison
        
        Query: {query}
        
        JSON output:
        """
        
        # Generate extraction using LLM
        result = self.llm.generate_text(prompt)
        
        # Parse the JSON from the response
        try:
            # Find the JSON part in the response
            import re
            import json
            json_match = re.search(r'({.*})', result, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                entities = json.loads(json_str)
            else:
                # Fallback to empty entities
                entities = {
                    "player_name": None,
                    "player_number": None,
                    "opponent": None,
                    "statistic": None,
                    "comparison": None,
                    "value": None
                }
        except Exception as e:
            logger.error(f"Error parsing JSON from LLM: {str(e)}")
            # Fallback to empty entities
            entities = {
                "player_name": None,
                "player_number": None,
                "opponent": None,
                "statistic": None,
                "comparison": None,
                "value": None
            }
        
        # Resolve and validate entities
        return self._resolve_entities(entities)
    
    def _resolve_entities(self, entities):
        """Resolve extracted entities to database entries using fuzzy matching."""
        from thefuzz import process
        
        resolved = entities.copy()
        
        # Resolve player name
        if entities.get("player_name"):
            player_match = self._fuzzy_match(entities["player_name"], self.players)
            if player_match:
                resolved["player_name"] = player_match
        
        # Resolve player number
        if entities.get("player_number"):
            # Convert to string for matching
            player_num = str(entities["player_number"])
            if player_num in self.player_numbers:
                resolved["player_number"] = player_num
        
        # Resolve opponent
        if entities.get("opponent"):
            opponent_match = self._fuzzy_match(entities["opponent"], self.opponents)
            if opponent_match:
                resolved["opponent"] = opponent_match
        
        return resolved
    
    def _fuzzy_match(self, query, options, threshold=70):
        """Find the best match for a query in a list of options."""
        if not query or not options:
            return None
            
        # Check cache first
        cache_key = f"{query}:{','.join(str(opt) for opt in options[:5])}"
        if cache_key in self.entity_cache:
            return self.entity_cache[cache_key]
        
        # Find best match
        match, score = process.extractOne(query, options)
        
        # Only accept match if score is above threshold
        if score >= threshold:
            self.entity_cache[cache_key] = match
            return match
        
        return None

class UCLASQLQueryGenerator:
    """Generate SQL queries for UCLA women's basketball data."""
    
    def __init__(self, llm_manager, db_connector):
        """Initialize with LLM manager and database connector."""
        self.llm = llm_manager
        self.db = db_connector
        
        # Get database schema
        self.table_schema = self.db.get_table_schema(table_name="ucla_player_stats")
    
    def generate_sql_query(self, user_query, extracted_entities=None):
        """Generate SQL query from user query and extracted entities."""
        # Format table schema for prompt
        schema_str = self._format_schema_for_prompt()
        
        # Format entities for prompt
        entities_str = "None" if not extracted_entities else str(extracted_entities)
        
        # Create prompt for SQL generation
        prompt = f"""
        You are an expert SQL query generator for a UCLA women's basketball statistics database.
        
        Given a natural language query, generate a valid SQL query to answer the question.
        
        Database schema:
        {schema_str}
        
        Extracted entities:
        {entities_str}
        
        User question: {user_query}
        
        Generate only the SQL query with no other text. Make sure the query is valid SQL and uses only columns that exist in the schema.
        
        SQL query:
        """
        
        # Generate SQL query
        sql_query = self.llm.generate_text(prompt)
        
        # Extract just the SQL query (remove any explanations)
        sql_query = self._extract_sql_from_response(sql_query)
        
        return sql_query
    
    def _format_schema_for_prompt(self):
        """Format database schema for LLM prompt."""
        if not self.table_schema:
            return "Table: ucla_player_stats (schema not available)"
        
        schema_lines = ["Table: ucla_player_stats"]
        for col in self.table_schema:
            schema_lines.append(f"- {col['name']} ({col['type']})")
        
        return "\n".join(schema_lines)
    
    def _extract_sql_from_response(self, response):
        """Extract SQL query from LLM response."""
        import re
        
        # Try to find SQL between triple backticks
        sql_match = re.search(r'```sql\s*(.*?)\s*```', response, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()
        
        # Try to find SQL between regular backticks
        sql_match = re.search(r'`(.*?)`', response, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()
        
        # Otherwise, just use the whole response
        return response.strip()

class UCLARAGPipeline:
    """RAG pipeline for UCLA women's basketball data."""
    
    def __init__(self, llm_manager, db_connector):
        """Initialize pipeline with LLM manager and database connector."""
        self.llm = llm_manager
        self.db = db_connector
        
        # Initialize components
        self.entity_extractor = UCLAEntityExtractor(self.db, self.llm)
        self.query_generator = UCLASQLQueryGenerator(self.llm, self.db)
    
    def process_query(self, user_query):
        """Process a natural language query and return response."""
        try:
            # Step 1: Extract entities from query
            extracted_entities = self.entity_extractor.extract_entities(user_query)
            
            # Step 2: Generate SQL query
            sql_query = self.query_generator.generate_sql_query(user_query, extracted_entities)
            
            # Step 3: Execute SQL query
            if self.db.conn is None:
                self.db.connect()
            
            query_results = self.db.execute_query(sql_query)
            
            # Step 4: Generate natural language response
            response = self._generate_response(user_query, sql_query, query_results)
            
            return {
                "user_query": user_query,
                "extracted_entities": extracted_entities,
                "sql_query": sql_query,
                "query_results": query_results,
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "user_query": user_query,
                "error": str(e),
                "response": f"Sorry, I encountered an error processing your query: {str(e)}"
            }
    
    def _generate_response(self, user_query, sql_query, query_results):
        """Generate natural language response from query results."""
        # Create prompt for response generation
        prompt = f"""
        Based on the following information, provide a natural language answer to the user's question about UCLA women's basketball.
        
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query results: {query_results}
        
        Provide a concise, clear answer that directly addresses the user's question based on the data.
        Format any statistics in a readable way and provide context about the players and games if relevant.
        """
        
        response = self.llm.generate_text(prompt)
        return response

def initialize_pipeline(model_name="claude-3-5-sonnet-20241022"):
    """Initialize the RAG pipeline for UCLA women's basketball data."""
    # Set up database
    db_path = setup_database()
    
    # Initialize LLM
    llm_manager = LLMManager(model_name=model_name)
    
    # Initialize database connector
    db_connector = DatabaseConnector(db_path)
    
    # Initialize RAG pipeline
    rag_pipeline = UCLARAGPipeline(llm_manager, db_connector)
    
    return rag_pipeline

def interactive_mode(pipeline):
    """Run in interactive command-line mode."""
    print("\n" + "="*50)
    print("UCLA Women's Basketball Statistics RAG System")
    print("Type 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        # Get user query
        user_input = input("Enter your question: ")
        
        # Check for exit command
        if user_input.lower() in ('exit', 'quit'):
            break
        
        # Process query
        print("\nProcessing query...")
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
    
    print(f"Initializing UCLA WBB RAG pipeline with {model_name}...")
    pipeline = initialize_pipeline(model_name)
    
    # Run in interactive mode
    interactive_mode(pipeline)
