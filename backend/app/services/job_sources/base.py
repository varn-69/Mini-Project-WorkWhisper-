"""Base source adapter for job data ingestion."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class BaseJobSource(ABC):
    """Abstract base class for job source adapters."""
    
    def __init__(self):
        class_name = self.__class__.__name__.replace('Adapter', '')
        # Convert CamelCase to snake_case
        import re
        self.source_name = re.sub('([A-Z]+)', r'_\1', class_name).lower().lstrip('_')
    
    @abstractmethod
    async def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from the source.
        
        Returns:
            List of raw job dictionaries from the source
        """
        pass
    
    @abstractmethod
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize a raw job from the source to the internal schema.
        
        Args:
            raw_job: Raw job dictionary from source
            
        Returns:
            Normalized job dictionary with internal schema
        """
        pass
    
    def normalize(self, raw_jobs: List[Dict]) -> List[Dict]:
        """
        Normalize all jobs from the source.
        
        Args:
            raw_jobs: List of raw job dictionaries
            
        Returns:
            List of normalized job dictionaries
        """
        normalized = []
        for raw_job in raw_jobs:
            try:
                job = self.normalize_job(raw_job)
                job['source'] = self.source_name
                job['fetched_at'] = datetime.utcnow().isoformat()
                normalized.append(job)
            except Exception as e:
                print(f"Error normalizing job from {self.source_name}: {e}")
                continue
        return normalized
    
    def get_deduplication_key(self, job: Dict) -> str:
        """
        Generate a deduplication key for a job.
        
        Args:
            job: Normalized job dictionary
            
        Returns:
            String key for deduplication
        """
        # Prefer source + source_job_id
        if job.get('source_job_id'):
            return f"{job['source']}:{job['source_job_id']}"
        
        # Fallback to normalized URL
        if job.get('source_url'):
            from urllib.parse import urlparse
            parsed = urlparse(job['source_url'])
            return parsed.path.lower()
        
        # Final fallback: company + title + location
        return f"{job['company'].lower()}:{job['job_title'].lower()}:{job['location'].lower()}"
