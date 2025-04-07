from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config.database import engine, Base
from src.app.routes import user_routes, book_routes

from src.app.model.models import User
from src.app.model.models import Book
from src.app.model.models import RecordBook


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="API for managing library books and user borrowing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)
app.include_router(book_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API"}
