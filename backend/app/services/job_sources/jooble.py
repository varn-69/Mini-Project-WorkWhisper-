"""Jooble API source adapter."""
import os
import httpx
from typing import List, Dict
from .base import BaseJobSource


class JoobleAdapter(BaseJobSource):
    """Adapter for Jooble job API."""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv('JOOBLE_API_KEY')
        self.base_url = "https://jooble.org/api"
    
    async def fetch_jobs(self) -> List[Dict]:
        """
        Fetch jobs from Jooble API.
        
        Returns:
            List of raw job dictionaries
        """
        if not self.api_key:
            print("Jooble API key not configured, skipping")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    'apiKey': self.api_key,
                    'keywords': 'software engineer',  # Default search
                    'location': 'us',  # Default location
                    'limit': 100,
                }
                
                response = await client.get(
                    f"{self.base_url}/{self.api_key}",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                return data.get('jobs', [])
                
        except Exception as e:
            print(f"Error fetching jobs from Jooble: {e}")
            return []
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize Jooble job to internal schema.
        
        Args:
            raw_job: Raw job from Jooble API
            
        Returns:
            Normalized job dictionary
        """
        # Parse salary from Jooble format (often in description)
        salary_min = 0
        salary_max = 0
        currency = 'USD'
        
        if raw_job.get('salary'):
            salary_text = raw_job['salary']
            # Simple parsing - in production, use more robust parser
            if '$' in salary_text:
                # Extract numbers
                import re
                numbers = re.findall(r'\d+', salary_text.replace(',', ''))
                if numbers:
                    salary_min = float(numbers[0])
                    if len(numbers) > 1:
                        salary_max = float(numbers[1])
        
        # Extract skills from description
        skills = self._extract_skills_from_description(
            raw_job.get('description', ''),
            raw_job.get('title', '')
        )
        
        return {
            'source_job_id': str(raw_job.get('id', '')),
            'job_title': raw_job.get('title', ''),
            'company': raw_job.get('company', ''),
            'skills': skills,
            'experience_required': self._extract_experience(raw_job.get('description', '')),
            'salary_min': salary_min,
            'salary_max': salary_max,
            'location': raw_job.get('location', ''),
            'education': self._extract_education(raw_job.get('description', '')),
            'description': raw_job.get('description', ''),
            'source_url': raw_job.get('link', ''),
            'posted_at': raw_job.get('published'),
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
