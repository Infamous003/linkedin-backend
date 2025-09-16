from fastapi import APIRouter, status, HTTPException, Depends
from ..models.models import User, Post, Reaction
from ..db.session import get_session
from sqlmodel import Session, select, text
from .auth import get_current_user
from ..models.enums import Role


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/{post_id}/metrics", status_code=status.HTTP_200_OK)
async def get_post_analytics(
    post_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if current_user.id != post.user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    reactions = session.exec(select(Reaction).where(Reaction.post_id == post_id)).all()

    likes = sum(1 for r in reactions if r.type == "like")
    support = sum(1 for r in reactions if r.type == "support")
    celebrate = sum(1 for r in reactions if r.type == "celebrate")
    insights = sum(1 for r in reactions if r.type == "insightful")
    love = sum(1 for r in reactions if r.type == "love")

    analytics = {
        "total_reactions": len(reactions),
        "impressions": post.impressions,
        "engagements": likes + support + insights + celebrate + love,
        "reaction_types": {
            "likes": likes,
            "support": support,
            "celebrate": celebrate,
            "insightful": insights,
            "love": love,
        },

        "comments": 0,
        "shares": 5,
    }

    return {"analytics": analytics}



@router.get("/analytics/posts/top", status_code=200)
async def get_top_posts(
    limit: int = 3,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = text("""
        SELECT 
            p.id,
            p.title,
            p.impressions,
            COUNT(r.id) AS total_reactions
        FROM posts p
        LEFT JOIN reactions r ON p.id = r.post_id
        GROUP BY p.id
        ORDER BY p.impressions DESC
        LIMIT :limit
    """).bindparams(limit=limit)

    results = session.exec(query).all()

    top_posts = []

    for r in results:
        post = {
            "id": r.id,
            "title": r.title,
            "impressions": r.impressions,
            "total_reactions": r.total_reactions
        }
        top_posts.append(post)

    return {"top_posts": top_posts}