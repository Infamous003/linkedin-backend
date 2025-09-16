from fastapi import FastAPI
from .db.session import init_db
from contextlib import asynccontextmanager
from .api import users, auth, posts, analytics
from apscheduler.schedulers.background import BackgroundScheduler
from .core.scheduler import publish_scheduled_posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(publish_scheduled_posts, "interval", minutes=1)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="LinkedIn Analytics API", 
              description="A backend API for LinkedIn",
              lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(analytics.router)


@app.get("/")
def home():
    return {"msg": "Yo, what's up?"}