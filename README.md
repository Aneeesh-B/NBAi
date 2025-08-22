# 🏀 NBAi: The Conversational NBA Stats Analyst

NBAi is an advanced AI agent that understands complex questions about NBA history and statistics. It acts as a data analyst, converting natural language into precise SQL queries, fetching data from a comprehensive basketball database, and even constructing data-driven arguments to settle classic fan debates.

This project leverages a powerful Large Language Model (LLM) with a sophisticated retrieval mechanism to intelligently select the most relevant data tables for any given question, ensuring accurate and efficient query generation.

---

## ✨ Features

-   **Natural Language to SQL:** Ask questions like "Who scored the most points in a single game during the 2023 season?" and get a direct answer from the database.
-   **Intelligent Table Retrieval:** Uses vector embeddings to semantically search and select only the most relevant database tables for a query, improving accuracy and efficiency.
-   **Complex Query Handling:** Capable of answering multi-step, comparative, and time-based questions (e.g., "Who shot better from three, Larry Bird in his best season or Stephen Curry in his worst?").
-   **Argument Generation:** Ask the agent to argue a point (e.g., "Explain why Steph Curry is a better shooter than Kobe Bryant"), and it will autonomously gather the necessary stats to build a case.
-   **Interactive Chat Interface:** Built with a user-friendly chat UI for a seamless conversational experience.

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.9+
-   A Google Cloud Platform (GCP) project with the **Vertex AI API** enabled.

### 2. Installation

First, clone the repository to your local machine:
```bash
git clone [https://github.com/your-username/NBA-Stats-Agent.git](https://github.com/your-username/NBA-Stats-Agent.git)
cd NBA-Stats-Agent
```
Next, create and activate a Python virtual environment. This keeps your project dependencies isolated.

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
For Windows:
```bash
python -m venv venv
.\\venv\\Scripts\\activate
```
Now, install all the required libraries from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
### 3. Configuration
Before running the agent, you need to set up your data, API credentials, and table embeddings.

#### Step A: Set Up the Database
Download the NBA statistics dataset. A great source is the [NBA Stats dataset on Kaggle](https://www.kaggle.com/datasets/nathanlauga/nba-games).
Unzip the archive and place all the `.csv` files into a new folder named `data_csvs` in the root of the project directory.
Run the `create_database.py` script to compile all the CSVs into a single SQLite database file.
```bash
python create_database.py
```
This will create an `nba_stats.db` file, which the agent will query.

#### Step B: Set Up Your API Key
Create a file named `.env` in the root of your project directory.
Add your Google Cloud credentials to this file. The agent needs your API key and the Project ID associated with it.
```
GOOGLE_API_KEY="your-google-api-key-here"
GOOGLE_CLOUD_PROJECT="your-gcp-project-id-here"
```

#### Step C: Pre-compute Table Embeddings
To enable the intelligent table retrieval, you must run a one-time script to analyze the database schema and save the embeddings locally.
```bash
python create_embeddings.py
```
This will create a `table_embeddings.npz` file. You only need to do this once, unless you change the database schema.

### 🏃‍♀️ Running the Agent
With the setup complete, you can now start the interactive chat application.
This project uses Chainlit to create the web interface. To run the app, execute the following command in your terminal:
```bash
chainlit run app.py -w
```
This will start a local server, and you can open the provided URL in your browser to begin chatting with the NBAi agent. The `-w` flag enables auto-reloading, which is helpful for development.

### 💬 Example Questions
Here are a few examples of questions you can ask the agent:

* **Simple Lookup:** "What were Michael Jordan's per-game stats in the 1998 season?"
* **Time-Based Aggregation:** "How many total rebounds did Shaquille O'Neal have during the 2001 playoffs?"
* **Comparative Analysis:** "Who had a higher Player Efficiency Rating (PER) in their rookie season, LeBron James or Michael Jordan?"
* **Complex Argument:** "Explain why you think Nikola Jokic is the best offensive center of all time, using stats to back up your claims."
