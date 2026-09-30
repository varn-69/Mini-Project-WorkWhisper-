from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./job_recommendation.db"
    openai_api_key: str = ""
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173"
    
    # Optional job source API keys
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    jooble_api_key: str = ""
    usajobs_api_key: str = ""
    usajobs_email: str = ""

    class Config:
        env_file = ".env"


settings = Settings()


# Scoring weights - these are initial project weights and can be tuned
SCORING_WEIGHTS = {
    "skill": 0.50,
    "experience": 0.20,
    "location": 0.10,
    "salary": 0.10,
    "education": 0.10,
}

# Skill score composition
SKILL_SCORE_WEIGHTS = {
    "explicit_match": 0.70,
    "tfidf_similarity": 0.30,
}

# Recommendation settings
TOP_N_RECOMMENDATIONS = 10
