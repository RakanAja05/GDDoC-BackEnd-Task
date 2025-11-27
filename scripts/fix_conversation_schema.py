"""Small one-off migration to ensure conversation tables have the expected columns.

Run this script from the project root with the same Python interpreter you use
for the project (e.g. activate venv then `python scripts/fix_conversation_schema.py`).

It will:
- create the conversation tables if they don't exist
- inspect `conversation_messages` and add a `content` TEXT column if missing (SQLite `ALTER TABLE ADD COLUMN`)
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import DATABASE_URL
from app.db import Base, engine


def main():
    print("Using DATABASE_URL:", DATABASE_URL)

    # ensure tables exist (will create tables according to current models)
    print("Creating missing tables (if any)...")
    Base.metadata.create_all(bind=engine)

    # only attempt ALTER TABLE on SQLite
    if DATABASE_URL.startswith("sqlite"):
        try:
            with engine.connect() as conn:
                # check if column exists
                res = conn.execute(text("PRAGMA table_info('conversation_messages')"))
                cols = [row[1] for row in res.fetchall()]
                print("conversation_messages columns:", cols)
                if 'content' not in cols:
                    print("Adding missing 'content' column to conversation_messages...")
                    conn.execute(text("ALTER TABLE conversation_messages ADD COLUMN content TEXT"))
                    print("Added column.")
                else:
                    print("'content' column already present. No change needed.")
        except Exception as e:
            print("Error while altering table:", e)
            sys.exit(2)
    else:
        print("DATABASE_URL is not SQLite. If using another DB, apply an appropriate migration manually.")


if __name__ == '__main__':
    main()
