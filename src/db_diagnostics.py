import sqlite3
import sys
import pandas as pd
import logging
import json
from datetime import datetime

# Add the parent directory to sys.path to ensure imports work correctly
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = 'data/ucla_wbb.db'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_header(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_table_names(conn):
    """Print all table names in the database."""
    print_header("DATABASE TABLES")
    try:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")
        print(f"\nTotal tables: {len(tables)}")
    except Exception as e:
        print(f"Error retrieving tables: {e}")
    print()

def print_table_schema(conn, table):
    """Print detailed schema information for a table."""
    print_header(f"SCHEMA FOR {table}")
    try:
        schema = conn.execute(f'PRAGMA table_info({table})').fetchall()
        if not schema:
            print(f"No schema found for table {table}")
            return
        
        print(f"{'Column':<20} {'Type':<15} {'NotNull':<8} {'Default':<15} {'PK':<4}")
        print("-" * 65)
        
        for col in schema:
            col_name = col[1]
            col_type = col[2]
            not_null = "YES" if col[3] else "NO"
            default_val = col[4] if col[4] is not None else ""
            primary_key = "YES" if col[5] else "NO"
            
            print(f"{col_name:<20} {col_type:<15} {not_null:<8} {str(default_val):<15} {primary_key:<4}")
        
        print(f"\nTotal columns: {len(schema)}")
        
        # Check for indexes
        indexes = conn.execute(f"PRAGMA index_list({table})").fetchall()
        if indexes:
            print(f"\nIndexes ({len(indexes)}):")
            for idx in indexes:
                print(f"  - {idx[1]} ({'UNIQUE' if idx[2] else 'NON-UNIQUE'})")
                
    except Exception as e:
        print(f"Error retrieving schema: {e}")
    print()

def analyze_data_types(conn, table):
    """Analyze actual data types and patterns in the table."""
    print_header(f"DATA TYPE ANALYSIS FOR {table}")
    try:
        # Get sample data
        sample_data = conn.execute(f"SELECT * FROM {table} LIMIT 100").fetchall()
        if not sample_data:
            print("No data found in table")
            return
        
        # Get column names
        columns = [description[0] for description in conn.execute(f"SELECT * FROM {table} LIMIT 1").description]
        
        print(f"Sample size: {len(sample_data)} rows")
        print(f"{'Column':<20} {'Sample Values':<40} {'Null Count':<12}")
        print("-" * 75)
        
        for i, col_name in enumerate(columns):
            # Get sample values
            sample_values = [str(row[i])[:30] if row[i] is not None else 'NULL' for row in sample_data[:3]]
            sample_str = ", ".join(sample_values)
            
            # Count nulls
            null_count = conn.execute(f'SELECT COUNT(*) FROM {table} WHERE "{col_name}" IS NULL').fetchone()[0]
            
            print(f"{col_name:<20} {sample_str:<40} {null_count:<12}")
            
    except Exception as e:
        print(f"Error analyzing data types: {e}")
    print()

def print_sample_data(conn, table, n=5):
    """Print sample data from the table."""
    print_header(f"SAMPLE DATA FROM {table} (showing {n} rows)")
    try:
        df = pd.read_sql_query(f'SELECT * FROM {table} LIMIT {n}', conn)
        if df.empty:
            print("No data found in table")
        else:
            print(df.to_string(index=False))
            print(f"\nTotal rows in table: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    except Exception as e:
        print(f"Error retrieving sample data: {e}")
    print()

def test_query_compatibility(conn):
    """Test various SQL queries for SQLite compatibility."""
    print_header("SQL COMPATIBILITY TESTS")
    
    test_queries = [
        # Basic queries (should work)
        ("Basic SELECT", "SELECT Name, Pts FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') LIMIT 5"),
        ("Basic aggregation", "SELECT Name, AVG(Pts) as avg_pts FROM ucla_player_stats WHERE Name NOT IN ('Totals', 'TM', 'Team') GROUP BY Name LIMIT 5"),
        ("Date filtering", "SELECT Name, Pts, game_date FROM ucla_player_stats WHERE date(game_date) >= date('2024-01-01') LIMIT 5"),
        
        # Advanced queries (potential issues)
        ("SQLite date functions", "SELECT Name, strftime('%Y', game_date) as year, AVG(Pts) FROM ucla_player_stats GROUP BY Name, year LIMIT 5"),
        ("Type casting", "SELECT Name, CAST(FGM AS REAL) / NULLIF(FGA, 0) as fg_pct FROM ucla_player_stats WHERE FGA > 0 LIMIT 5"),
        ("CTE (Common Table Expression)", """
            WITH player_avg AS (
                SELECT Name, AVG(Pts) as avg_pts 
                FROM ucla_player_stats 
                WHERE Name NOT IN ('Totals', 'TM', 'Team') 
                GROUP BY Name
            )
            SELECT * FROM player_avg ORDER BY avg_pts DESC LIMIT 5
        """),
        
        # Potentially problematic queries
        ("EXTRACT function (PostgreSQL)", "SELECT Name, EXTRACT(YEAR FROM game_date) FROM ucla_player_stats LIMIT 1"),
        ("INTERVAL syntax (PostgreSQL)", "SELECT Name FROM ucla_player_stats WHERE game_date >= '2024-01-01'::date + INTERVAL '30 days' LIMIT 1"),
        ("STDDEV function (PostgreSQL)", "SELECT Name, STDDEV(Pts) FROM ucla_player_stats GROUP BY Name LIMIT 1"),
    ]
    
    results = []
    for test_name, query in test_queries:
        try:
            start_time = pd.Timestamp.now()
            result = conn.execute(query).fetchall()
            execution_time = (pd.Timestamp.now() - start_time).total_seconds()
            
            status = "✓ SUCCESS"
            result_count = len(result)
            error_msg = None
            
        except Exception as e:
            status = "✗ FAILED"
            result_count = 0
            error_msg = str(e)
            execution_time = 0
        
        results.append({
            'test': test_name,
            'status': status,
            'rows': result_count,
            'time_ms': round(execution_time * 1000, 2),
            'error': error_msg
        })
        
        print(f"{status:<10} {test_name:<30} ({result_count} rows, {round(execution_time * 1000, 2)}ms)")
        if error_msg:
            print(f"           Error: {error_msg}")
    
    print(f"\nCompatibility Summary:")
    passed = len([r for r in results if 'SUCCESS' in r['status']])
    total = len(results)
    print(f"  Passed: {passed}/{total} ({round(passed/total*100, 1)}%)")
    
    return results

def test_rag_system_integration():
    """Test the RAG system components with the database."""
    print_header("RAG SYSTEM INTEGRATION TEST")
    
    try:
        # Import RAG components
        from db_connector import DatabaseConnector
        from query_generator import SQLQueryGenerator
        from entity_extractor import EntityExtractor
        from llm_utils import LLMManager
        
        print("✓ Successfully imported RAG components")
        
        # Test database connection
        db = DatabaseConnector(db_path=DB_PATH)
        connected = db.connect()
        
        if connected:
            print("✓ Database connection successful")
            
            # Test schema retrieval
            schema = db.get_table_schema()
            if schema:
                print(f"✓ Schema retrieval successful ({len(schema)} columns)")
            else:
                print("✗ Schema retrieval failed")
            
            # Test query statistics
            stats = db.get_query_statistics()
            print(f"✓ Query statistics: {stats}")
            
        else:
            print("✗ Database connection failed")
            return
        
        # Test LLM connection (if API key available)
        try:
            llm_manager = LLMManager()
            print("✓ LLM manager initialized")
            
            # Test entity extraction
            entity_extractor = EntityExtractor(db, llm_manager)
            print("✓ Entity extractor initialized")
            
            # Test query generation
            query_generator = SQLQueryGenerator(llm_manager, db)
            print("✓ Query generator initialized")
            
            # Test simple query generation
            test_query = "Who scored the most points?"
            entities = {"statistic": "points"}
            
            sql = query_generator.generate_sql_query(test_query, entities)
            is_valid, error = query_generator.validate_sql(sql)
            
            if is_valid:
                print(f"✓ Query generation and validation successful")
                print(f"  Generated SQL: {sql[:100]}...")
            else:
                print(f"✗ Query validation failed: {error}")
            
        except Exception as e:
            print(f"✗ LLM integration test failed: {e}")
            print("  (This may be due to missing API key or network issues)")
        
        db.close()
        
    except ImportError as e:
        print(f"✗ Failed to import RAG components: {e}")
    except Exception as e:
        print(f"✗ RAG integration test failed: {e}")

def generate_diagnostic_report(conn, compatibility_results):
    """Generate a comprehensive diagnostic report."""
    print_header("DIAGNOSTIC REPORT")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "database_path": DB_PATH,
        "database_info": {},
        "compatibility_results": compatibility_results,
        "recommendations": []
    }
    
    try:
        # Database info
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_name = tables[0][0] if tables else "unknown"
        
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        column_count = len(conn.execute(f"PRAGMA table_info({table_name})").fetchall())
        
        report["database_info"] = {
            "tables": len(tables),
            "main_table": table_name,
            "total_rows": row_count,
            "total_columns": column_count
        }
        
        # Analyze compatibility results
        passed_tests = len([r for r in compatibility_results if 'SUCCESS' in r['status']])
        total_tests = len(compatibility_results)
        
        # Generate recommendations
        recommendations = []
        
        if passed_tests < total_tests:
            recommendations.append("Some SQL compatibility tests failed - review PostgreSQL vs SQLite syntax")
        
        failed_tests = [r for r in compatibility_results if 'FAILED' in r['status']]
        if any('EXTRACT' in r['test'] for r in failed_tests):
            recommendations.append("Use strftime() instead of EXTRACT() for date operations")
        
        if any('INTERVAL' in r['test'] for r in failed_tests):
            recommendations.append("Use date() function instead of INTERVAL for date arithmetic")
        
        if any('STDDEV' in r['test'] for r in failed_tests):
            recommendations.append("Implement custom standard deviation calculation using AVG and subqueries")
        
        if passed_tests == total_tests:
            recommendations.append("All compatibility tests passed - system ready for production")
        
        report["recommendations"] = recommendations
        
        # Print summary
        print(f"Database: {DB_PATH}")
        print(f"Tables: {report['database_info']['tables']}")
        print(f"Main table: {report['database_info']['main_table']} ({row_count:,} rows, {column_count} columns)")
        print(f"SQL Compatibility: {passed_tests}/{total_tests} tests passed")
        
        print(f"\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        # Save report
        report_file = f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nDetailed report saved to: {report_file}")
        
    except Exception as e:
        print(f"Error generating diagnostic report: {e}")

def run_custom_query(conn, query):
    """Run a custom query provided by the user."""
    print_header("CUSTOM QUERY EXECUTION")
    print(f"Query: {query}")
    print("-" * 60)
    
    try:
        start_time = pd.Timestamp.now()
        result = conn.execute(query).fetchall()
        execution_time = (pd.Timestamp.now() - start_time).total_seconds()
        
        if result:
            # Try to format as DataFrame if possible
            try:
                columns = [desc[0] for desc in conn.execute(query).description]
                df = pd.DataFrame(result, columns=columns)
                print(df.to_string(index=False))
            except:
                # Fallback to simple print
                for row in result:
                    print(row)
        else:
            print("No results returned")
        
        print(f"\nExecution time: {execution_time*1000:.2f}ms")
        print(f"Rows returned: {len(result)}")
        
    except Exception as e:
        print(f"Error executing query: {e}")

def main():
    """Main diagnostic function."""
    print_header("UCLA BASKETBALL RAG SYSTEM DIAGNOSTICS")
    print(f"Database: {DB_PATH}")
    print(f"Timestamp: {datetime.now()}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return
    
    try:
        # Core diagnostics
        print_table_names(conn)
        
        tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for table in tables:
            print_table_schema(conn, table)
            analyze_data_types(conn, table)
            print_sample_data(conn, table)
        
        # SQL compatibility tests
        compatibility_results = test_query_compatibility(conn)
        
        # RAG system integration test
        test_rag_system_integration()
        
        # Generate diagnostic report
        generate_diagnostic_report(conn, compatibility_results)
        
        # Handle custom query if provided
        if len(sys.argv) > 1:
            custom_query = ' '.join(sys.argv[1:])
            run_custom_query(conn, custom_query)
        
    except Exception as e:
        print(f"Error during diagnostics: {e}")
    finally:
        conn.close()
        print("\n" + "="*60)
        print(" DIAGNOSTICS COMPLETE")
        print("="*60)

if __name__ == '__main__':
    main() 