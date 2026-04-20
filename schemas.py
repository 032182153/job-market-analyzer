from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class SkillBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class JobBase(BaseModel):
    id: int
    title: str
    company: Optional[str]
    location: Optional[str]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    description: Optional[str]
    posted_at: Optional[datetime]
    source_url: str
    skills: List[SkillBase] = []

    class Config:
        from_attributes = True

class TrendingSkill(BaseModel):
    name: str
    count: int

class SkillTrend(BaseModel):
    month: str
    count: int

class Cooccurrence(BaseModel):
    skill_a: str
    skill_b: str
    count: int

class SummaryStats(BaseModel):
    total_jobs: int
    total_companies: int
    date_range: str
    top_role: str
