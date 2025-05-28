import unittest
import sqlite3
import logging

DB_PATH = 'ragmodelv2/data/ucla_wbb.db'

logging.basicConfig(filename='test_sql_queries.log', level=logging.INFO)

class TestSQLQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def run_and_log(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            logging.info(f"SUCCESS: {query}\nResults: {results}")
            return results
        except Exception as e:
            logging.error(f"ERROR: {query}\nError: {e}")
            return None

    def test_stddev_workaround(self):
        # SQLite does not support STDDEV, so use variance workaround
        query = """
        SELECT Name, AVG(Pts) as avg_pts, 
        (AVG((Pts - (SELECT AVG(Pts) FROM ucla_player_stats)) * (Pts - (SELECT AVG(Pts) FROM ucla_player_stats)))) as variance
        FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') GROUP BY Name LIMIT 5;
        """
        results = self.run_and_log(query)
        self.assertIsNotNone(results)

    def test_player_vs_player(self):
        query = """
        SELECT Name, SUM(Pts) as total_pts FROM ucla_player_stats WHERE Name IN ('Betts, Lauren', 'Rice, Kiki') GROUP BY Name;
        """
        results = self.run_and_log(query)
        self.assertIsNotNone(results)

    def test_seasonal_improvement(self):
        query = """
        SELECT Name, MIN(game_date), MAX(game_date), MAX(Pts)-MIN(Pts) as improvement FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') GROUP BY Name LIMIT 5;
        """
        results = self.run_and_log(query)
        self.assertIsNotNone(results)

    def test_cte_fallback(self):
        # CTEs are supported in SQLite >= 3.8.3, but test a simple one
        query = """
        WITH player_totals AS (
            SELECT Name, SUM(Pts) as total_pts FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') GROUP BY Name
        )
        SELECT * FROM player_totals LIMIT 5;
        """
        results = self.run_and_log(query)
        self.assertIsNotNone(results)

    def test_simple_query(self):
        query = "SELECT Name, Pts FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') LIMIT 5;"
        results = self.run_and_log(query)
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main() 