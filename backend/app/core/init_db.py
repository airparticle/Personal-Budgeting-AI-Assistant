from sqlalchemy import text
from app.core.database import engine, Base
from app.models.user import User
from app.models.transaction import Transaction
from app.models.goal import Goal


def init_db():
    """
    Create all tables in the database.
    This should only be run once during initial setup.
    """
    print("Creating database tables...")

    # Import all models before creating tables
    # This ensures all relationships are registered
    Base.metadata.create_all(bind=engine)

    print("[SUCCESS] Database tables created successfully!")

    # Optional: Verify tables were created
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
        ))
        tables = [row[0] for row in result]
        print(f"[INFO] Created tables: {', '.join(tables)}")


if __name__ == "__main__":
    init_db()