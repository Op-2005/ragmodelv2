class RAGPipeline:
    """Main RAG pipeline for UCLA women's basketball data."""
    
    def __init__(self, llm_manager, db_connector, table_name="ucla_player_stats"):
        """Initialize pipeline with LLM manager and database connector.
        
        Args:
            llm_manager: LLM manager instance
            db_connector: Database connector instance
            table_name: Name of the table to query (default: ucla_player_stats)
        """
        self.llm = llm_manager
        self.db = db_connector
        self.table_name = table_name
        
        # Initialize components
        from src.entity_extractor import EntityExtractor
        from src.query_generator import SQLQueryGenerator
        
        self.entity_extractor = EntityExtractor(self.db, self.llm, table_name=self.table_name)
        self.query_generator = SQLQueryGenerator(self.llm, self.db, table_name=self.table_name)
    
    def process_query(self, user_query):
        """Process a natural language query and return response."""
        import logging
        logger = logging.getLogger(__name__)
        try:
            # Step 1: Extract entities from query
            extracted_entities = self.entity_extractor.extract_entities(user_query)
            logger.info(f"Extracted entities: {extracted_entities}")
            # Step 2: Generate SQL query
            sql_query = self.query_generator.generate_sql_query(user_query, extracted_entities)
            logger.info(f"Generated SQL: {sql_query}")
            # Step 3: Validate SQL
            valid, err = self.query_generator.validate_sql(sql_query)
            if not valid:
                logger.error(f"SQL validation failed: {err}")
                return {
                    "user_query": user_query,
                    "error": err,
                    "sql_query": sql_query,
                    "response": f"Sorry, the system generated an unsupported SQL query: {err}"
                }
            # Step 4: Execute SQL query
            if self.db.conn is None:
                self.db.connect()
            query_results, sql_error = self.db.execute_query(sql_query, return_error=True)
            if sql_error:
                logger.error(f"SQL execution error: {sql_error}")
                # Fallback: try a simpler query (e.g., remove aggregation/CTE)
                fallback_sql = self._fallback_query(user_query, extracted_entities)
                if fallback_sql:
                    logger.info(f"Trying fallback SQL: {fallback_sql}")
                    query_results, sql_error = self.db.execute_query(fallback_sql, return_error=True)
                    if sql_error:
                        logger.error(f"Fallback SQL error: {sql_error}")
                        return {
                            "user_query": user_query,
                            "error": sql_error,
                            "sql_query": fallback_sql,
                            "response": f"Sorry, there was an error running your query: {sql_error}"
                        }
                    sql_query = fallback_sql
                else:
                    return {
                        "user_query": user_query,
                        "error": sql_error,
                        "sql_query": sql_query,
                        "response": f"Sorry, there was an error running your query: {sql_error}"
                    }
            # Step 5: Generate natural language response
            response = self._generate_response(user_query, sql_query, query_results)
            return {
                "user_query": user_query,
                "extracted_entities": extracted_entities,
                "sql_query": sql_query,
                "query_results": query_results,
                "response": response
            }
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"Error processing query: {error_details}")
            return {
                "user_query": user_query,
                "error": str(e),
                "response": f"Sorry, I encountered an error processing your query: {str(e)}"
            }
    
    def _fallback_query(self, user_query, extracted_entities):
        """Attempt to generate a simpler fallback SQL query (e.g., remove aggregation/CTE)."""
        # For now, just try to remove common aggregation keywords
        import re
        fallback = re.sub(r'STDDEV|AVG|WITH|CTE|OVER|PARTITION BY', '', user_query, flags=re.IGNORECASE)
        # Regenerate SQL
        sql = self.query_generator.generate_sql_query(fallback, extracted_entities)
        valid, _ = self.query_generator.validate_sql(sql)
        if valid:
            return sql
        return None
    
    def _generate_response(self, user_query, sql_query, query_results):
        """Generate natural language response from query results."""
        # Create prompt for response generation
        prompt = f"""
        Based on the following information, provide a natural language answer to the user's question about UCLA women's basketball statistics.
        
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query results: {query_results}
        
        Provide a concise, clear answer that directly addresses the user's question based on the data.
        Format any statistics in a readable way and provide context about the players and games if relevant.
        """
        
        response = self.llm.generate_text(prompt)
        return response