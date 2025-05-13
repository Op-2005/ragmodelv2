class RAGPipeline:
    """Main RAG pipeline combining all components."""
    
    def __init__(self, llm_manager, db_connector, table_name="player_game_stats", dataset_type="nba"):
        """Initialize pipeline with LLM manager and database connector.
        
        Args:
            llm_manager: LLM manager instance
            db_connector: Database connector instance
            table_name: Name of the table to query
            dataset_type: Type of dataset (nba or ucla)
        """
        self.llm = llm_manager
        self.db = db_connector
        self.table_name = table_name
        self.dataset_type = dataset_type
        
        # Initialize components
        from src.entity_extractor import EntityExtractor
        from src.query_generator import SQLQueryGenerator
        
        self.entity_extractor = EntityExtractor(self.db, self.llm, table_name=self.table_name, dataset_type=self.dataset_type)
        self.query_generator = SQLQueryGenerator(self.llm, self.db, table_name=self.table_name)
    
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
            import traceback
            error_details = traceback.format_exc()
            print(f"Error processing query: {error_details}")
            return {
                "user_query": user_query,
                "error": str(e),
                "response": f"Sorry, I encountered an error processing your query: {str(e)}"
            }
    
    def _generate_response(self, user_query, sql_query, query_results):
        """Generate natural language response from query results."""
        # Create prompt for response generation based on dataset type
        if self.dataset_type == "ucla":
            dataset_description = "UCLA women's basketball statistics"
        else:
            dataset_description = "NBA statistics"
            
        prompt = f"""
        Based on the following information, provide a natural language answer to the user's question about {dataset_description}.
        
        User question: {user_query}
        
        SQL query used: {sql_query}
        
        Query results: {query_results}
        
        Provide a concise, clear answer that directly addresses the user's question based on the data.
        Format any statistics in a readable way and provide context about the players and games if relevant.
        """
        
        response = self.llm.generate_text(prompt)
        return response