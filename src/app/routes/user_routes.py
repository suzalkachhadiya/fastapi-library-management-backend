from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.config.database import get_db
from src.app.controllers.user_controller import UserController
from src.app.model.schemas import UserCreate, UserResponse, Token
from src.app.utils.auth import get_current_active_user
from src.app.model.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    controller = UserController(db)
    return controller.register_user(user)

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    controller = UserController(db)
    return controller.authenticate_user(form_data.username, form_data.password)

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        user_id=current_user.user_id,
        username=current_user.username,
        email=current_user.email
    ) 