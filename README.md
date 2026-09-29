# Machine Learning System – Data Collection & Market Intelligence

## Milestone 1

This project implements:

1. Project submission form
2. PostgreSQL storage
3. Market analysis
4. Competitor landscape
5. Dashboard UI

## Step 1 – Install Python

Check:

```bash
python --version
```

## Step 2 – Create virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

## Step 3 – Install packages

```bash
pip install -r requirements.txt
```

## Step 4 – Create PostgreSQL database

Open pgAdmin 4.

Create database:

`ml_project`

Then open Query Tool for `ml_project` and run the `CREATE TABLE` statement from `database.sql`.

## Step 5 – Set PostgreSQL password

Open:

`database.py`

Change:

`YOUR_POSTGRES_PASSWORD`

to the password created during PostgreSQL installation.

## Step 6 – Run

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## Project flow

Project Input
-> Flask
-> PostgreSQL
-> Market Analysis
-> Competitor Analysis
-> Dashboard

## Milestone 2

Risk scoring, SWOT analysis and feasibility assessment can be added later.
