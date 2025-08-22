from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google import genai

import sqlite3
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from dotenv import load_dotenv

from . import prompt
# import prompt

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
gcp_project = os.getenv("GOOGLE_CLOUD_PROJECT")
_AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_AGENTS_DIR, "nba_stats.db")
EMBEDDINGS_PATH = os.path.join(_AGENTS_DIR, "table_embeddings.npz")

client = genai.Client(vertexai=True, project=gcp_project)
    
def find_relevant_tables(question: str, top_k: int = 8) -> list[str]:
    """Finds the most relevant tables for a given question."""

    print("Loading pre-computed table embeddings...")
    loaded_data = np.load(EMBEDDINGS_PATH)
    table_names = loaded_data['table_names']
    table_embeddings = loaded_data['embeddings']

    response = client.models.embed_content(
        model="text-embedding-004", contents=question
    )

    question_embedding = np.array([response.embeddings[0].values])

    similarities = cosine_similarity(question_embedding, table_embeddings)[0]

    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        
    relevant_tables = [table_names[i] for i in top_k_indices]
    print(f"Found relevant tables: {relevant_tables}")
    return relevant_tables
    
def get_enhanced_schema(db_path: str, table_names: list[str]) -> str:
    """
    For a given list of tables, fetches their CREATE TABLE schema
    and the first 5 rows as a markdown table.
    """
    enhanced_info = []
    try:
        with sqlite3.connect(db_path) as conn:
            for table in table_names:
                # Get the CREATE TABLE statement
                schema_query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';"
                schema = pd.read_sql_query(schema_query, conn).iloc[0, 0]
                
                # Get the first 5 rows as examples
                examples_query = f"SELECT * FROM '{table}' LIMIT 5;"
                examples_df = pd.read_sql_query(examples_query, conn)
                
                # Format everything into a nice string
                table_info = (
                    f"Table: `{table}`\n"
                    f"Schema: {schema}\n"
                    f"Examples:\n{examples_df.to_markdown(index=False)}\n"
                )
                enhanced_info.append(table_info)
    except Exception as e:
        print(f"Error fetching enhanced schema: {e}")
        return ""
        
    return "\n---\n".join(enhanced_info)

def get_nba_stats(question: str) -> str:
    print(f"Tool called with question: {question}")
    
    relevant_tables = find_relevant_tables(question)
    enhanced_schema = get_enhanced_schema(DB_PATH, relevant_tables)    
    if not enhanced_schema:
        return "Sorry, I encountered an error while accessing the schema."
        
    try:
        

        SQL_TOOL_PROMPT = prompt.SQL_GENERATION_TEMPLATE.format(schema=enhanced_schema, question=question)

        sql_query = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SQL_TOOL_PROMPT
        )

        sql_query =  sql_query.text.strip()

        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        print(f"Generated SQL Query: {sql_query}")

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            

            if results:
                result_dict = dict(zip(columns, results[0]))
                print(f"Results: {result_dict}")
                return results
            else:
                return "No results found."
    except Exception as e:
        print(f"Error querying database: {e}")
        return "Sorry, I encountered an error while accessing the database."

root_agent = Agent(
    model="gemini-2.0-flash",
    name='nba_stats_agent',
    description='An intelligent assistant for NBA Stats that can answer complex questions by querying a SQL database of NBA Stats data.',
    tools=[FunctionTool(get_nba_stats)],
    instruction=prompt.ROOT_AGENT_INSTRUCTIONS
)

if __name__ == "__main__":
    print(get_schema(DB_PATH))
