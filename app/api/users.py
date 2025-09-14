from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas.user import UserPublic, UserUpdate
from ..models.models import User
from ..db.session import get_session
from sqlmodel import Session, select
from .deps import get_password_hash
from .auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", 
            status_code=status.HTTP_200_OK, 
            response_model=list[UserPublic])
def get_user(session: Session = Depends(get_session)):
    query = select(User)
    user = session.exec(query).fetchall()

    return user


@router.get("/{id}", 
            status_code=status.HTTP_200_OK, 
            response_model=UserPublic)
def get_user_by_id(id: int, 
                   session: Session = Depends(get_session)):
    query = select(User).where(User.id == id)
    user = session.exec(query).one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return user
    

@router.put("/",
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
def update_user(user: UserUpdate, 
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    query = select(User).where(User.id == current_user.id)
    user_found = session.exec(query).one_or_none()

    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.username: user_found.username = user.username
    if user.firstname: user_found.firstname = user.firstname
    if user.lastname: user_found.lastname = user.lastname
    if user.password: user_found.password = get_password_hash(user.password)

    session.add(user_found)
    session.commit()
    session.refresh(user_found)
    return user_found


@router.delete("/",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    query = select(User).where(User.id == current_user.id)

    user_found = session.exec(query).one_or_none()

    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        session.delete(user_found)
        session.commit()