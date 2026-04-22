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
    cache_key = f"trending_{role}_{location}_{days}"
    cached = global_cache.get(cache_key)
    if cached: return cached

    since_date = datetime.now() - timedelta(days=days)
    
    query = db.query(Skill.name, func.count(job_skills.c.job_id).label('count'))\
        .join(job_skills, Skill.id == job_skills.c.skill_id)\
        .join(Job, Job.id == job_skills.c.job_id)\
        .filter(Job.posted_at >= since_date)

    if role:
        query = query.filter(Job.title.ilike(f"%{role}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    results = query.group_by(Skill.name).order_by(desc('count')).limit(20).all()
    
    response = [{"name": r.name, "count": r.count} for r in results]
    global_cache.set(cache_key, response)
    return response

@app.get("/skills/trend", response_model=List[schemas.SkillTrend])
def get_skill_trend(
    skill: str,
    role: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    cache_key = f"trend_{skill}_{role}_{location}"
    cached = global_cache.get(cache_key)
    if cached: return cached

    # Last 12 months
    start_date = datetime.now() - timedelta(days=365)
    
    query = db.query(
        func.to_char(Job.posted_at, 'YYYY-MM').label('month'),
        func.count(Job.id).label('count')
    ).join(job_skills)\
     .join(Skill)\
     .filter(Skill.name.ilike(skill))\
     .filter(Job.posted_at >= start_date)

    if role:
        query = query.filter(Job.title.ilike(f"%{role}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    results = query.group_by('month').order_by('month').all()
    
    response = [{"month": r.month, "count": r.count} for r in results]
    global_cache.set(cache_key, response)
    return response

@app.get("/skills/cooccurrence", response_model=List[schemas.Cooccurrence])
def get_cooccurrence(db: Session = Depends(get_db)):
    cache_key = "cooccurrence"
    cached = global_cache.get(cache_key)
    if cached: return cached

    # Join job_skills with itself to find pairs
    js1 = job_skills.alias("js1")
    js2 = job_skills.alias("js2")
    s1 = Skill.__table__.alias("s1")
    s2 = Skill.__table__.alias("s2")

    query = db.query(
        s1.c.name.label('skill_a'),
        s2.c.name.label('skill_b'),
        func.count(js1.c.job_id).label('count')
    ).join(js2, js1.c.job_id == js2.c.job_id)\
     .join(s1, js1.c.skill_id == s1.c.id)\
     .join(s2, js2.c.skill_id == s2.c.id)\
     .filter(s1.c.name < s2.c.name)\
     .group_by(s1.c.name, s2.c.name)\
     .order_by(desc('count'))\
     .limit(100) # Limit to top co-occurrences for performance

    results = query.all()
    response = [{"skill_a": r.skill_a, "skill_b": r.skill_b, "count": r.count} for r in results]
    global_cache.set(cache_key, response)
    return response

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
    offset = (page - 1) * 20
    query = db.query(Job)

    if skill:
        query = query.join(job_skills).join(Skill).filter(Skill.name.ilike(skill))
    if role:
        query = query.filter(Job.title.ilike(f"%{role}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if date_from:
        query = query.filter(Job.posted_at >= date_from)
    if date_to:
        query = query.filter(Job.posted_at <= date_to)

    results = query.order_by(desc(Job.posted_at)).offset(offset).limit(20).all()
    return results

@app.get("/stats", response_model=schemas.SummaryStats)
def get_stats(db: Session = Depends(get_db)):
    cache_key = "stats"
    cached = global_cache.get(cache_key)
    if cached: return cached

    total_jobs = db.query(func.count(Job.id)).scalar()
    total_companies = db.query(func.count(func.distinct(Job.company))).scalar()
    
    date_range_res = db.query(func.min(Job.posted_at), func.max(Job.posted_at)).first()
    date_range = f"{date_range_res[0].date()} to {date_range_res[1].date()}" if date_range_res[0] else "N/A"
    
    top_role_res = db.query(Job.title, func.count(Job.id).label('count'))\
        .group_by(Job.title).order_by(desc('count')).first()
    top_role = top_role_res.title if top_role_res else "N/A"

    response = schemas.SummaryStats(
        total_jobs=total_jobs,
        total_companies=total_companies,
        date_range=date_range,
        top_role=top_role
    )
    global_cache.set(cache_key, response)
    return response
