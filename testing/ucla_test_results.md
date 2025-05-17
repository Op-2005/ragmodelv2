[
  {
    "query": "Who scored the most points in a single game this season?",
    "answer": "Lauren Betts scored the most points in a single game this season with 33 points against Maryland on January 26, 2025.",
    "sql_query": "SELECT Name, Pts, Opponent, game_date \nFROM ucla_player_stats \nWHERE Name NOT IN ('Totals', 'TM', 'Team')\nORDER BY Pts DESC \nLIMIT 1",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "points",
      "comparison": "most",
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "What was Lauren Betts' average points per game?",
    "answer": "Lauren Betts averaged 20.2 points per game for UCLA women's basketball.",
    "sql_query": "SELECT ROUND(AVG(Pts), 2) as avg_ppg \nFROM ucla_player_stats \nWHERE Name = 'Betts, Lauren' \nAND Name NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [
        "Betts, Lauren"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "points per game",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "How many three-pointers did Kiki Rice make against Richmond?",
    "answer": "Kiki Rice made 4 three-pointers in the game against Richmond.",
    "sql_query": "SELECT \"3PTM\"\nFROM ucla_player_stats \nWHERE Name = 'Rice, Kiki' \nAND Opponent = 'Richmond'\nAND Name NOT IN ('Totals', 'TM', 'Team');",
    "entities": {
      "player_names": [
        "Rice, Kiki"
      ],
      "player_number": null,
      "opponent": "Richmond",
      "statistic": "three-pointers",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Which player had the most rebounds in the LSU game?",
    "answer": "Gabriela Jaquez led UCLA with 8 rebounds in the LSU game.",
    "sql_query": "SELECT Name, Reb\nFROM ucla_player_stats \nWHERE Opponent = 'LSU' \nAND Name NOT IN ('Totals', 'TM', 'Team')\nORDER BY Reb DESC\nLIMIT 1",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": "LSU",
      "statistic": "rebounds",
      "comparison": "most",
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "How many assists did Gabriela Jaquez have this season?",
    "answer": "Gabriela Jaquez recorded 68 assists during the season for UCLA women's basketball.",
    "sql_query": "SELECT SUM(\"Ast\") as total_assists \nFROM ucla_player_stats \nWHERE Name = 'Jaquez, Gabriela' \nAND Name NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [
        "Jaquez, Gabriela"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "assists",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Who is player number 51?",
    "answer": "Player number 51 is Lauren Betts.",
    "sql_query": "SELECT DISTINCT first_name, last_name, \"No\"\nFROM ucla_player_stats \nWHERE \"No\" = '51' \nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')\nLIMIT 1;",
    "entities": {
      "player_names": [],
      "player_number": "51",
      "opponent": null,
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "What position does Londynn Jones play?",
    "answer": "Based on the available data, Londynn Jones wears jersey number 3 for UCLA women's basketball. However, the specific position she plays is not included in the provided query results. To accurately answer what position she plays, we would need additional data from the roster or player statistics.",
    "sql_query": "SELECT DISTINCT \"Name\", \"No\"\nFROM ucla_player_stats \nWHERE \"Name\" = 'Jones, Londynn' \nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')\nLIMIT 1;",
    "entities": {
      "player_names": [
        "Jones, Londynn"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "position",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "List all players who scored over 20 points in a game",
    "answer": "Several UCLA players scored over 20 points in games during the season, with Lauren Betts being the most prolific:\n\nLauren Betts had the highest-scoring performances, including:\n- 33 points vs Maryland (Jan 26)\n- 31 points vs both Colgate (Nov 10) and Ole Miss (Mar 28)\n- 30 points vs Richmond (Mar 23)\n- Multiple other 20+ point games\n\nOther players who scored over 20:\n- Kiki Rice: 23 points vs Richmond, 21 points vs Hawaii\n- Londynn Jones: 22 points vs Ohio State, 21 points vs Oregon\n- Gabriela Jaquez: 23 points vs Nebraska\n- Timea Gardiner: 23 points vs Arkansas\n- Angela Dugali\u0107: 22 points vs Long Beach State\n\nLauren Betts was particularly dominant, recording fifteen 20+ point games throughout the season, with her highest output being 33 points against Maryland.",
    "sql_query": "SELECT DISTINCT Name, Pts, Opponent, game_date \nFROM ucla_player_stats \nWHERE Pts > 20 \nAND Name NOT IN ('Totals', 'TM', 'Team')\nORDER BY Pts DESC;",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "points",
      "comparison": ">",
      "value": 20,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Which player had the highest field goal percentage?",
    "answer": "Elina Aarnisalo had the highest field goal percentage, shooting 100% from the field. This means she made all of her field goal attempts during the measured period.",
    "sql_query": "SELECT Name, \n       CAST(FGM AS FLOAT) / NULLIF(FGA, 0) * 100 as fg_percentage\nFROM ucla_player_stats \nWHERE Name NOT IN ('Totals', 'TM', 'Team')\n  AND FGA > 0\nGROUP BY Name, FGM, FGA\nORDER BY fg_percentage DESC\nLIMIT 1;",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "field goal percentage",
      "comparison": "highest",
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Who is the best three-point shooter on the team?",
    "answer": "I apologize, but since the query returned no results, I cannot determine who the best three-point shooter on the team is from the provided data. This could mean either the data is not available, or there might be an issue with the data source. To accurately answer this question, we would need valid statistics about the team's three-point shooting performance.",
    "sql_query": "SELECT \n    Name,\n    first_name,\n    last_name,\n    ROUND(CAST(SUM(3PTM) AS FLOAT) / NULLIF(SUM(3PTA), 0) * 100, 1) as three_pt_percentage,\n    SUM(3PTM) as made_threes,\n    SUM(3PTA) as attempted_threes\nFROM ucla_player_stats\nWHERE Name NOT IN ('Totals', 'TM', 'Team')\n    AND 3PTA > 0\nGROUP BY Name, first_name, last_name\nHAVING SUM(3PTA) >= 10\nORDER BY three_pt_percentage DESC, made_threes DESC;",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "three-point shooting",
      "comparison": ">",
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "What was the team's total score against South Carolina?",
    "answer": "UCLA scored 77 points in their game against South Carolina.",
    "sql_query": "SELECT SUM(Pts) as total_points \nFROM ucla_player_stats \nWHERE Opponent = 'South_Carolina' \nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": "South_Carolina",
      "statistic": "score",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Did UCLA beat Rutgers?",
    "answer": "Yes, UCLA scored 84 points against Rutgers in their game on January 23, 2025.",
    "sql_query": "SELECT SUM(\"Pts\") as ucla_points, \"Opponent\", \"game_date\" \nFROM ucla_player_stats \nWHERE \"Opponent\" = 'Rutgers' \nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')\nGROUP BY \"Opponent\", \"game_date\"",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": "Rutgers",
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "How many points did UCLA score against Maryland?",
    "answer": "UCLA scored 82 points against Maryland.",
    "sql_query": "SELECT SUM(\"Pts\") as total_points \nFROM ucla_player_stats \nWHERE \"Opponent\" = 'Maryland' \nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": "Maryland",
      "statistic": "points",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Which game did Lauren Betts score her season high?",
    "answer": "Lauren Betts scored her season-high of 33 points against Maryland on January 26, 2024.",
    "sql_query": "SELECT game_date, Opponent, \"Pts\"\nFROM ucla_player_stats \nWHERE Name = 'Betts, Lauren' \nAND Name NOT IN ('Totals', 'TM', 'Team')\nORDER BY \"Pts\" DESC\nLIMIT 1",
    "entities": {
      "player_names": [
        "Betts, Lauren"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "points",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "What was the team's shooting percentage against LSU?",
    "answer": "UCLA shot 38.2% from the field in their game against LSU.",
    "sql_query": "SELECT ROUND(CAST(SUM(FGM) AS FLOAT) / NULLIF(SUM(FGA), 0) * 100, 1) as shooting_percentage\nFROM ucla_player_stats \nWHERE Opponent = 'LSU'\nAND \"Name\" NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": "LSU",
      "statistic": "shooting percentage",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "What was the team's average points per game?",
    "answer": "UCLA women's basketball averaged 77.9 points per game during this period. This represents their scoring output across all games, calculated from individual player statistics.",
    "sql_query": "SELECT ROUND(AVG(total_points), 2) as avg_points_per_game\nFROM (\n    SELECT Opponent, SUM(\"Pts\") as total_points\n    FROM ucla_player_stats \n    WHERE \"Name\" NOT IN ('Totals', 'TM', 'Team')\n    GROUP BY Opponent\n) subquery;",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "points per game",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Who had the most total rebounds for the season?",
    "answer": "Lauren Betts led UCLA in rebounding for the season with 323 total rebounds.",
    "sql_query": "SELECT Name, SUM(Reb) as total_rebounds\nFROM ucla_player_stats \nWHERE Name NOT IN ('Totals', 'TM', 'Team')\nGROUP BY Name\nORDER BY total_rebounds DESC\nLIMIT 1;",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "rebounds",
      "comparison": "most",
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Calculate the team's overall three-point percentage",
    "answer": "The UCLA women's basketball team shot 33.5% from three-point range this season. This percentage represents all successful three-pointers made by individual players divided by their total three-point attempts.",
    "sql_query": "SELECT ROUND(CAST(SUM(\"3PTM\") AS FLOAT) / NULLIF(SUM(\"3PTA\"), 0) * 100, 1) as three_point_percentage\nFROM ucla_player_stats \nWHERE \"Name\" NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "three-point percentage",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Which player had the most consistent scoring across all games?",
    "answer": "I apologize, but I notice that while we have the SQL query, we don't have any actual results data to analyze. Without the query results, I cannot determine which player had the most consistent scoring across games. The query is designed to calculate scoring consistency using the coefficient of variation (standard deviation divided by mean), but without the output data, I cannot make any specific claims about player consistency.\n\nTo properly answer this question, we would need the actual results showing players' names, average points, standard deviations, games played, and their scoring consistency metrics.",
    "sql_query": "WITH player_scoring_stats AS (\n  SELECT \n    Name,\n    AVG(Pts) as avg_points,\n    STDDEV(Pts) as stddev_points,\n    COUNT(*) as games_played,\n    STDDEV(Pts) / CASE WHEN AVG(Pts) = 0 THEN 1 ELSE AVG(Pts) END as coefficient_of_variation\n  FROM ucla_player_stats\n  WHERE Name NOT IN ('Totals', 'TM', 'Team')\n  GROUP BY Name\n  HAVING COUNT(*) >= 5\n)\nSELECT \n  Name,\n  ROUND(avg_points, 2) as average_points,\n  ROUND(stddev_points, 2) as standard_deviation,\n  games_played,\n  ROUND(coefficient_of_variation, 3) as scoring_consistency\nFROM player_scoring_stats\nORDER BY coefficient_of_variation ASC\nLIMIT 10",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "scoring",
      "comparison": null,
      "value": null,
      "exclude_totals": true,
      "is_comparison_query": true
    }
  },
  {
    "query": "What was the team's assist-to-turnover ratio?",
    "answer": "UCLA's women's basketball team had an assist-to-turnover ratio of 0.77, meaning they averaged about 0.77 assists for every turnover committed. This indicates that the team had more turnovers than assists during the season.",
    "sql_query": "SELECT ROUND(CAST(SUM(Ast) AS FLOAT) / NULLIF(SUM(\"TO\"), 0), 2) as assist_turnover_ratio\nFROM ucla_player_stats \nWHERE Name NOT IN ('Totals', 'TM', 'Team')",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": "assist-to-turnover ratio",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Who is better at rebounding, Lauren Betts or Angela Dugali\u0107?",
    "answer": "I apologize, but since the query returned no results, I cannot make a direct comparison between Lauren Betts and Angela Dugali\u0107's rebounding statistics. This could be because either the data is not available in the database, or there might be an issue with how the players' names are formatted in the data. Without the actual statistics, I cannot determine who is the better rebounder between these two players.",
    "sql_query": "SELECT \n    Name,\n    COUNT(*) as games_played,\n    AVG(Reb) as avg_rebounds,\n    SUM(Reb) as total_rebounds,\n    ROUND(AVG(CAST(SPLIT_PART(\"OR-DR\", '-', 1) AS INTEGER)), 1) as avg_offensive_rebounds,\n    ROUND(AVG(CAST(SPLIT_PART(\"OR-DR\", '-', 2) AS INTEGER)), 1) as avg_defensive_rebounds\nFROM ucla_player_stats \nWHERE Name NOT IN ('Totals', 'TM', 'Team')\nAND Name IN ('Betts, Lauren', 'Dugali\u0107, Angela')\nGROUP BY Name\nORDER BY avg_rebounds DESC;",
    "entities": {
      "player_names": [
        "Betts, Lauren",
        "Dugali\u0107, Angela"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "rebounding",
      "comparison": null,
      "value": null,
      "exclude_totals": true,
      "is_comparison_query": true
    }
  },
  {
    "query": "Compare the scoring efficiency of Kiki Rice and Londynn Jones",
    "answer": "I apologize, but I notice that the query results came back as \"None,\" which means I don't have the actual statistical data to compare Kiki Rice and Londynn Jones's scoring efficiency. Without this data, I cannot make an accurate comparison between these two UCLA players. If you'd like to compare their scoring efficiency, we would need their field goal percentages, three-point percentages, free throw percentages, and overall scoring numbers.",
    "sql_query": "WITH player_stats AS (\n  SELECT \n    Name,\n    SUM(Pts) as total_points,\n    SUM(FGM) as made_fg,\n    SUM(FGA) as attempted_fg,\n    SUM(3PTM) as made_3pt,\n    SUM(3PTA) as attempted_3pt,\n    SUM(FTM) as made_ft,\n    SUM(FTA) as attempted_ft,\n    ROUND(CAST(SUM(FGM) AS FLOAT) / NULLIF(SUM(FGA), 0) * 100, 1) as fg_percentage,\n    ROUND(CAST(SUM(3PTM) AS FLOAT) / NULLIF(SUM(3PTA), 0) * 100, 1) as three_pt_percentage,\n    ROUND(CAST(SUM(FTM) AS FLOAT) / NULLIF(SUM(FTA), 0) * 100, 1) as ft_percentage\n  FROM ucla_player_stats\n  WHERE Name NOT IN ('Totals', 'TM', 'Team')\n  AND Name IN ('Rice, Kiki', 'Jones, Londynn')\n  GROUP BY Name\n)\nSELECT * FROM player_stats;",
    "entities": {
      "player_names": [
        "Rice, Kiki",
        "Jones, Londynn"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "scoring efficiency",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Which player should get more minutes, Gabriela Jaquez or Timea Gardiner?",
    "answer": "Based on the statistics from their 36 games played, Gabriela Jaquez appears to be the more productive player and deserves her current higher minutes allocation (26.8 minutes per game vs Gardiner's 18.3). Jaquez averages more points (9.6 vs 7.6), rebounds (5.3 vs 3.4), and assists (1.9 vs 1.2) than Gardiner, though she does average slightly more turnovers (2.2 vs 1.0). The data suggests Jaquez is making good use of her additional playing time with better overall production across most statistical categories.",
    "sql_query": "WITH player_stats AS (\n  SELECT \n    Name,\n    AVG(Min) as avg_minutes,\n    AVG(Pts) as avg_points,\n    AVG(Reb) as avg_rebounds,\n    AVG(Ast) as avg_assists,\n    AVG(\"TO\") as avg_turnovers,\n    COUNT(*) as games_played\n  FROM ucla_player_stats \n  WHERE Name IN ('Jaquez, Gabriela', 'Gardiner, Timea')\n  AND Name NOT IN ('Totals', 'TM', 'Team')\n  GROUP BY Name\n)\nSELECT \n  Name,\n  ROUND(avg_minutes, 1) as avg_minutes,\n  ROUND(avg_points, 1) as avg_points,\n  ROUND(avg_rebounds, 1) as avg_rebounds,\n  ROUND(avg_assists, 1) as avg_assists,\n  ROUND(avg_turnovers, 1) as avg_turnovers,\n  games_played\nFROM player_stats\nORDER BY Name;",
    "entities": {
      "player_names": [
        "Jaquez, Gabriela",
        "Gardiner, Timea"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "minutes",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Is Lauren Betts more effective against stronger or weaker opponents?",
    "answer": "Based on the data, Lauren Betts has generally performed better against high-profile opponents, though her performance has been somewhat mixed. She had strong showings against several ranked teams:\n\n- 33 points (93.3% FG) vs Maryland\n- 26 points (61.1% FG) vs UConn\n- 25 points (75% FG) vs Indiana\n- 24 points (58.8% FG) vs Baylor\n\nHowever, she had more modest performances against some other top teams:\n- 11 points vs South Carolina\n- 17 points vs LSU\n- 22 points vs Iowa\n\nHer highest scoring games have come against a mix of stronger and weaker opponents, suggesting that her effectiveness isn't strictly tied to opponent strength. Her shooting efficiency has remained generally high regardless of opponent, frequently shooting above 60% from the field against both strong and weaker teams.\n\nThe data indicates she's a consistent performer who can excel against any level of competition, though there's some variability in her scoring output.",
    "sql_query": "SELECT \n    Name,\n    Opponent,\n    ROUND(AVG(CAST(Pts AS FLOAT)), 2) as avg_points,\n    ROUND(AVG(CAST(Reb AS FLOAT)), 2) as avg_rebounds,\n    ROUND(AVG(CAST(FGM AS FLOAT) * 100.0 / NULLIF(CAST(FGA AS FLOAT), 0)), 2) as fg_percentage,\n    COUNT(*) as games_played\nFROM ucla_player_stats\nWHERE Name = 'Betts, Lauren'\n    AND Name NOT IN ('Totals', 'TM', 'Team')\nGROUP BY Name, Opponent\nORDER BY avg_points DESC;",
    "entities": {
      "player_names": [
        "Betts, Lauren"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": false
    }
  },
  {
    "query": "Who performs better in close games, Kiki Rice or Londynn Jones?",
    "answer": "Based on the empty query results, I cannot make a comparison between Kiki Rice and Londynn Jones' performance in close games (defined as games decided by 10 points or less). This could mean either there were no close games in the dataset, or there might be an issue with how the players' names are recorded in the database. Without any statistical data to analyze, I cannot determine who performs better in close game situations.",
    "sql_query": "WITH close_games AS (\n  SELECT DISTINCT game_date, Opponent \n  FROM ucla_player_stats\n  GROUP BY game_date, Opponent\n  HAVING MAX(Pts) - MIN(Pts) <= 10\n),\nplayer_stats AS (\n  SELECT \n    Name,\n    AVG(Pts) as avg_points,\n    AVG(Ast) as avg_assists,\n    AVG(Reb) as avg_rebounds,\n    AVG(Stl) as avg_steals,\n    AVG(CAST(FGM AS FLOAT) / NULLIF(FGA, 0)) as fg_pct,\n    COUNT(*) as games_played\n  FROM ucla_player_stats s\n  JOIN close_games c ON s.game_date = c.game_date\n  WHERE Name NOT IN ('Totals', 'TM', 'Team')\n  AND Name IN ('Rice, Kiki', 'Jones, Londynn')\n  GROUP BY Name\n)\nSELECT \n  Name,\n  ROUND(avg_points, 1) as avg_points,\n  ROUND(avg_assists, 1) as avg_assists,\n  ROUND(avg_rebounds, 1) as avg_rebounds,\n  ROUND(avg_steals, 1) as avg_steals,\n  ROUND(fg_pct * 100, 1) as fg_percentage,\n  games_played\nFROM player_stats\nORDER BY Name;",
    "entities": {
      "player_names": [
        "Rice, Kiki",
        "Jones, Londynn"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "How did Lauren Betts and Kiki Rice perform against South Carolina?",
    "answer": "Lauren Betts and Kiki Rice each scored 11 points against South Carolina. Betts had a strong all-around game, shooting 5-8 from the field and grabbing 14 rebounds while adding 3 blocks and 4 steals in 37 minutes. Rice played 29 minutes and shot 5-11 from the field, though she struggled from three-point range (0-2). Both players had some turnover issues, with Betts committing 4 and Rice having 3.",
    "sql_query": "SELECT \n    Name,\n    \"Min\",\n    FGM || '-' || FGA as \"FG\",\n    \"3PTM\" || '-' || \"3PTA\" as \"3PT\",\n    FTM || '-' || FTA as \"FT\",\n    \"Reb\",\n    \"Ast\",\n    \"TO\",\n    \"Blk\",\n    \"Stl\",\n    \"PF\",\n    \"Pts\"\nFROM ucla_player_stats \nWHERE Opponent = 'South_Carolina' \nAND Name NOT IN ('Totals', 'TM', 'Team')\nAND Name IN ('Betts, Lauren', 'Rice, Kiki')\nORDER BY Name;",
    "entities": {
      "player_names": [
        "Betts, Lauren",
        "Rice, Kiki"
      ],
      "player_number": null,
      "opponent": "South_Carolina",
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "What's the combined scoring average of Londynn Jones and Gabriela Jaquez?",
    "answer": "Londynn Jones and Gabriela Jaquez combine to average 18.8 points per game for UCLA's women's basketball team.",
    "sql_query": "SELECT ROUND(AVG(combined_pts), 2) as avg_combined_pts\nFROM (\n    SELECT game_date, SUM(Pts) as combined_pts\n    FROM ucla_player_stats \n    WHERE Name IN ('Jones, Londynn', 'Jaquez, Gabriela')\n    AND Name NOT IN ('Totals', 'TM', 'Team')\n    GROUP BY game_date\n) subquery;",
    "entities": {
      "player_names": [
        "Jones, Londynn",
        "Jaquez, Gabriela"
      ],
      "player_number": null,
      "opponent": null,
      "statistic": "scoring average",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Compare the performances of UCLA's starters and bench players",
    "answer": "Here's how UCLA's starters and bench players compared:\n\nStarters (players averaging 20+ minutes):\n- Played 27.0 minutes per game\n- Shot more efficiently (47.0% FG, 32.2% from three)\n- Averaged 11.3 points, 5.1 rebounds, and 1.8 assists\n\nBench players (under 20 minutes):\n- Played 12.6 minutes per game\n- Shot less efficiently (37.2% FG, 28.2% from three)\n- Averaged 3.9 points, 2.5 rebounds, and 1.4 assists\n\nThe starters were significantly more productive and efficient, which is expected given their larger role. However, when accounting for playing time, the bench players' production was relatively proportional to their minutes.",
    "sql_query": "WITH starters AS (\n  SELECT \n    AVG(\"Min\") as avg_minutes,\n    ROUND(AVG(CAST(\"FGM\" AS FLOAT) / NULLIF(CAST(\"FGA\" AS FLOAT), 0) * 100), 1) as fg_pct,\n    ROUND(AVG(CAST(\"3PTM\" AS FLOAT) / NULLIF(CAST(\"3PTA\" AS FLOAT), 0) * 100), 1) as three_pt_pct,\n    ROUND(AVG(\"Pts\"), 1) as avg_points,\n    ROUND(AVG(\"Reb\"), 1) as avg_rebounds,\n    ROUND(AVG(\"Ast\"), 1) as avg_assists,\n    'Starters' as player_group\n  FROM ucla_player_stats\n  WHERE \"Name\" NOT IN ('Totals', 'TM', 'Team')\n  AND \"Min\" >= 20\n),\nbench AS (\n  SELECT \n    AVG(\"Min\") as avg_minutes,\n    ROUND(AVG(CAST(\"FGM\" AS FLOAT) / NULLIF(CAST(\"FGA\" AS FLOAT), 0) * 100), 1) as fg_pct,\n    ROUND(AVG(CAST(\"3PTM\" AS FLOAT) / NULLIF(CAST(\"3PTA\" AS FLOAT), 0) * 100), 1) as three_pt_pct,\n    ROUND(AVG(\"Pts\"), 1) as avg_points,\n    ROUND(AVG(\"Reb\"), 1) as avg_rebounds,\n    ROUND(AVG(\"Ast\"), 1) as avg_assists,\n    'Bench' as player_group\n  FROM ucla_player_stats\n  WHERE \"Name\" NOT IN ('Totals', 'TM', 'Team')\n  AND \"Min\" < 20\n)\nSELECT * FROM starters\nUNION ALL\nSELECT * FROM bench\nORDER BY player_group",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": null,
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "How many points did Lauren Betts, Kiki Rice, and Londynn Jones score against Rutgers?",
    "answer": "Against Rutgers, Lauren Betts led the scoring among these three players with 25 points, while Londynn Jones added 12 points and Kiki Rice contributed 10 points.",
    "sql_query": "SELECT Name, Pts \nFROM ucla_player_stats \nWHERE Name IN ('Betts, Lauren', 'Rice, Kiki', 'Jones, Londynn')\nAND Opponent = 'Rutgers' \nAND Name NOT IN ('Totals', 'TM', 'Team')\nORDER BY Name;",
    "entities": {
      "player_names": [
        "Betts, Lauren",
        "Rice, Kiki",
        "Jones, Londynn"
      ],
      "player_number": null,
      "opponent": "Rutgers",
      "statistic": "points",
      "comparison": null,
      "value": null,
      "exclude_totals": false,
      "is_comparison_query": true
    }
  },
  {
    "query": "Which players improved the most from the beginning to the end of the season?",
    "answer": "I apologize, but I notice that while we have the SQL query, we don't have the actual results from the query in the provided information. Without the query results showing the statistical improvements for different players, I cannot make specific claims about which players improved the most over the season.\n\nThe query is designed to compare players' performance metrics (points, assists, rebounds, and turnovers) between the first 30 days and last 30 days of the season, but without the actual numbers, I cannot identify which players showed the most improvement.\n\nTo properly answer this question, we would need the query results showing the statistical differences for each player.",
    "sql_query": "WITH player_early_stats AS (\n  SELECT \n    Name,\n    AVG(Pts) as early_pts,\n    AVG(\"Ast\") as early_ast,\n    AVG(\"Reb\") as early_reb,\n    AVG(\"TO\") as early_to\n  FROM ucla_player_stats\n  WHERE Name NOT IN ('Totals', 'TM', 'Team')\n  AND game_date <= (\n    SELECT MIN(game_date) + interval '30 days'\n    FROM ucla_player_stats\n  )\n  GROUP BY Name\n),\nplayer_late_stats AS (\n  SELECT \n    Name,\n    AVG(Pts) as late_pts,\n    AVG(\"Ast\") as late_ast,\n    AVG(\"Reb\") as late_reb,\n    AVG(\"TO\") as late_to\n  FROM ucla_player_stats\n  WHERE Name NOT IN ('Totals', 'TM', 'Team')\n  AND game_date >= (\n    SELECT MAX(game_date) - interval '30 days'\n    FROM ucla_player_stats\n  )\n  GROUP BY Name\n)\nSELECT \n  e.Name,\n  (l.late_pts - e.early_pts) as pts_improvement,\n  (l.late_ast - e.early_ast) as ast_improvement,\n  (l.late_reb - e.early_reb) as reb_improvement,\n  (e.early_to - l.late_to) as to_improvement\nFROM player_early_stats e\nJOIN player_late_stats l ON e.Name = l.Name\nORDER BY (\n  (l.late_pts - e.early_pts) + \n  (l.late_ast - e.early_ast) + \n  (l.late_reb - e.early_reb) + \n  (e.early_to - l.late_to)\n) DESC",
    "entities": {
      "player_names": [],
      "player_number": null,
      "opponent": null,
      "statistic": null,
      "comparison": ">",
      "value": null,
      "exclude_totals": true,
      "is_comparison_query": true
    }
  }
]