from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from typing import List, Optional

import schemas

app = FastAPI(title="Job Market Skills Trend API")

# ---------------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------------
_explicit_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://job-market-analyzer-iota.vercel.app",
]
_frontend_url = os.getenv("FRONTEND_URL", "").strip()
if _frontend_url:
    _explicit_origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_explicit_origins,
    allow_origin_regex=r"https?://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Job Market Skills Trend API is running"}

# ---------------------------------------------------------------------------
# Static / hardcoded data
# ---------------------------------------------------------------------------

_TRENDING_SKILLS = [
    {"name": "Python",      "count": 45},
    {"name": "JavaScript",  "count": 38},
    {"name": "React",       "count": 32},
    {"name": "PostgreSQL",  "count": 28},
    {"name": "Docker",      "count": 25},
    {"name": "AWS",         "count": 22},
    {"name": "Node.js",     "count": 20},
    {"name": "TypeScript",  "count": 18},
    {"name": "FastAPI",     "count": 15},
    {"name": "Tailwind",    "count": 12},
    {"name": "Kubernetes",  "count": 10},
    {"name": "GraphQL",     "count":  9},
]

_SKILL_TREND = [
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
    {"month": "2024-04", "count": 50},
]

_COOCCURRENCE = [
    {"skill_a": "Python",     "skill_b": "SQL",        "count": 30},
    {"skill_a": "React",      "skill_b": "TypeScript",  "count": 25},
    {"skill_a": "Docker",     "skill_b": "Kubernetes",  "count": 20},
    {"skill_a": "Node.js",    "skill_b": "Express",     "count": 18},
    {"skill_a": "FastAPI",    "skill_b": "PostgreSQL",  "count": 15},
    {"skill_a": "Python",     "skill_b": "Docker",      "count": 14},
    {"skill_a": "AWS",        "skill_b": "Docker",      "count": 12},
    {"skill_a": "JavaScript", "skill_b": "React",       "count": 11},
    {"skill_a": "Python",     "skill_b": "FastAPI",     "count": 10},
    {"skill_a": "AWS",        "skill_b": "Kubernetes",  "count":  9},
]

_JOBS = [
    {
        "id": 1,
        "title": "Senior Backend Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "salary_min": None,
        "salary_max": None,
        "description": "Build scalable APIs with Python and FastAPI.",
        "posted_at": datetime(2026, 4, 20),
        "source_url": "https://example.com/job1",
        "skills": [{"id": 1, "name": "Python"}, {"id": 2, "name": "FastAPI"}],
    },
    {
        "id": 2,
        "title": "Frontend Architect",
        "company": "WebFlow",
        "location": "New York, NY",
        "salary_min": None,
        "salary_max": None,
        "description": "Lead the frontend team building React applications.",
        "posted_at": datetime(2026, 4, 19),
        "source_url": "https://example.com/job2",
        "skills": [{"id": 3, "name": "React"}, {"id": 4, "name": "TypeScript"}],
    },
    {
        "id": 3,
        "title": "DevOps Engineer",
        "company": "CloudScale",
        "location": "Remote",
        "salary_min": None,
        "salary_max": None,
        "description": "Manage Kubernetes clusters and CI/CD pipelines.",
        "posted_at": datetime(2026, 4, 18),
        "source_url": "https://example.com/job3",
        "skills": [{"id": 5, "name": "Docker"}, {"id": 6, "name": "Kubernetes"}],
    },
    {
        "id": 4,
        "title": "Data Engineer",
        "company": "DataStream",
        "location": "Remote",
        "salary_min": None,
        "salary_max": None,
        "description": "Design data pipelines using Python and PostgreSQL.",
        "posted_at": datetime(2026, 4, 17),
        "source_url": "https://example.com/job4",
        "skills": [{"id": 1, "name": "Python"}, {"id": 7, "name": "PostgreSQL"}],
    },
    {
        "id": 5,
        "title": "Full Stack Developer",
        "company": "Startup Labs",
        "location": "San Francisco, CA",
        "salary_min": None,
        "salary_max": None,
        "description": "Build end-to-end features across React and Node.js.",
        "posted_at": datetime(2026, 4, 16),
        "source_url": "https://example.com/job5",
        "skills": [{"id": 3, "name": "React"}, {"id": 8, "name": "Node.js"}],
    },
]

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/stats", response_model=schemas.SummaryStats)
def get_stats():
    return schemas.SummaryStats(
        total_jobs=148,
        total_companies=51,
        date_range="2026-04-01 to 2026-04-23",
        top_role="Software Engineer",
    )


@app.get("/skills/trending", response_model=List[schemas.TrendingSkill])
def get_trending_skills(
    role: Optional[str] = None,
    location: Optional[str] = None,
    days: int = 30,
):
    return _TRENDING_SKILLS


@app.get("/skills/trend", response_model=List[schemas.SkillTrend])
def get_skill_trend(
    skill: str,
    role: Optional[str] = None,
    location: Optional[str] = None,
):
    return _SKILL_TREND


@app.get("/skills/cooccurrence", response_model=List[schemas.Cooccurrence])
def get_cooccurrence():
    return _COOCCURRENCE


@app.get("/jobs", response_model=List[schemas.JobBase])
def get_jobs(
    page: int = 1,
    skill: Optional[str] = None,
    role: Optional[str] = None,
    location: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
):
    return _JOBS
