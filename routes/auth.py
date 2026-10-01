from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import supabase
from schemas.user import UserRegister, UserResponse, TokenResponse

from utils.auth import (
    get_user_by_email,
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister):

    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password_hash": hashed_password
    }

    try:
        response = (
            supabase
            .table("users")
            .insert(new_user)
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    return response.data[0]


@router.post("/login", response_model=TokenResponse)
def login_user(
    user: OAuth2PasswordRequestForm = Depends()
):

    existing_user = get_user_by_email(user.username)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    is_verified = verify_password(
        user.password,
        existing_user["password_hash"]
    )

    if not is_verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    access_token = create_access_token(
        existing_user["id"],
        existing_user["email"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }