import sqlite3

def search_cards_by_name(query, db_path="mtg_collection.db"):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row  # Enable row access by column name
    cur = con.cursor()
    cur.execute("SELECT * FROM cards WHERE name LIKE ?", (f"%{query}%",))
    results = cur.fetchall()
    con.close()
    return results

if __name__ == "__main__":
    name = input("Search for card name: ")
    cards = search_cards_by_name(name)
    for card in cards:
        print(dict(card))  # Convert Row to dict for easier printing