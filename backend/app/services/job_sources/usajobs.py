"""USAJOBS API source adapter."""
import os
import httpx
from typing import List, Dict
from .base import BaseJobSource


class USAJobsAdapter(BaseJobSource):
    """Adapter for USAJOBS API (government jobs)."""
    
    def __init__(self, api_key: str = None, email: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv('USAJOBS_API_KEY')
        self.email = email or os.getenv('USAJOBS_EMAIL')
        self.base_url = "https://api.usajobs.gov/api/search"
    
    async def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from USAJOBS API.
        
        Returns:
            List of raw job dictionaries
        """
        if not self.api_key or not self.email:
            print("USAJOBS credentials not configured, skipping")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'Authorization-Key': self.api_key,
                    'User-Agent': self.email,
                }
                
                params = {
                    'Keyword': 'software engineer',  # Default search
                    'ResultsPerPage': 100,
                }
                
                response = await client.get(
                    self.base_url,
                    headers=headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                return data.get('SearchResult', {}).get('SearchResultItems', [])
                
        except Exception as e:
            print(f"Error fetching jobs from USAJOBS: {e}")
            return []
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize USAJOBS job to internal schema.
        
        Args:
            raw_job: Raw job from USAJOBS API
            
        Returns:
            Normalized job dictionary
        """
        # Parse salary from USAJOBS format
        salary_min = 0
        salary_max = 0
        currency = 'USD'
        
        salary_range = raw_job.get('SalaryRange', {})
        if salary_range:
            if salary_range.get('Minimum'):
                salary_min = float(salary_range['Minimum'])
            if salary_range.get('Maximum'):
                salary_max = float(salary_range['Maximum'])
            if salary_range.get('RateIntervalCode'):
                # Handle hourly/yearly conversion if needed
                pass
        
        # Extract skills from description
        skills = self._extract_skills_from_description(
            raw_job.get('JobSummary', ''),
            raw_job.get('JobTitle', '')
        )
        
        return {
            'source_job_id': str(raw_job.get('MatchObjectId', '')),
            'job_title': raw_job.get('JobTitle', ''),
            'company': raw_job.get('OrganizationName', ''),
            'skills': skills,
            'experience_required': self._extract_experience(raw_job.get('JobSummary', '')),
            'salary_min': salary_min,
            'salary_max': salary_max,
            'location': raw_job.get('Locations', [{}])[0].get('CityName', '') if raw_job.get('Locations') else '',
            'education': self._extract_education(raw_job.get('JobSummary', '')),
            'description': raw_job.get('JobSummary', ''),
            'source_url': raw_job.get('ApplyURI', [{}])[0].get('URI', '') if raw_job.get('ApplyURI') else '',
            'posted_at': raw_job.get('StartDate'),
            'currency': currency,
        }
    
    def _extract_skills_from_description(self, description: str, title: str) -> List[str]:
        """Extract skills from job description and title."""
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
        
        return 3.0
    
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
