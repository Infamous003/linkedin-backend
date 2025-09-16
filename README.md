# LinkedIn Backend (Take-Home Assignment)

A RESTful backend built with **FastAPI** and **PostgreSQL** implementing user authentication, user management, posts with scheduling, reactions, and basic post analytics.

## Features
- JWT authentication (register, login, etc)
- CRUD for Users (list, get by ID, update, delete)
- CRUD for Posts (create, list, get, update, delete)
- Post scheduling, impressions (count views), reactions
- Alembic migrations for PostgreSQL schema
- Postman collection with sample requests and data


## Configuration
Configuration is handled via `config.py` / environment variables.  
Default values:

```env
DB_USERNAME=postgres
DB_PASSWORD=password123
DB_NAME=linkedindb
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=this_is_a_secret
ALGORITHM=HS256
TOKEN_EXPIRATION_MINUTES=60
```

## Installation
```bash
git clone https://github.com/yourname/linkedin-backend.git
cd linkedin-backend
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

## Migrations and DB
- After creating the database and changing the .env file, run the alembic migrations
```bash
alembic upgrade head
```

## Start the app
```bash
uvicorn app.main:app --reload
```

**Interactive docs are available at:** http://localhost:8000/docs

## Postman Collection
You can import the Postman collection from the following URL:  
[Postman Collection Link](https://www.postman.com/just-me-3110/linkedin-analytics-api/collection/sz2hc98/api?action=share&creator=40067502)