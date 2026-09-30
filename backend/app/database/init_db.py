from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.database.models import Base, Job
import pandas as pd
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def init_database():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


def seed_jobs_from_csv(csv_path: str):
    """Seed jobs table from CSV file."""
    df = pd.read_csv(csv_path)

    db = SessionLocal()
    try:
        # Clear existing jobs
        db.query(Job).delete()

        # Add jobs from CSV
        for _, row in df.iterrows():
            # Parse skills if they're a string
            skills = row['skills']
            if isinstance(skills, str):
                # Simple parsing - in production, use the preprocess.py function
                skills = [s.strip() for s in skills.split(',')]

            job = Job(
                job_title=row['job_title'],
                company=row['company'],
                skills=skills,
                experience_required=float(row.get('experience_required', 0)),
                salary_min=float(row.get('salary_min', 0)),
                salary_max=float(row.get('salary_max', 0)),
                location=row.get('location', ''),
                education=row.get('education', ''),
                description=row.get('description', ''),
                source='open_jobs_data',
                source_job_id=str(row.get('job_id', '')),
                source_url=None,
                posted_at=None,
                fetched_at=datetime.utcnow(),
                currency='USD',
                is_active=True
            )
            db.add(job)

        db.commit()
        print(f"Seeded {len(df)} jobs from {csv_path}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding jobs: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database
    init_database()

    # Seed jobs from CSV
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'jobs_real.csv')
    if os.path.exists(csv_path):
        seed_jobs_from_csv(csv_path)
    else:
        print(f"CSV file not found: {csv_path}")
