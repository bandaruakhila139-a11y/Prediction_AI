CREATE DATABASE ml_project;

-- After creating the database, connect to ml_project and run:

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    startup_name VARCHAR(150) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    business_model VARCHAR(100) NOT NULL,
    target_market VARCHAR(150),
    budget NUMERIC(15,2),
    project_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
