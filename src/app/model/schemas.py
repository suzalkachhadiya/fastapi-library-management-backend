from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    
    class Config:
        orm_mode = True

# Book schemas
class BookBase(BaseModel):
    book_name: str
    book_quantity: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    book_id: int
    
    class Config:
        orm_mode = True

# Record Book schemas
class RecordBookBase(BaseModel):
    user_id: int
    book_id: int

class RecordBookCreate(RecordBookBase):
    pass

class RecordBookResponse(RecordBookBase):
    record_id: int
    borrowed_at: date
    submitted_at: Optional[date] = None
    
    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 