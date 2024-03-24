import sqlite3

# Establish a connection to the database
CONN = sqlite3.connect('company.db')

# Create a cursor object to interact with the database
CURSOR = CONN.cursor()

# Ensure foreign key constraints are enabled
CURSOR.execute("PRAGMA foreign_keys = ON")

# Import the Employee and Review classes
from .Employee import Employee
from .Review import Review
