from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.config.database import get_db
from src.app.controllers.book_controller import BookController
from src.app.model.schemas import BookCreate, BookResponse, RecordBookResponse
from src.app.utils.auth import get_current_active_user
from src.app.model.models import User

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    controller = BookController(db)
    return controller.create_book(book)

@router.get("/", response_model=List[BookResponse])
def get_all_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    controller = BookController(db)
    return controller.get_all_books()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    controller = BookController(db)
    return controller.get_book_by_id(book_id)

@router.post("/{book_id}/borrow", response_model=RecordBookResponse)
def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    controller = BookController(db)
    return controller.borrow_book(current_user, book_id)

@router.post("/{book_id}/return", response_model=RecordBookResponse)
def return_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    controller = BookController(db)
    return controller.return_book(current_user, book_id)
