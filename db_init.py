import sqlite3

def initialize_db(db_path="mtg_collection.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # --- CARDS Table ---
    # Contains all Scryfall cards you import. Only 1 row per print/edition.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id TEXT PRIMARY KEY,                 -- Scryfall card UUID (unique per print)
        oracle_id TEXT,                      -- Links reprints of the same card
        name TEXT,                           -- Composite name for double-faced cards (ex: 'Fire // Ice')
        "set" TEXT,                            -- Set code
        collector_number TEXT,               -- Human-readable collector number
        lang TEXT,                           -- Language code
        layout TEXT,                         -- Card layout (normal, split, transform, etc.)
        released_at TEXT,                    -- Release date (ISO string)
        mana_cost TEXT,                      -- May be "{2}{G}{G}" or ""; can render text-only in TUI
        cmc REAL,                            -- Mana value (as float, supports half pips)
        type_line TEXT,
        oracle_text TEXT,                    -- Card rules text (may have {T}, {R}, etc. for symbols)
        flavor_text TEXT,
        power TEXT,
        toughness TEXT,
        loyalty TEXT,
        defense TEXT,
        rarity TEXT,                         -- common, uncommon, rare, mythic, etc.
        colors TEXT,                         -- comma-joined, e.g. "R,G,B"
        color_identity TEXT,                 -- comma-joined like above
        keywords TEXT,                       -- comma-joined for simple search/filter
        produced_mana TEXT,                  -- comma-joined if card can produce mana
        edhrec_rank INTEGER,                 -- popularity on EDHRec
        penny_rank INTEGER,                  -- popularity on Penny Dreadful
        reserved BOOLEAN,                    -- Reserved List
        is_story_spotlight BOOLEAN,
        hand_modifier TEXT,
        life_modifier TEXT,

        -- Print-identity fields
        artist TEXT,
        border_color TEXT,
        frame TEXT,
        frame_effects TEXT,                  -- comma-joined
        full_art BOOLEAN,
        promo BOOLEAN,
        promo_types TEXT,                    -- comma-joined
        variation BOOLEAN,
        finishes TEXT,                       -- comma-joined: foil/nonfoil/etched
        oversized BOOLEAN,
        textless BOOLEAN,
        reprint BOOLEAN,
        set_name TEXT,
        set_type TEXT,

        UNIQUE(id)
    );
    """)

    # --- CARD_FACES Table (optional, for multifaced cards) ---
    # If you want to allow your app to show preview/stats for individual faces of DFCs, you can normalize them here.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS card_faces (
        card_id TEXT,                  -- FK to cards.id
        face_index INTEGER,            -- 0 = front, 1 = back, etc.
        name TEXT,
        mana_cost TEXT,
        type_line TEXT,
        oracle_text TEXT,
        flavor_text TEXT,
        power TEXT,
        toughness TEXT,
        defense TEXT,
        loyalty TEXT,
        colors TEXT,
        color_indicator TEXT,
        artist TEXT,
        illustration_id TEXT,
        watermark TEXT,
        -- image_uris TEXT,             -- for image support (TUI: NOT NEEDED)
        PRIMARY KEY(card_id, face_index)
    );
    """)

    # --- USERS Table ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    """)

    # --- COLLECTIONS Table (users can have multiple collections) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,              -- "Main Collection", "Trade Binder", etc
        description TEXT,
        date_created TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # --- COLLECTION_CARDS Table (cards in each collection) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS collection_cards (
        collection_id INTEGER NOT NULL,
        card_id TEXT NOT NULL,           -- Scryfall print id (cards.id)
        quantity INTEGER NOT NULL DEFAULT 1,
        notes TEXT,                      -- For custom tags, or per-card notes
        PRIMARY KEY (collection_id, card_id),
        FOREIGN KEY(collection_id) REFERENCES collections(collection_id),
        FOREIGN KEY(card_id) REFERENCES cards(id)
    )
    """)

    # --- TAGS Table (optional, for custom tags per collection) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS card_tags (
        collection_id INTEGER,
        card_id TEXT,
        tag_id INTEGER,
        PRIMARY KEY(collection_id, card_id, tag_id),
        FOREIGN KEY(collection_id, card_id) REFERENCES collection_cards(collection_id, card_id),
        FOREIGN KEY(tag_id) REFERENCES tags(tag_id)
    )
    """)

    # --- DECKS Table (future: for deck building/management) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS decks (
        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        date_created TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deck_cards (
        deck_id INTEGER NOT NULL,
        card_id TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (deck_id, card_id),
        FOREIGN KEY(deck_id) REFERENCES decks(deck_id),
        FOREIGN KEY(card_id) REFERENCES cards(id)
    )
    """)

    # --- STATS Table (optional, but usually generated on the fly with SQL, not stored) ---
    # leave this table out; can use SQL to COUNT/AVG/ETC directly.
    # To store snapshots, add a stats table here later.

    con.commit()
    con.close()
    print("Database tables created or verified.")

if __name__ == "__main__":
    initialize_db()