"""Database migration script to add multi-source job fields."""
from sqlalchemy import text
from app.database.connection import engine


def migrate_database():
    """Add new columns for multi-source job ingestion."""
    
    # Add new columns if they don't exist
    migrations = [
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'open_jobs_data'
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS source_job_id VARCHAR(255)
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS source_url TEXT
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS posted_at TIMESTAMP
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'USD'
        """,
        """
        ALTER TABLE jobs 
        ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
        """,
    ]
    
    with engine.connect() as conn:
        for migration in migrations:
            try:
                conn.execute(text(migration))
                print(f"Migration successful: {migration[:50]}...")
            except Exception as e:
                print(f"Migration failed (may already exist): {e}")
    
    print("Database migration completed.")


if __name__ == "__main__":
    migrate_database()
