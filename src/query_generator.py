from langchain_core.prompts import PromptTemplate
import re

class SQLQueryGenerator:
    """Generate SQL queries from natural language using LLM."""
    
    def __init__(self, llm_manager, db_connector):
        """Initialize with LLM manager and database connector."""
        self.llm = llm_manager
        self.db = db_connector
        
        # Get database schema
        self.table_schema = self.db.get_table_schema()
    
    def generate_sql_query(self, user_query, extracted_entities=None):
        """Generate SQL query from user query and extracted entities."""
        # Format table schema for prompt
        schema_str = self._format_schema_for_prompt()
        
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["query", "schema", "entities"],
            template="""
            You are an expert SQL query generator for an NBA statistics database.
            
            Given a natural language query, generate a valid SQL query to answer the question.
            
            Database schema:
            {schema}
            
            Extracted entities:
            {entities}
            
            User question: {query}
            
            Generate only the SQL query with no other text. Make sure the query is valid SQL and uses only columns that exist in the schema.
            
            SQL query:
            """
        )
        
        # Format entities for prompt
        entities_str = "None" if not extracted_entities else str(extracted_entities)
        
        # Generate SQL query
        prompt = prompt_template.format(
            query=user_query,
            schema=schema_str,
            entities=entities_str
        )
        
        sql_query = self.llm.generate_text(prompt)
        
        # Extract just the SQL query (remove any explanations)
        sql_query = self._extract_sql_from_response(sql_query)
        
        return sql_query
    
    def _format_schema_for_prompt(self):
        """Format database schema for LLM prompt."""
        if not self.table_schema:
            return "Table: player_game_stats (schema not available)"
        
        schema_lines = ["Table: player_game_stats"]
        for col in self.table_schema:
            schema_lines.append(f"- {col['name']} ({col['type']})")
        
        return "\n".join(schema_lines)
    
    def _extract_sql_from_response(self, response):
        """Extract SQL query from LLM response."""
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