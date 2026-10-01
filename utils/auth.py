from database import supabase
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing")

if not ALGORITHM:
    raise RuntimeError("ALGORITHM is missing")


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_access_token(user_id: int, email: str):
    from datetime import datetime, timedelta, timezone

    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expiration
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_user_by_email(email: str):
    try:
        response = (
            supabase
            .table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    return response.data[0] if response.data else None


def get_user_by_id(user_id: int):
    try:
        response = (
            supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    return response.data[0] if response.data else None


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token not valid"
        )

    return payload


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user