# Product Requirements Document (PRD)
## Product Title
### AetherLab: Magic the Gathering Collection & Deck Manager (TUI)

## Purpose
To provide a robust, cross-platform, text user interface (TUI) application for physical Magic: The Gathering (MTG) card collection management supporting multiple users, offline Scryfall data, detailed searching/filtering, multi-collection and deck management, and full control over import/export and backup—all designed to be easily usable on Windows or Linux with minimal dependencies.

## Target Users
- Physical MTG card collectors and players (primarily self and gaming partner)
- Users wanting complete, local, private control over their card database and collections
- Users preferring keyboard-centric, terminal/console interfaces over GUIs or web apps

## Platforms
Windows (10+)
Linux (Ubuntu and compatible distros)
*(Optionally extensible to macOS)*
## Data & Storage
- Scryfall Bulk Data
- Source: oracle-cards.json Scryfall bulk data file (manually downloaded)
- **No live API calls, for data privacy and speed**
- Local Database
- Uses SQLite (mtg_collection.db) for all app data
- All card metadata, user accounts, collections, decks, tags, and logs persist in this DB
## Export/Import
Users may export/import their collections as JSON files for backup and migration purposes

# Major Features
1. **User Management**
Multiple users (hardcoded)
Per-user collections, decks, and session context
2. **Card Database**
All physical MTG cards from Scryfall’s oracle bulk file
No dependency on images, digital-only data, or marketplace links
Schema designed to capture all essential physical collection fields, including multiface cards
3. **Searching & Filtering**
Search cards by name, partial name, or advanced Scryfall-like SQL filtering
Filters by set, color, rarity, card type, mana cost, and more (expandable)
Instant search and keyboard navigation of results
4. **Collections**
Each user may have multiple named collections (e.g. “Main Binder”, “Trade”, etc.)
Easily view, search, filter, and sort collection content (TUI table/spreadsheet)
Add, edit, or remove card quantities
Custom notes and tags on any card in any collection
5. **Deck Management (Future-Ready)**
Each user can create named decks
Deck lists reference cards by Scryfall ID and version
Easy deck-editing and summary export (even if rudimentary at first, schema is ready)
6. **Undo and Logging**
Action log displayed persistently in TUI for user confidence/history
Undo last change stack for safety against mistakes
7. **Import/Export & Backup**
Export collection(s) as JSON for backup, re-import, or sharing
Ability to restore from a prior exported file
8. **Scryfall Data Updates**
Easy update tool to re-import latest Scryfall bulk data; never destroys collection/deck data—always merges or adds
9. **Multi-Face Card Support**
Handles both sides of double-faced cards, split, adventure, etc., with either a detail view or face/side browse
10. **Statistics**
Per-user and per-collection summary stats (total unique cards, by color, set, type, rarity, CMC curve, etc.)
Displayed in a dedicated stats window/popup
11. **Tags and Custom Notes**
Users can add/assign custom tags (e.g., “Commander”, “Trade”, “Signed”, etc.) to any card
Freeform notes field per card in a collection
12. **TUI/Terminal Interface**
- Modern, visually appealing terminal app (Textual/rich library)
- Keyboard-centric, mode-based navigation
- Two-panel layout—main data/work area, persistent action log window
- Context-aware help and soft-keyboard popups for all commands
- All common commands bound to hotkeys for ergonomic fast entry (see "User Flows" below)

### *Out of Scope (For Now)*
- Image/scan support or display of art
- Online syncing/cloud features (all local)
- Price/TCGplayer/market data (out of privacy and complexity concerns)
- Support for digital-only Magic cards
- Advanced migration/versioning (handled manually or with simple scripts as needed)

# Database Schema (Simplified)
**Summary:**

cards: All Scryfall printings (fields: id, name, set, type_line, mana_cost, cmc, oracle_text, rarity, etc.)

card_faces: Details for each face of multiface cards (card_id, face_index, face-specific fields)

users: id, username

collections: id, user_id, name, description, date_created

collection_cards: collection_id, card_id, quantity, notes

tags & card_tags: custom tagging system

decks & deck_cards: decklists for future expansion

## User Flows/Interactions (Overview)
- **Start Application:** Choose user (hardcoded or username entry)
- **Main Menu:** Modes for [Search], [Collection], [Decks], [Stats], [Export/Import], [DB Update]
- **Search Mode:** Keyboard entry for quick find, filter by card details, press hotkey to add card to a collection
- **Collections Mode:** Tabular view of collection, live filter/search, hotkey to edit/remove, select cards for actions, see summary info, use Undo as needed
- **Stats View:** Press hotkey to see printable stats for current collection/user (breakdown by color, type, etc.)
- **Decks Mode (future):** Select deck for editing, add/remove cards, view which cards are missing from collection
- **Export/Import:** menu for backup/restore, user confirms before overwriting anything
- **Log:** See most recent actions anytime at bottom of UI

## Implementation Stack
**Python 3.9+** (uses built-in sqlite3)
**SQLite** (no server, single-file db)
**Textual** (textual package) for TUI
**tqdm** for import progress
**pyinstaller** (optional, for easy distribution)
**No external DB/image/market dependencies**

## Requirements Table
Requirement	| Must	| Notes
--- | --- | ---
Search all cards by name, filter |	YES	| Full offline search
Add/remove cards from one or more collections	| YES	| Must track quantities, organize by user
Undo action, persistent log	| YES	| Extremely important for user trust
Hotkey-based data entry/navigation	| YES	| Keyboard-driven interface
Backup/export/import per user	| YES	| Critical for data portability and safety
TUI spreadsheet-style browsing	|YES	| Avoids menu clutter, supports table view
Update card database safely	| YES	| Must NOT lose user/collection/deck data
Stats window	| YES	| Per collection and/or user
Tagging/custom notes	| YES	| For flexible extra management
Support multiface cards	| YES	| At least enough details for preview, later full card_faces
Per-user, multi-collection support	| YES	
Deck support (future)	| YES	| Schema in place, UI can be added/extended

## Future Enhancements (Planned or "Nice-to-Have")
- Deck legality/highland count checking UI for decks
- Export to external deckbuilders (e.g. Moxfield)
- Price tracking (optional add-on via Scryfall API/local cache)
- Import from other collection formats (e.g. CSV)
- Automatic diff/check when updating Scryfall data to flag missing/renamed cards

## Non-Functional Requirements
Fast local search (matching Scryfall search feel)
Cross-platform (Windows/Linux)
No online/cloud dependency (privacy-first)
No data loss—even during schema changes or Scryfall updates
Security & Privacy
All data stored locally
No analytics, telemetry, or remote API calls

## Project Organization
AetherLab-Python/
  main.py
  db_init.py
  import_cards.py
  tui/                  # Textual app source
  oracle-cards.json   # gitignored; user-supplied Scryfall data
  mtg_collection.db
  requirements.txt
  README.md
Acceptance Criteria / Test Plan
Can add, remove, edit amounts of cards in a collection and see changes persistently
Can search and filter globally among all Scryfall cards
Can create and switch between users and collections
Undo stack and action log show correct events after each TUI action
Can backup and restore collection and user data via import/export
Can update/replace Scryfall bulk data with no loss to user data
Can use app on Windows or Linux terminals without issues
Appendix: Limitations
Does NOT display card art or use image-heavy features (ASCII only)
Does NOT track or display live prices/outside-market data
All inputs/fields are designed for standard 80+ column terminals but optimized for widescreen