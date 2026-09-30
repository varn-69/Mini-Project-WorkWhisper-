"""API endpoint for job refresh."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from ..database.connection import get_db
from ..services.job_sources import JobSourceManager

router = APIRouter()

job_manager = JobSourceManager()


@router.post("/refresh")
async def refresh_jobs(db: Session = Depends(get_db)) -> Dict:
    """
    Refresh jobs from all configured sources.
    
    This endpoint:
    - Fetches jobs from all configured sources (Open Jobs Data, Adzuna, Jooble, USAJOBS)
    - Normalizes jobs to internal schema
    - Deduplicates across sources
    - Upserts to PostgreSQL
    
    Returns:
        Summary dictionary with counts
    """
    try:
        result = await job_manager.refresh_jobs(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job refresh failed: {str(e)}")
