CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    description TEXT,
    posted_at TIMESTAMP,
    source_url TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);

-- Pre-populate skills
INSERT INTO skills (name) VALUES 
('Python'), ('JavaScript'), ('TypeScript'), ('React'), ('Node.js'), 
('SQL'), ('PostgreSQL'), ('MongoDB'), ('Docker'), ('Kubernetes'), 
('AWS'), ('GCP'), ('Azure'), ('FastAPI'), ('Django'), ('Flask'), 
('Spark'), ('Kafka'), ('Airflow'), ('dbt'), ('Terraform'), ('Git'), 
('GraphQL'), ('REST'), ('Redis'), ('Elasticsearch'), ('Pandas'), 
('NumPy'), ('PyTorch'), ('TensorFlow'), ('Scikit-learn')
ON CONFLICT (name) DO NOTHING;
