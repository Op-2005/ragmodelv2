from langchain_core.prompts import PromptTemplate
import re

class SQLQueryGenerator:
    """Generate SQL queries from natural language for UCLA women's basketball data."""
    
    def __init__(self, llm_manager, db_connector, table_name="ucla_player_stats"):
        """Initialize with LLM manager and database connector.
        
        Args:
            llm_manager: LLM manager instance
            db_connector: Database connector instance
            table_name: Name of the table to query (default: ucla_player_stats)
        """
        self.llm = llm_manager
        self.db = db_connector
        self.table_name = table_name
        
        # Get database schema
        self.table_schema = self.db.get_table_schema(table_name=self.table_name)
        
        self.column_map = {
            "points": "Pts",
            "rebounds": "Reb",
            "assists": "Ast",
            "steals": "Stl",
            "blocks": "Blk",
            "turnovers": "TO",
            "field goals": "FG",
            "three pointers": "3PT",
            "free throws": "FT",
            "minutes": "Min",
            "opponent": "Opponent",
            "date": "game_date",
            # Add more mappings as needed
        }
    
    def generate_sql_query(self, user_query, extracted_entities=None):
        """Generate SQL query from user query and extracted entities."""
        # Format table schema for prompt
        schema_str = self._format_schema_for_prompt()
        
        # Map statistics in user query/entities to schema columns
        if extracted_entities and extracted_entities.get("statistic"):
            stat = extracted_entities["statistic"].lower()
            if stat in self.column_map:
                user_query = user_query.replace(stat, self.column_map[stat])
        
        # Create prompt for SQL generation
        prompt = f"""
        You are an expert SQL query generator for a UCLA women's basketball statistics database.
        
        Given a natural language query, generate a valid SQL query to answer the question.
        
        Database schema:
        {schema_str}
        
        Extracted entities:
        {extracted_entities if extracted_entities else 'None'}
        
        User question: {user_query}
        
        IMPORTANT NOTES:
        1. Exclude rows where Name='Totals' or Name='TM' or Name='Team' as these are team totals, not individual players.
        2. When querying for individual player stats, always add WHERE Name NOT IN ('Totals', 'TM', 'Team') to your query.
        3. Make sure the query is valid SQL and uses only columns that exist in the schema.
        4. For comparison queries between players, use multiple SELECT statements or subqueries to get statistics for each player.
        5. If the query is asking for a recommendation or comparison between players, return data for all players mentioned so the LLM can make the comparison.
        6. CRITICAL: Always put column names in double quotes, especially for reserved SQL keywords. For example, use "TO" instead of TO for the turnovers column.
        
        Generate only the SQL query with no other text.
        
        SQL query:
        """
        
        # Generate SQL query
        sql_query = self.llm.generate_text(prompt)
        
        # Extract just the SQL query (remove any explanations)
        sql_query = self._extract_sql_from_response(sql_query)
        sql_query = self._sqlite_compat(sql_query)
        
        return sql_query
    
    def _format_schema_for_prompt(self):
        """Format database schema for LLM prompt."""
        if not self.table_schema:
            return f"Table: {self.table_name} (schema not available)"
        
        schema_lines = [f"Table: {self.table_name}"]
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

    def _sqlite_compat(self, sql_query):
        """Patch SQL for SQLite compatibility (e.g., replace STDDEV, unsupported functions)."""
        # Replace STDDEV with custom aggregation (if needed)
        if "STDDEV" in sql_query.upper():
            # SQLite does not support STDDEV by default
            # Replace with a workaround or raise a warning
            sql_query = sql_query.replace("STDDEV", "(AVG((Pts - AVG(Pts)) * (Pts - AVG(Pts))))")
            # This is a placeholder; for real stddev, use a custom aggregate or calculate in Python
        # Remove unsupported PostgreSQL syntax
        for keyword in ["ILIKE", "SIMILAR TO", "::", "INTERVAL", "DATE_TRUNC", "EXTRACT", "ARRAY", "UNNEST", "LEAD", "LAG", "RANK", "ROW_NUMBER", "OVER", "PARTITION BY"]:
            if keyword in sql_query.upper():
                sql_query += f" -- WARNING: {keyword} is not supported in SQLite."
        return sql_query

    def validate_sql(self, sql_query):
        """Validate SQL for SQLite compatibility before execution."""
        # Simple check for unsupported functions
        unsupported = ["STDDEV", "ILIKE", "SIMILAR TO", "::", "INTERVAL", "DATE_TRUNC", "EXTRACT", "ARRAY", "UNNEST", "LEAD", "LAG", "RANK", "ROW_NUMBER", "OVER", "PARTITION BY"]
        for kw in unsupported:
            if kw in sql_query.upper():
                return False, f"Unsupported SQL keyword for SQLite: {kw}"
        return True, None