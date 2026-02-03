import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class DatabaseConnection:
    def __init__(self):
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            print("Database connection established")
            return self.conn
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query"""
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params or ())
            self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            print(f"Query execution error: {e}")
            return None

# Singleton instance
_db = None

def get_db():
    global _db
    if _db is None:
        _db = DatabaseConnection()
        _db.connect()
    return _db
