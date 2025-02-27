import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        auth_plugin='mysql_native_password',  # Try this first
        use_pure=True,  # Use pure Python implementation
        connection_timeout=30
        )
        if connection.is_connected():
            print(f"Connected to MySQL Server version {connection.get_server_info()}")
            return connection
        else:
            print("Failed to connect to MySQL database.")
            return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def select_query(query, params=None):
    """Execute a SELECT query and return results"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if not connection:
            return None
            
        cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        result = cursor.fetchall()
        return result
        
    except Error as e:
        print(f"Query execution error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def execute_query(query, params=None):
    """Execute a non-SELECT query (INSERT, UPDATE, DELETE)"""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if not connection:
            return False
            
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        connection.commit()
        return True
        
    except Error as e:
        print(f"Query execution error: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

