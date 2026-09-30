from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import RecommendationRequest, RecommendationResponse, ExplainRequest, ExplainResponse
from app.ml.recommendation import RecommendationEngine
from app.services.llm_service import generate_explanation, generate_learning_roadmap
from app.database.connection import get_db
from app.database.models import Job
import pandas as pd

router = APIRouter()


def load_jobs_from_db(db: Session) -> pd.DataFrame:
    """Load jobs from database into DataFrame for recommendation engine."""
    jobs = db.query(Job).filter(Job.is_active == True).all()
    
    job_data = []
    for job in jobs:
        job_data.append({
            'job_id': job.job_id,
            'job_title': job.job_title,
            'company': job.company,
            'skills': job.skills,
            'experience_required': job.experience_required,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'location': job.location,
            'education': job.education,
            'description': job.description,
            'source': job.source,
            'source_url': job.source_url,
            'currency': job.currency,
        })
    
    return pd.DataFrame(job_data)


def get_recommendation_engine(db: Session) -> RecommendationEngine:
    """Get or create recommendation engine with current database data."""
    jobs_df = load_jobs_from_db(db)
    return RecommendationEngine(jobs_df)


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_jobs(request: RecommendationRequest, db: Session = Depends(get_db)):
    """Generate job recommendations for a candidate."""
    try:
        # Get recommendation engine with current data
        recommendation_engine = get_recommendation_engine(db)
        
        # Convert candidate profile to dict
        candidate_dict = request.candidate.model_dump()

        # Get recommendations
        recommendations = recommendation_engine.recommend_jobs(candidate_dict, top_n=10)

        return RecommendationResponse(
            recommendations=recommendations,
            candidate_name=request.candidate.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=ExplainResponse)
def explain_recommendation(request: ExplainRequest):
    """Generate an explanation and learning roadmap for a job recommendation."""
    try:
        # Convert to dicts
        candidate_dict = request.candidate_profile.model_dump()
        job_dict = request.job.model_dump()

        # Generate explanation
        explanation = generate_explanation(candidate_dict, job_dict)

        # Generate learning roadmap
        learning_roadmap = generate_learning_roadmap(candidate_dict, job_dict)

        return ExplainResponse(
            explanation=explanation,
            learning_roadmap=learning_roadmap
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
