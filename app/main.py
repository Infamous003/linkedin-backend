from fastapi import FastAPI
from .db.session import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="LinkedIn Analytics API", 
              description="A backend API for LinkedIn",
              lifespan=lifespan)

@app.get("/")
def home():
    return {"msg": "Yo, what's up?"}