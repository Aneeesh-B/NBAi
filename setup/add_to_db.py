import pandas as pd
import sqlite3
import os

# --- 1. Configuration ---
# Update these three variables
CSV_FILE_PATH = 'PlayerStatistics.csv'
DB_NAME = 'nba_stats.db'
# The name you want the new table to have in the database.
# By default, it uses the CSV filename without the extension.
TABLE_NAME = "Player Individual Game Stats"
# --------------------------

print(f"Connecting to database: {DB_NAME}")
# This connects to your existing database file
conn = sqlite3.connect(DB_NAME)

print(f"Reading data from: {CSV_FILE_PATH}")
# Read the entire CSV file into a pandas DataFrame
df = pd.read_csv(CSV_FILE_PATH)

print(f"Writing data to new table: '{TABLE_NAME}'")
# Write the DataFrame to a new table in the SQLite database
df.to_sql(
    name=TABLE_NAME,
    con=conn,
    if_exists='replace', # Use 'replace' to create a new table, or overwrite if it exists.
    index=False        # Do not write the pandas DataFrame index as a column
)

# Close the database connection
conn.close()

print(f"✅ Successfully added '{CSV_FILE_PATH}' as the '{TABLE_NAME}' table in '{DB_NAME}'.")