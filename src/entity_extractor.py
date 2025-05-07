import re
import json
from thefuzz import process
from langchain_core.prompts import PromptTemplate

class EntityExtractor:
    """Extract and resolve entities from user queries."""
    
    def __init__(self, db_connector, llm_manager):
        """Initialize with database connector and LLM manager."""
        self.db = db_connector
        self.llm = llm_manager
        self.entity_cache = {}  # Cache for entity resolution results
        
        # Pre-load common entities for faster matching
        self._load_common_entities()
    
    def _load_common_entities(self):
        """Load common entities like teams and player names from database."""
        # Load teams
        self.teams = self.db.get_distinct_values("teamName")
        
        # Load players
        self.players = self.db.get_distinct_values("personName")
        
        # Load opponents
        self.opponents = self.db.get_distinct_values("opponent")
        
        # Load seasons
        self.seasons = self.db.get_distinct_values("season_year")
    
    def extract_entities(self, query):
        """Extract entities from query using LLM."""
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""
            Extract entities from this NBA statistics query.
            Return a JSON object with these fields:
            - player_name: Full name of player mentioned (if any)
            - team_name: Team name mentioned (if any)
            - opponent: Opponent team mentioned (if any)
            - season: Season mentioned (if any)
            - statistic: Specific statistic mentioned (points, rebounds, assists, etc.)
            - comparison: Any comparison operators (>, <, =, etc.)
            - value: Any numeric value mentioned for comparison
            
            Query: {query}
            
            JSON output:
            """
        )
        
        # Generate extraction using LLM
        prompt = prompt_template.format(query=query)
        result = self.llm.generate_text(prompt)
        
        # Parse the JSON from the response
        try:
            # Find the JSON part in the response
            json_match = re.search(r'({.*})', result, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                entities = json.loads(json_str)
            else:
                # Fallback to matching with pattern extraction
                entities = self._pattern_extract_entities(query)
        except Exception as e:
            print(f"Error parsing JSON from LLM: {str(e)}")
            # Fallback to pattern extraction
            entities = self._pattern_extract_entities(query)
        
        # Resolve and validate entities
        return self._resolve_entities(entities)
    
    def _pattern_extract_entities(self, query):
        """Fallback extraction using regex patterns."""
        entities = {
            "player_name": None,
            "team_name": None,
            "opponent": None,
            "season": None,
            "statistic": None,
            "comparison": None,
            "value": None
        }
        
        # Extract statistics
        stat_keywords = ["points", "rebounds", "assists", "steals", "blocks", "turnovers"]
        for stat in stat_keywords:
            if stat in query.lower():
                entities["statistic"] = stat
                break
        
        # Extract seasons (like 2023-24)
        season_pattern = r'(\d{4}-\d{2,4}|\d{4}[-/]\d{2,4})'
        season_match = re.search(season_pattern, query)
        if season_match:
            entities["season"] = season_match.group(1)
        
        # Extract comparisons
        comparison_pattern = r'(more than|less than|at least|at most|equal to|>|<|>=|<=|=)'
        comparison_match = re.search(comparison_pattern, query)
        if comparison_match:
            entities["comparison"] = comparison_match.group(1)
        
        # Extract numeric values
        value_pattern = r'\b(\d+)\b'
        value_match = re.search(value_pattern, query)
        if value_match:
            entities["value"] = value_match.group(1)
        
        return entities
    
    def _resolve_entities(self, entities):
        """Resolve extracted entities to database entries using fuzzy matching."""
        resolved = entities.copy()
        
        # Resolve player name
        if entities.get("player_name"):
            player_match = self._fuzzy_match(entities["player_name"], self.players)
            if player_match:
                resolved["player_name"] = player_match
        
        # Resolve team name
        if entities.get("team_name"):
            team_match = self._fuzzy_match(entities["team_name"], self.teams)
            if team_match:
                resolved["team_name"] = team_match
        
        # Resolve opponent
        if entities.get("opponent"):
            opponent_match = self._fuzzy_match(entities["opponent"], self.opponents)
            if opponent_match:
                resolved["opponent"] = opponent_match
        
        # Resolve season
        if entities.get("season"):
            season_match = self._fuzzy_match(entities["season"], self.seasons)
            if season_match:
                resolved["season"] = season_match
        
        return resolved
    
    def _fuzzy_match(self, query, options, threshold=80):
        """Find the best match for a query in a list of options."""
        if not query or not options:
            return None
            
        # Check cache first
        cache_key = f"{query}:{','.join(options[:5])}"
        if cache_key in self.entity_cache:
            return self.entity_cache[cache_key]
        
        # Find best match
        match, score = process.extractOne(query, options)
        
        # Only accept match if score is above threshold
        if score >= threshold:
            self.entity_cache[cache_key] = match
            return match
        
        return None