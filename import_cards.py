import sqlite3
import json
from tqdm import tqdm

DB_PATH = "mtg_collection.db"
JSON_PATH = "oracle-cards.json"

def insert_card(cur, card):
    """Insert a card into the cards table."""
    cur.execute("""
        INSERT OR REPLACE INTO cards (
            id, oracle_id, name, "set", collector_number, lang,
            layout, released_at, mana_cost, cmc, type_line,
            oracle_text, flavor_text, power, toughness, loyalty, defense, rarity, colors, color_identity,
            keywords, produced_mana, edhrec_rank, penny_rank, reserved, is_story_spotlight, hand_modifier, life_modifier,
            artist, border_color, frame, frame_effects, full_art,
            promo, promo_types, variation, finishes, oversized, textless, reprint, set_name, set_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            card["id"],
            card.get("oracle_id"),
            card["name"],
            card["set"],
            card.get("collector_number"),
            card.get("lang", "en"),
            card.get("layout"),
            card.get("released_at"),
            card.get("mana_cost", ""),
            card.get("cmc", 0),
            card.get("type_line"),
            card.get("oracle_text", ""),
            card.get("flavor_text"),
            card.get("power"),
            card.get("toughness"),
            card.get("loyalty"),
            card.get("defense"),
            card.get("rarity"),
            ",".join(card.get("colors", [])) if card.get("colors") else "",
            ",".join(card.get("color_identity", [])) if card.get("color_identity") else "",
            ",".join(card.get("keywords", [])) if card.get("keywords") else "",
            ",".join(card.get("produced_mana", [])) if card.get("produced_mana") else "",
            card.get("edhrec_rank"),
            card.get("penny_rank"),
            int(card.get("reserved", False)),
            int(card.get("is_story_spotlight", False)), # Corrected key from 'story_spotlight'
            card.get("hand_modifier"),
            card.get("life_modifier"),
            card.get("artist"),
            card.get("border_color"),
            card.get("frame"),
            ",".join(card.get("frame_effects", [])) if card.get("frame_effects") else "",
            int(card.get("full_art", False)),
            int(card.get("promo", False)),
            ",".join(card.get("promo_types", [])) if card.get("promo_types") else "",
            int(card.get("variation", False)),
            ",".join(card.get("finishes", [])) if card.get("finishes") else "",
            int(card.get("oversized", False)),
            int(card.get("textless", False)),
            int(card.get("reprint", False)),
            card.get("set_name"),
            card.get("set_type"),
        )
    )

def insert_card_faces(cur, card_id, faces):
    """Insert card faces for multiface cards."""
    for idx, face in enumerate(faces):
        cur.execute("""
            INSERT OR REPLACE INTO card_faces (
                card_id, face_index, name, mana_cost,
                type_line, oracle_text, flavor_text, power, toughness, defense,
                loyalty, colors, color_indicator, artist, illustration_id, watermark
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                card_id,
                idx,
                face.get("name"),
                face.get("mana_cost", ""),
                face.get("type_line"),
                face.get("oracle_text", ""),
                face.get("flavor_text"),
                face.get("power"),
                face.get("toughness"),
                face.get("defense"),
                face.get("loyalty"),
                ",".join(face.get("colors", [])) if face.get("colors") else "",
                ",".join(face.get("color_indicator", [])) if face.get("color_indicator") else "",
                face.get("artist"),
                face.get("illustration_id"),
                face.get("watermark")
            )
        )

def import_cards():
    """Load all card data from oracle-cards.json into the database."""
    print("Loading Scryfall card data...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for card in tqdm(cards, desc="Importing cards"):
        insert_card(cur, card)
        # Handle multi-faced cards (split, transform, etc)
        card_faces = card.get("card_faces")
        if card_faces:
            insert_card_faces(cur, card["id"], card_faces)

    con.commit()
    con.close()
    print(f"Imported {len(cards)} cards.")

if __name__ == "__main__":
    import_cards()