from fastapi import FastAPI
from .db.session import init_db
from contextlib import asynccontextmanager
from .api import users, auth, posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="LinkedIn Analytics API", 
              description="A backend API for LinkedIn",
              lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def home():
    return {"msg": "Yo, what's up?"}