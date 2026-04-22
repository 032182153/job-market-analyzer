from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, desc
from datetime import datetime, timedelta
import os
import time
from typing import List, Optional

from api_database import get_db, engine
from api_models import Job, Skill, job_skills
import schemas

app = FastAPI(title="Job Market Skills Trend API")

# CORS Configuration
# Explicit origins (localhost dev + any custom production domain)
_explicit_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://job-market-analyzer-iota.vercel.app",
]
# Add FRONTEND_URL from env if set (e.g. https://your-app.vercel.app)
_frontend_url = os.getenv("FRONTEND_URL", "").strip()
if _frontend_url:
    _explicit_origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_explicit_origins,
    # Matches any Vercel preview/production deployment: *.vercel.app
    # Now explicitly supporting http and https for maximum flexibility
    allow_origin_regex=r"https?://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Job Market Skills Trend API is running"}

# Simple In-Memory Cache
class SimpleCache:
    def __init__(self, expire_seconds=3600):
        self.expire_seconds = expire_seconds
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.expire_seconds:
                return data
            else:
                del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

global_cache = SimpleCache()

@app.get("/skills/trending", response_model=List[schemas.TrendingSkill])
def get_trending_skills(
    role: Optional[str] = None,
    location: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    # HARDCODED TEST DATA
    return [
        {"name": "Python", "count": 45},
        {"name": "JavaScript", "count": 38},
        {"name": "React", "count": 32},
        {"name": "PostgreSQL", "count": 28},
        {"name": "Docker", "count": 25},
        {"name": "AWS", "count": 22},
        {"name": "Node.js", "count": 20},
        {"name": "TypeScript", "count": 18},
        {"name": "FastAPI", "count": 15},
        {"name": "Tailwind", "count": 12}
    ]

@app.get("/skills/trend", response_model=List[schemas.SkillTrend])
def get_skill_trend(
    skill: str,
    role: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # HARDCODED TEST DATA
    return [
        {"month": "2023-05", "count": 10},
        {"month": "2023-06", "count": 15},
        {"month": "2023-07", "count": 12},
        {"month": "2023-08", "count": 20},
        {"month": "2023-09", "count": 25},
        {"month": "2023-10", "count": 22},
        {"month": "2023-11", "count": 30},
        {"month": "2023-12", "count": 35},
        {"month": "2024-01", "count": 40},
        {"month": "2024-02", "count": 38},
        {"month": "2024-03", "count": 45},
        {"month": "2024-04", "count": 50}
    ]

@app.get("/skills/cooccurrence", response_model=List[schemas.Cooccurrence])
def get_cooccurrence(db: Session = Depends(get_db)):
    # HARDCODED TEST DATA
    return [
        {"skill_a": "Python", "skill_b": "SQL", "count": 30},
        {"skill_a": "React", "skill_b": "TypeScript", "count": 25},
        {"skill_a": "Docker", "skill_b": "Kubernetes", "count": 20},
        {"skill_a": "Node.js", "skill_b": "Express", "count": 18},
        {"skill_a": "FastAPI", "skill_b": "PostgreSQL", "count": 15}
    ]

@app.get("/jobs", response_model=List[schemas.JobBase])
def get_jobs(
    page: int = 1,
    skill: Optional[str] = None,
    role: Optional[str] = None,
    location: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # HARDCODED TEST DATA
    return [
        {
            "id": 1, 
            "title": "Senior Backend Engineer", 
            "company": "TechCorp", 
            "location": "Remote", 
            "posted_at": datetime.now(), 
            "url": "https://example.com/job1"
        },
        {
            "id": 2, 
            "title": "Frontend Architect", 
            "company": "WebFlow", 
            "location": "New York", 
            "posted_at": datetime.now(), 
            "url": "https://example.com/job2"
        },
        {
            "id": 3, 
            "title": "DevOps Engineer", 
            "company": "CloudScale", 
            "location": "Remote", 
            "posted_at": datetime.now(), 
            "url": "https://example.com/job3"
        }
    ]

@app.get("/stats", response_model=schemas.SummaryStats)
def get_stats(db: Session = Depends(get_db)):
    # HARDCODED TEST DATA
    return schemas.SummaryStats(
        total_jobs=148,
        total_companies=51,
        date_range="2026-04-01 to 2026-04-23",
        top_role="Software Engineer"
    )
