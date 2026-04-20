from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for job_skills
job_skills = Table(
    'job_skills',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String)
    location = Column(String)
    salary_min = Column(Numeric)
    salary_max = Column(Numeric)
    description = Column(Text)
    posted_at = Column(DateTime)
    source_url = Column(String, unique=True, nullable=False)
    
    skills = relationship("Skill", secondary=job_skills, back_populates="jobs")

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    jobs = relationship("Job", secondary=job_skills, back_populates="skills")
