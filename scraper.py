import requests
import logging
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SKILLS_LIST = [
    'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 
    'SQL', 'PostgreSQL', 'MongoDB', 'Docker', 'Kubernetes', 
    'AWS', 'GCP', 'Azure', 'FastAPI', 'Django', 'Flask', 
    'Spark', 'Kafka', 'Airflow', 'dbt', 'Terraform', 'Git', 
    'GraphQL', 'REST', 'Redis', 'Elasticsearch', 'Pandas', 
    'NumPy', 'PyTorch', 'TensorFlow', 'Scikit-learn'
]

def clean_html(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=' ')

def extract_skills(description):
    found_skills = []
    if not description:
        return found_skills
    
    # Simple regex search for skills
    for skill in SKILLS_LIST:
        # Match skill as a whole word, case insensitive
        # Need to handle special characters like .js (Node.js)
        # Escaping skill names for regex
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, description, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

def fetch_remoteok():
    logging.info("Fetching from RemoteOK...")
    url = "https://remoteok.com/api"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # remoteok returns a list where the first item is a legal notice
        jobs = []
        for item in data[1:]:
            description = clean_html(item.get('description', ''))
            job = {
                'title': item.get('position'),
                'company': item.get('company'),
                'location': item.get('location', 'Remote'),
                'salary_min': item.get('salary_min'),
                'salary_max': item.get('salary_max'),
                'description': description,
                'posted_at': item.get('date'),
                'source_url': item.get('url'),
                'skills': extract_skills(description)
            }
            jobs.append(job)
        return jobs
    except Exception as e:
        logging.error(f"Error fetching from RemoteOK: {e}")
        return []

def fetch_adzuna():
    logging.info("Fetching from Adzuna...")
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    country = os.getenv("ADZUNA_COUNTRY", "us")
    
    if not app_id or not app_key:
        logging.warning("Adzuna API credentials missing. Skipping Adzuna.")
        return []

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 50,
        'what': 'software engineer', # Narrow down to relevant jobs
        'content-type': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for item in data.get('results', []):
            description = clean_html(item.get('description', ''))
            job = {
                'title': item.get('title'),
                'company': item.get('company', {}).get('display_name'),
                'location': item.get('location', {}).get('display_name'),
                'salary_min': item.get('salary_min'),
                'salary_max': item.get('salary_max'),
                'description': description,
                'posted_at': item.get('created'),
                'source_url': item.get('redirect_url'),
                'skills': extract_skills(description)
            }
            jobs.append(job)
        return jobs
    except Exception as e:
        logging.error(f"Error fetching from Adzuna: {e}")
        return []
