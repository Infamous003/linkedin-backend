from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas.post import PostCreate, PostPublic, PostUpdate
from ..schemas.reaction import ReactionPublic
from ..models.models import User, Post, Reaction
from ..db.session import get_session
from sqlmodel import Session, select
from .auth import get_current_user
from ..models.enums import Role, Status, ReactionType
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/",
            response_model=list[PostPublic],
            status_code=status.HTTP_200_OK)
async def get_posts(
    user_id: int | None = None,
    status: Status | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    session: Session = Depends(get_session)
):
    query = select(Post)

    if user_id is not None:
        query = query.where(Post.user_id == user_id)

    if start_date is not None:
        query = query.where(Post.created_at >= start_date)

    if end_date is not None:
        query = query.where(Post.created_at <= end_date)
    
    if status is not None:
        query = query.where(Post.status == status)    

    posts = session.exec(query).all()
    return posts


@router.get("/my-posts",
            response_model=list[PostPublic],
            status_code=status.HTTP_200_OK)
async def get_my_posts(current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    my_posts = session.exec(
    select(Post).where(Post.user_id == current_user.id)
    ).fetchall()

    return my_posts


@router.get("/{id}",
            response_model=PostPublic,
            status_code=status.HTTP_200_OK)
def get_posts(
    id: int, 
    session: Session = Depends(get_session)
):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()
    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    
    # simulating a view. Each time this post is requested, increase the impression/view
    post_found.impressions += 1
    session.add(post_found)
    session.commit()
    session.refresh(post_found)
    return post_found


@router.post("/", 
             response_model=PostPublic, 
             status_code=status.HTTP_201_CREATED)
async def create_posts(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    now = datetime.now(timezone.utc)

    # Making sure that the post cannot be scheduled in the past
    # and also a 5 second delya
    if post.scheduled_at and post.scheduled_at < now - timedelta(seconds=5):
        raise HTTPException(status_code=422, detail="scheduled_at cannot be in the past")

    new_post = Post(**post.model_dump())
    new_post.user_id = current_user.id

    if new_post.scheduled_at and new_post.scheduled_at > now:
        new_post.status = Status.SCHEDULED
    else:
        new_post.status = Status.PUBLISHED

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post



@router.put("/{id}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def update_posts(id: int,
                        post: PostUpdate,
                        current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post_found.user_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access. You don't have to permission to modify/delete this post")

    if post.title: post_found.title = post.title
    if post.body: post_found.body = post.body
    if post.status: post_found.status = post.status
    if post.scheduled_at: post_found.scheduled_at = post.scheduled_at

    session.add(post_found)
    session.commit()
    session.refresh(post_found)
    return post_found


@router.delete("/{id}",
                status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post_found.user_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access. You don't have to permission to modify/delete this post")
    session.delete(post_found)
    session.commit()


@router.get(
    "/{id}/reactions", 
    status_code=status.HTTP_201_CREATED,
    response_model=list[ReactionPublic]
)
async def get_reactions(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    query = select(Reaction).where(Reaction.post_id == id)
    reactions = session.exec(query).fetchall()

    return reactions


@router.post(
    "/{id}/reactions", 
    status_code=status.HTTP_201_CREATED,
    response_model=ReactionPublic
)
async def create_reactions(
    id: int, 
    reaction: ReactionType,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    query = select(Reaction).where(Reaction.post_id == id, Reaction.user_id == current_user.id)
    reaction_found = session.exec(query).one_or_none()

    if reaction_found is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already reacted to this post")

    new_reaction = Reaction(post_id=id, user_id=current_user.id, type=reaction)
    print(new_reaction)
    session.add(new_reaction)
    session.commit()
    session.refresh(new_reaction)
    return new_reaction


@router.delete(
    "/{id}/reactions", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reactions(
    id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    query = select(Reaction).where(Reaction.post_id == id, Reaction.user_id == current_user.id)
    reaction = session.exec(query).one_or_none()

    if reaction is None:
        raise HTTPException(status_code=404, detail="Reaction not found")

    session.delete(reaction)
    session.commit()
    return  
