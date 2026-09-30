"""Job source manager for multi-source job ingestion."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .open_jobs_data import OpenJobsDataAdapter
from .adzuna import AdzunaAdapter
from .jooble import JoobleAdapter
from .usajobs import USAJobsAdapter
from ...database.models import Job


class JobSourceManager:
    """Manager for fetching and normalizing jobs from multiple sources."""
    
    def __init__(self):
        self.sources = [
            OpenJobsDataAdapter(),
            AdzunaAdapter(),
            JoobleAdapter(),
            USAJobsAdapter(),
        ]
    
    async def fetch_all_jobs(self) -> Dict[str, List[Dict]]:
        """
        Fetch jobs from all configured sources.
        
        Returns:
            Dictionary mapping source names to normalized job lists
        """
        results = {}
        
        for source in self.sources:
            try:
                print(f"Fetching jobs from {source.source_name}...")
                raw_jobs = await source.fetch_jobs()
                normalized_jobs = source.normalize(raw_jobs)
                results[source.source_name] = normalized_jobs
                print(f"Fetched {len(normalized_jobs)} jobs from {source.source_name}")
            except Exception as e:
                print(f"Error fetching from {source.source_name}: {e}")
                results[source.source_name] = []
        
        return results
    
    def deduplicate_jobs(self, all_jobs: List[Dict]) -> List[Dict]:
        """
        Deduplicate jobs across all sources.
        
        Args:
            all_jobs: List of all normalized jobs from all sources
            
        Returns:
            Deduplicated list of jobs
        """
        seen_keys = set()
        deduplicated = []
        
        for job in all_jobs:
            # Use the first source adapter to generate dedup key
            key = self.sources[0].get_deduplication_key(job)
            
            if key not in seen_keys:
                seen_keys.add(key)
                deduplicated.append(job)
            else:
                print(f"Skipping duplicate job: {key}")
        
        return deduplicated
    
    async def upsert_to_database(self, db: Session, jobs: List[Dict]) -> Dict[str, int]:
        """
        Upsert jobs into database (insert or update).
        
        Args:
            db: Database session
            jobs: List of normalized jobs
            
        Returns:
            Dictionary with counts: inserted, updated, skipped
        """
        inserted = 0
        updated = 0
        skipped = 0
        
        for job_data in jobs:
            try:
                # Check if job exists by source + source_job_id
                existing = db.query(Job).filter(
                    Job.source == job_data['source'],
                    Job.source_job_id == job_data['source_job_id']
                ).first()
                
                if existing:
                    # Update existing job
                    existing.job_title = job_data['job_title']
                    existing.company = job_data['company']
                    existing.skills = job_data['skills']
                    existing.experience_required = job_data['experience_required']
                    existing.salary_min = job_data['salary_min']
                    existing.salary_max = job_data['salary_max']
                    existing.location = job_data['location']
                    existing.education = job_data['education']
                    existing.description = job_data['description']
                    existing.source_url = job_data['source_url']
                    existing.posted_at = job_data.get('posted_at')
                    existing.fetched_at = datetime.utcnow()
                    existing.currency = job_data.get('currency', 'USD')
                    existing.is_active = True
                    updated += 1
                else:
                    # Insert new job
                    new_job = Job(
                        job_title=job_data['job_title'],
                        company=job_data['company'],
                        skills=job_data['skills'],
                        experience_required=job_data['experience_required'],
                        salary_min=job_data['salary_min'],
                        salary_max=job_data['salary_max'],
                        location=job_data['location'],
                        education=job_data['education'],
                        description=job_data['description'],
                        source=job_data['source'],
                        source_job_id=job_data['source_job_id'],
                        source_url=job_data.get('source_url'),
                        posted_at=job_data.get('posted_at'),
                        fetched_at=datetime.utcnow(),
                        currency=job_data.get('currency', 'USD'),
                        is_active=True
                    )
                    db.add(new_job)
                    inserted += 1
                    
            except Exception as e:
                print(f"Error upserting job {job_data.get('source_job_id')}: {e}")
                skipped += 1
        
        db.commit()
        
        return {
            'inserted': inserted,
            'updated': updated,
            'skipped': skipped
        }
    
    async def refresh_jobs(self, db: Session) -> Dict:
        """
        Complete refresh cycle: fetch, normalize, deduplicate, upsert.
        
        Args:
            db: Database session
            
        Returns:
            Summary dictionary with counts
        """
        print("Starting job refresh...")
        
        # Fetch from all sources
        source_results = await self.fetch_all_jobs()
        
        # Flatten all jobs
        all_jobs = []
        for source_name, jobs in source_results.items():
            all_jobs.extend(jobs)
        
        print(f"Total jobs fetched: {len(all_jobs)}")
        
        # Deduplicate
        deduplicated = self.deduplicate_jobs(all_jobs)
        print(f"After deduplication: {len(deduplicated)}")
        
        # Upsert to database
        db_results = await self.upsert_to_database(db, deduplicated)
        
        return {
            'sources': {k: len(v) for k, v in source_results.items()},
            'inserted': db_results['inserted'],
            'updated': db_results['updated'],
            'skipped': db_results['skipped'],
            'failed_sources': [k for k, v in source_results.items() if not v]
        }
