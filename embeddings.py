import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
import google.auth

load_dotenv()

TABLE_METADATA = {
    # Player Stat Tables (Primary)
    "Player Per Game": "The primary table for individual player performance, containing per-game averages for every full season. Use this for questions about points per game (pts_per_game), rebounds, assists, steals, blocks, turnovers, and shooting percentages like field goal percent (fg_percent) and three-point percentage (x3p_percent).",
    "Player Totals": "Contains the cumulative season totals for individual players across a full season. Use this for questions about total points (pts), total rebounds (trb), total assists (ast), and other cumulative stats over a full season, not averages.",
    "Player Shooting": "Contains highly detailed individual player shooting data across a full season. Use this for complex questions about a player's shooting effectiveness from different ranges (e.g., 0-3 feet, 3-10 feet, corner threes), the percentage of shots that were assisted, number of dunks, and career-highs for specific shooting stats.",
    "Advanced": "Contains advanced  statistics for individual players for each full season. Use this for deep statistical analysis involving metrics like Player Efficiency Rating (per), True Shooting Percentage (ts_percent), Win Shares (ows, dws, ws), Box Plus/Minus (bpm), and Value Over Replacement Player (vorp).",

    "Player Individual Game Stats": "Contains player statistics for individual games. Use this for questions that require looking at unique game box score stats like 'What's the most points Kobe Bryant scored in 2006?' This is also necessary for looking at stats over a specific time period (e. g. LeBron James stats in January 2014).",

    # Player Stat Tables (Normalized)
    "Per 100 Poss": "Contains player statistics normalized per 100 team possessions by season. This is useful for comparing players' production in a pace-adjusted manner, removing the effect of team speed on their stats.",
    "Per 36 Minutes": "Contains player statistics normalized to a per-36-minute basis by season. This is useful for comparing the per-minute production of players who have different roles or playing times (e.g., a starter vs. a bench player).",

    # Player Information & Awards
    "Player Career Info": "Contains biographical and high-level career data for individual players. Use this to find a player's height (ht_in_in), weight (wt), birth date, college, and Hall of Fame (hof) status. This table is essential for linking a player's name to their unique player_id.",
    "Player Award Shares": "Details the results of voting for major individual awards (like MVP, DPOY) each season. Use this to find who won an award (winner), who received votes, and how close the voting was (pts_won, pts_max, share).",
    "All-Star Selections": "A simple log of every player selected for an All-Star game in a given season, including the team they represented.",
    "End of Season Teams": "Lists the players who were selected to honorary end-of-season teams, such as All-NBA, All-Defensive, and All-Rookie teams for each season.",
    "End of Season Teams (Voting)": "Provides the detailed voting results for the honorary end-of-season teams (All-NBA, etc.), showing the points and vote share each player received.",
    
    # Team Stat Tables
    "Team Summaries": "Contains a high-level summary of each team's performance for a given season. The best table for finding a team's record (wins 'w', losses 'l'), offensive rating (o_rtg), defensive rating (d_rtg), pace, and strength of schedule (sos).",
    "Team Stats Per Game": "Contains team-level statistics averaged per game for a season, such as points per game, rebounds per game, and assists per game for the entire team.",
    "Team Totals": "Contains the total cumulative statistics for each team over an entire season. Useful for questions about total points, field goals made, etc., for the whole team.",
    "Team Stats Per 100 Poss": "Contains team-level statistics normalized per 100 possessions. Ideal for comparing team performance while adjusting for pace.",
    
    # Opponent Stat Tables
    "Opponent Stats Per Game": "Shows the average statistics that a team's OPPONENTS recorded against them on a per-game basis. Use this to answer questions about a team's defense (e.g., 'which team allowed the fewest points per game?').",
    "Opponent Totals": "Shows the total cumulative statistics that a team's OPPONENTS recorded against them over a full season.",
    "Opponent Stats Per 100 Poss": "Opponent statistics normalized per 100 possessions, useful for analyzing a team's defensive performance adjusted for pace.",

    # Miscellaneous Tables
    "Draft Pick History": "Contains historical NBA draft data from every season. Use this to find where a player was drafted (overall_pick, round), by which team, and from what college.",
    "Player Play By Play": "Contains niche statistics derived from play-by-play logs, such as a player's on-court plus-minus per 100 possessions and the percentage of minutes they played at each position (pg_percent, c_percent).",
    "Player Season Info": "A simple utility table that links a player_id to their team, position, and years of experience for a specific season.",
    "Team Abbrev": "A utility table that maps a team's full name to its abbreviation for a given season."
}

EMBEDDINGS_FILE_PATH = "table_embeddings.npz"
credentials, project_id = google.auth.default()

def create_and_save_embeddings():
    """
    Generates embeddings for the table metadata and saves them to a file.
    """
    table_names = list(TABLE_METADATA.keys())
    descriptions = list(TABLE_METADATA.values())
    
    print(f"Generating embeddings for {len(descriptions)} tables...")
    
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        credentials=credentials,
        project=project_id 
    )

    embeddings = embeddings_model.embed_documents(descriptions)
    
    embeddings_array = np.array(embeddings)

    # Save both the table names and their embeddings to a single file
    np.savez_compressed(
        EMBEDDINGS_FILE_PATH,
        table_names=table_names,
        embeddings=embeddings_array
    )
    
    print(f"✅ Embeddings saved successfully to '{EMBEDDINGS_FILE_PATH}'")
    print(f"Shape of embeddings array: {embeddings_array.shape}")

if __name__ == "__main__":
    create_and_save_embeddings()