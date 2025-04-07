from sqlalchemy import Column, Integer, String, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.app.config.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Will store hashed password
    
    # Relationship with record_book
    borrowed_books = relationship("RecordBook", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, index=True)
    book_quantity = Column(Integer)
    
    # Relationship with record_book
    borrowing_records = relationship("RecordBook", back_populates="book")

class RecordBook(Base):
    __tablename__ = "record_book"

    record_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    borrowed_at = Column(Date, default=func.current_date())
    submitted_at = Column(Date, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowing_records") 