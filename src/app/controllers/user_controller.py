from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from src.app.config.database import get_db
from src.app.model.schemas import UserCreate, UserResponse, Token
from src.app.repositories.user_repository import UserRepository
from src.app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

class UserController:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user: UserCreate) -> UserResponse:
        # Check if username or email already exists
        if self.user_repo.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        if self.user_repo.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        db_user = self.user_repo.create_user(user)
        return UserResponse(
            user_id=db_user.user_id,
            username=db_user.username,
            email=db_user.email
        )
    
    def authenticate_user(self, username: str, password: str) -> Token:
        user = self.user_repo.get_user_by_username(username)
        if not user or not self.user_repo.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer") 