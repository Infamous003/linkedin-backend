from fastapi import APIRouter, status, HTTPException, Depends
from ..schemas.user import UserCreate, UserPublic, Token
from ..models.models import User
from ..db.session import get_session
from sqlmodel import Session, select
from .deps import (
    get_password_hash,
    authenticate_user, 
    create_access_token,
    decode_jwt,
    get_user_or_404
)
from ..core.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token, secret_key=SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_or_404(username=username, session=session)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             response_model=UserPublic)
def register(new_user: UserCreate, session: Session = Depends(get_session)):
    query = select(User).where(User.username == new_user.username)
    user = session.exec(query).one_or_none()

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        user = User(**new_user.model_dump())
        user.password = get_password_hash(new_user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.post("/login",
             response_model=Token,
             status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(user_data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


# This route is responsible for displaying the Authorize button
@router.get("/users/me",
            response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user