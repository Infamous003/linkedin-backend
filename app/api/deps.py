from fastapi import status, HTTPException, Depends
from ..db.session import get_session
from sqlmodel import Session, select
from ..models.user import User
from ..schemas.user import UserPublic
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
# from .auth import oauth2_scheme
from ..core.config import settings
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRATION_MINUTES = settings.TOKEN_EXPIRATION_MINUTES


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def decode_jwt(token: str, secret_key: str, algorithms: list[str]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_or_404(username: str, session: Session):
    query = select(User).where(User.username == username)
    user = session.exec(query).one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def authenticate_user(username: str, password: str, session: Session):
    user = None
    
    query = select(User).where(User.username == username)
    user = session.exec(query).one_or_none()

    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(user_data: dict):
    # user_data dictionary contains the username
    to_encode = user_data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt