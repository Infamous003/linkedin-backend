from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from sqlmodel import select, Session
from ..models.models import Post
from ..models.enums import Status
from ..db.session import engine

def publish_scheduled_posts():
    now = datetime.now(timezone.utc)
    # session = get_session()
    with Session(engine) as session:
        query = select(Post).where(Post.status == "SCHEDULED", Post.scheduled_at <= now)
        posts_to_publish = session.exec(query).all()
        for post in posts_to_publish:
            fake_linkedin_api_call(post)
            post.status = Status.PUBLISHED
            session.add(post)
            session.commit()

def fake_linkedin_api_call(post: Post):
    print(f"-----Publishing post with ID: {post.id}")

scheduler = BackgroundScheduler()
scheduler.add_job(publish_scheduled_posts, "interval", minutes=1)
scheduler.start()
