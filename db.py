# db.py
import mysql.connector # Import MySQL connector library to interact with the database.
from config import DB_CONFIG # Import DB configuration from config.py

# This function returns a connection object using credentials and config from DB_CONFIG.
# It will be used by other modules to execute SQL queries.
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
