import sqlite3

def initialize_db(db_path="mtg_collection.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # card fields can be adjusted as needed
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        scryfall_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        set_code TEXT,
        type_line TEXT,
        colors TEXT,
        oracle_text TEXT,
        rarity TEXT,
        cmc REAL,
        mana_cost TEXT
        -- can add more fields if desired!
    )
    """)
    con.commit()
    con.close()

    if __name__ == "__main__":
        initialize_db()
        print("Database and Tables initialized.")

# This script initializes the SQLite database for the MTG collection.
# Creates the mtg_collection.db in project root and a cards table.
# To run, execute this script directly or import the function in another script.