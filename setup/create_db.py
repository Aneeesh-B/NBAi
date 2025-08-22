import os
import pandas as pd
import sqlite3

csvs_path="nba_stats_csvs"

db_name="nba_stats.db"
conn = sqlite3.connect(db_name)
print(f"Connected to database: {db_name}")

for file in os.listdir(csvs_path):
    if file.endswith(".csv"):
        print(f"Processing file: {file}")
        file_path = os.path.join(csvs_path, file)

        table_name=file.replace(".csv","")

        df = pd.read_csv(file_path)
        df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

conn.close()
print(f"Database {db_name} created successfully.")

