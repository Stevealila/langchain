import os 
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.environ.get("PG_HOST")
PG_DATABASE = os.environ.get("PG_DATABASE")
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")


class User:
    def __init__(self):
        self.connection_params = {
            "host": PG_HOST,
            "database": PG_DATABASE,
            "user": PG_USER,
            "password": PG_PASSWORD
        }
    
    
    def get_connection(self):
        """Create a database connection"""
        return psycopg2.connect(**self.connection_params)
    

    def create_table(self, table_name="users"):
        """CREATE: Create a sample table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return f"Table '{table_name}' created successfully"
        except Exception as e:
            conn.rollback()
            return f"Error creating table: {e}"
        finally:
            cursor.close()
            conn.close()


    def insert_record(self, name, email, table_name="users"):
        """CREATE: Insert a record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {table_name} (name, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING RETURNING id",
                (name, email)
            )
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                return f"Record inserted with ID: {result[0]}"
            else:
                return f"Record with email '{email}' already exists, skipped insertion"
        except Exception as e:
            conn.rollback()
            return f"Error inserting record: {e}"
        finally:
            cursor.close()
            conn.close()
    
    
    def read_records(self, table_name="users"):
        """READ: Get all records"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            return records
        except Exception as e:
            return f"Error reading records: {e}"
        finally:
            cursor.close()
            conn.close()
    
    
    def delete_record(self, user_email, table_name="users"):
        """DELETE: Delete a record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE email = %s", (user_email,))
            affected = cursor.rowcount  
            conn.commit()
            
            if affected > 0:
                return f"Successfully deleted {affected} record(s) with email '{user_email}'"
            else:
                return f"No record found with email '{user_email}'"
        except Exception as e:
            conn.rollback()
            return f"Error deleting record: {e}"
        finally:
            cursor.close()
            conn.close()