import os
import sys
import time
import json
import psycopg

# --- Database Connection Details ---
# Read environment variables with default values for local development
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "secretpw")
DB_NAME = os.getenv("DB_NAME", "appdb")
TOP_N = int(os.getenv("APP_TOP_N", "5"))

def connect_with_retry(retries=10, delay=3):
    """Attempt to connect to the database with a retry mechanism."""
    last_err = None
    for i in range(retries):
        try:
            # Attempt to connect to the PostgreSQL database
            conn = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname=DB_NAME,
                connect_timeout=3
            )
            print("Successfully connected to the database.")
            return conn
        except Exception as e:
            last_err = e
            print(f"Waiting for database... (attempt {i+1}/{retries})", file=sys.stderr)
            time.sleep(delay)
    
    # If all retries fail, print error and exit
    print("Failed to connect to Postgres:", last_err, file=sys.stderr)
    sys.exit(1)

def main():
    """Main function to run queries and generate summary."""
    conn = connect_with_retry()
    
    # Use a cursor to execute queries
    with conn.cursor() as cur:
        
        # 1. Total number of trips
        cur.execute("SELECT COUNT(*) FROM trips;")
        total_trips = cur.fetchone()[0]
        
        # 2. Average fare by city
        cur.execute("""
            SELECT city, AVG(fare) 
            FROM trips 
            GROUP BY city 
            ORDER BY city;
        """)
        by_city = [{"city": c, "avg_fare": float(a)} for (c, a) in cur.fetchall()]
        
        # 3. Top N longest trips by duration
        cur.execute("""
            SELECT city, minutes, fare 
            FROM trips 
            ORDER BY minutes DESC 
            LIMIT %s;
        """, (TOP_N,))
        top_trips = [{"city": c, "minutes": m, "fare": float(f)} for (c, m, f) in cur.fetchall()]

    # Close the database connection
    conn.close()

    # --- Prepare the Summary Output ---
    summary = {
        "total_trips": int(total_trips),
        "avg_fare_by_city": by_city,
        f"top_{TOP_N}_longest_trips": top_trips
    }
    
    # --- Write Summary to File and Console ---
    # Create the output directory if it doesn't exist
    os.makedirs("/out", exist_ok=True)
    
    # Write summary to a JSON file
    with open("/out/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print a formatted summary to the console (stdout)
    print("\n=== Trip Summary ===")
    print(json.dumps(summary, indent=2))
    print("\nSummary successfully written to /out/summary.json")

if __name__ == "__main__":
    main()