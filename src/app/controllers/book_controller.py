from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.model.schemas import BookCreate, BookResponse, RecordBookResponse
from src.app.repositories.book_repository import BookRepository
from src.app.model.models import User

class BookController:
    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)
    
    def create_book(self, book: BookCreate) -> BookResponse:
        db_book = self.book_repo.create_book(book)
        return BookResponse(
            book_id=db_book.book_id,
            book_name=db_book.book_name,
            book_quantity=db_book.book_quantity
        )
    
    def get_all_books(self) -> List[BookResponse]:
        books = self.book_repo.get_all_books()
        return [
            BookResponse(
                book_id=book.book_id,
                book_name=book.book_name,
                book_quantity=book.book_quantity
            ) for book in books
        ]
    
    def get_book_by_id(self, book_id: int) -> BookResponse:
        book = self.book_repo.get_book_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return BookResponse(
            book_id=book.book_id,
            book_name=book.book_name,
            book_quantity=book.book_quantity
        )
    
    def borrow_book(self, user: User, book_id: int) -> RecordBookResponse:
        book = self.book_repo.get_book_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        if book.book_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not available for borrowing"
            )
        
        record = self.book_repo.borrow_book(user.user_id, book_id)
        return RecordBookResponse(
            record_id=record.record_id,
            user_id=record.user_id,
            book_id=record.book_id,
            borrowed_at=record.borrowed_at,
            submitted_at=record.submitted_at
        )
    
    def return_book(self, user: User, book_id: int) -> RecordBookResponse:
        record = self.book_repo.return_book(user.user_id, book_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active borrowing record found for this book"
            )
        
        return RecordBookResponse(
            record_id=record.record_id,
            user_id=record.user_id,
            book_id=record.book_id,
            borrowed_at=record.borrowed_at,
            submitted_at=record.submitted_at
        ) 