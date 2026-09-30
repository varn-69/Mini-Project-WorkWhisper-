"""Open Jobs Data source adapter."""
import pandas as pd
from typing import List, Dict
from .base import BaseJobSource
import os


class OpenJobsDataAdapter(BaseJobSource):
    """Adapter for the existing Open Jobs Data CSV dataset."""
    
    def __init__(self, csv_path: str = None):
        super().__init__()
        self.csv_path = csv_path or os.path.join(
            os.path.dirname(__file__),
            '../../../data/jobs_real.csv'
        )
    
    async def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from the local CSV file.
        
        Returns:
            List of raw job dictionaries
        """
        try:
            df = pd.read_csv(self.csv_path)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading Open Jobs Data CSV: {e}")
            return []
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize Open Jobs Data job to internal schema.
        
        Args:
            raw_job: Raw job from CSV
            
        Returns:
            Normalized job dictionary
        """
        return {
            'source_job_id': str(raw_job.get('job_id', '')),
            'job_title': raw_job.get('job_title', ''),
            'company': raw_job.get('company', ''),
            'skills': self._parse_skills(raw_job.get('skills', '')),
            'experience_required': float(raw_job.get('experience_required', 0)),
            'salary_min': float(raw_job.get('salary_min', 0)),
            'salary_max': float(raw_job.get('salary_max', 0)),
            'location': raw_job.get('location', ''),
            'education': raw_job.get('education', ''),
            'description': raw_job.get('description', ''),
            'source_url': None,  # CSV doesn't have source URLs
            'posted_at': None,  # CSV doesn't have posting dates
            'currency': 'USD',  # Default to USD for this dataset
        }
    
    def _parse_skills(self, skills_str: str) -> List[str]:
        """Parse skills from comma-separated string."""
        if not skills_str:
            return []
        return [skill.strip() for skill in skills_str.split(',') if skill.strip()]
