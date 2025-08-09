import sqlite3
import pandas as pd

DB_FILE = "rasoi.db"

def setup_database():
    """Creates the database and the recipes table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            region TEXT,
            story TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            photo_filename TEXT,
            upvotes INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_recipe(name, region, story, ingredients, instructions, photo_filename):
    """Adds a new recipe to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, region, story, ingredients, instructions, photo_filename) VALUES (?, ?, ?, ?, ?, ?)",
        (name, region, story, ingredients, instructions, photo_filename)
    )
    conn.commit()
    conn.close()

def get_all_recipes():
    """Fetches all recipes from the database, sorted by upvotes."""
    conn = sqlite3.connect(DB_FILE)
    # Use pandas to easily read the SQL query into a DataFrame
    df = pd.read_sql_query("SELECT * FROM recipes ORDER BY upvotes DESC", conn)
    conn.close()
    return df

def upvote_recipe(recipe_id):
    """Increments the upvote count for a specific recipe."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE recipes SET upvotes = upvotes + 1 WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
# Add this new function to your database.py file

def get_recipes_by_names(name_list):
    """Fetches full recipe details for a given list of recipe names."""
    if not name_list:
        return pd.DataFrame() # Return empty DataFrame if list is empty
        
    conn = sqlite3.connect(DB_FILE)
    # The '?' placeholders are parameterized to prevent SQL injection
    placeholders = ', '.join(['?'] * len(name_list))
    query = f"SELECT * FROM recipes WHERE name IN ({placeholders})"
    
    df = pd.read_sql_query(query, conn, params=name_list)
    conn.close()
    return df