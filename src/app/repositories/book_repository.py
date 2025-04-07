from sqlalchemy.orm import Session
from src.app.model.models import Book, RecordBook
from src.app.model.schemas import BookCreate
from datetime import date

class BookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_book_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.book_id == book_id).first()
    
    def get_all_books(self):
        return self.db.query(Book).all()
    
    def create_book(self, book: BookCreate):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def update_book_quantity(self, book_id: int, change: int):
        book = self.get_book_by_id(book_id)
        if book:
            book.book_quantity += change
            self.db.commit()
            self.db.refresh(book)
        return book
    
    def borrow_book(self, user_id: int, book_id: int):
        # Create borrowing record
        record = RecordBook(user_id=user_id, book_id=book_id)
        self.db.add(record)
        
        # Decrease book quantity
        self.update_book_quantity(book_id, -1)
        
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def return_book(self, user_id: int, book_id: int):
        # Find the borrowing record
        record = self.db.query(RecordBook).filter(
            RecordBook.user_id == user_id,
            RecordBook.book_id == book_id,
            RecordBook.submitted_at.is_(None)
        ).first()
        
        if record:
            # Update record with submission date
            record.submitted_at = date.today()
            
            # Increase book quantity
            self.update_book_quantity(book_id, 1)
            
            self.db.commit()
            self.db.refresh(record)
        
        return record 