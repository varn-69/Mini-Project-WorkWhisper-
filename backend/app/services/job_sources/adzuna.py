"""Adzuna API source adapter."""
import os
import httpx
from typing import List, Dict
from .base import BaseJobSource


class AdzunaAdapter(BaseJobSource):
    """Adapter for Adzuna job API."""
    
    def __init__(self, app_id: str = None, app_key: str = None):
        super().__init__()
        self.app_id = app_id or os.getenv('ADZUNA_APP_ID')
        self.app_key = app_key or os.getenv('ADZUNA_APP_KEY')
        self.base_url = "http://api.adzuna.com/v1/api/jobs"
        self.country = "us"  # Default to US
    
    async def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from Adzuna API.
        
        Returns:
            List of raw job dictionaries
        """
        if not self.app_id or not self.app_key:
            print("Adzuna credentials not configured, skipping")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                # Fetch a sample of jobs (limit to 100 for this demo)
                params = {
                    'app_id': self.app_id,
                    'app_key': self.app_key,
                    'content-type': 'application/json',
                    'what': 'software engineer',  # Default search term
                    'where': 'us',  # Default location
                    'limit': 100,
                }
                
                response = await client.get(
                    f"{self.base_url}/{self.country}/search/1",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                return data.get('results', [])
                
        except Exception as e:
            print(f"Error fetching jobs from Adzuna: {e}")
            return []
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize Adzuna job to internal schema.
        
        Args:
            raw_job: Raw job from Adzuna API
            
        Returns:
            Normalized job dictionary
        """
        # Extract salary from Adzuna format
        salary_min = 0
        salary_max = 0
        currency = 'USD'
        
        if raw_job.get('salary_min'):
            salary_min = float(raw_job['salary_min'])
        if raw_job.get('salary_max'):
            salary_max = float(raw_job['salary_max'])
        if raw_job.get('salary_currency'):
            currency = raw_job['salary_currency']
        
        # Parse skills from description (Adzuna doesn't provide explicit skills)
        skills = self._extract_skills_from_description(
            raw_job.get('description', ''),
            raw_job.get('title', '')
        )
        
        return {
            'source_job_id': str(raw_job.get('id', '')),
            'job_title': raw_job.get('title', ''),
            'company': raw_job.get('company', {}).get('display_name', ''),
            'skills': skills,
            'experience_required': self._extract_experience(raw_job.get('description', '')),
            'salary_min': salary_min,
            'salary_max': salary_max,
            'location': raw_job.get('location', {}).get('display_name', ''),
            'education': self._extract_education(raw_job.get('description', '')),
            'description': raw_job.get('description', ''),
            'source_url': raw_job.get('redirect_url', ''),
            'posted_at': raw_job.get('created'),
            'currency': currency,
        }
    
    def _extract_skills_from_description(self, description: str, title: str) -> List[str]:
        """Extract skills from job description and title."""
        # Simple keyword-based extraction
        # In production, this would use NLP or a skills database
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'fastapi', 'sql', 'nosql',
            'mongodb', 'postgresql', 'mysql', 'git', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'machine learning', 'data science',
            'typescript', 'go', 'rust', 'c++', 'java', 'spring',
            'linux', 'agile', 'scrum', 'devops', 'ci/cd', 'jenkins'
        ]
        
        text = f"{title} {description}".lower()
        found_skills = []
        
        for keyword in tech_keywords:
            if keyword in text:
                found_skills.append(keyword.title())
        
        return found_skills
    
    def _extract_experience(self, description: str) -> float:
        """Extract experience requirement from description."""
        # Simple heuristic - in production, use NLP
        description_lower = description.lower()
        
        if 'senior' in description_lower:
            return 5.0
        elif 'lead' in description_lower or 'principal' in description_lower:
            return 7.0
        elif 'junior' in description_lower or 'entry' in description_lower:
            return 1.0
        elif 'intern' in description_lower:
            return 0.0
        elif 'mid' in description_lower:
            return 3.0
        
        return 3.0  # Default
    
    def _extract_education(self, description: str) -> str:
        """Extract education requirement from description."""
        description_lower = description.lower()
        
        if 'phd' in description_lower or 'doctorate' in description_lower:
            return "PhD"
        elif 'master' in description_lower or 'mba' in description_lower:
            return "Master's"
        elif 'bachelor' in description_lower or 'bs' in description_lower or 'ba' in description_lower:
            return "Bachelor's"
        
        return "Not specified"
