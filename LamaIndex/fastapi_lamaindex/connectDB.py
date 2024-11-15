
import os
import snowflake.connector
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_connection():
    """Establishes a connection to Snowflake."""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            account=os.getenv("DB_ACCOUNT"),
            warehouse=os.getenv("DB_WAREHOUSE"),
            database=os.getenv("DB_NAME"),
            schema=os.getenv("DB_SCHEMA"),
            role=os.getenv("DB_USER_ROLE")
        )
        logger.info("Connected to Snowflake successfully")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {e}")
        return None

def close_connection(conn, cursor=None):
    """Closes the Snowflake connection."""
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info("Snowflake connection closed")
    except Exception as e:
        logger.error(f"Error closing Snowflake connection: {e}")
