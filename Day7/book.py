from typing import List, Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

# ------------------------
# Database setup
# ------------------------
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, echo=True)

# ------------------------
# Book model
# ------------------------
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str

# ------------------------
# Create DB tables
# ------------------------
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ------------------------
# FastAPI app
# ------------------------
app = FastAPI(title="Book Manager API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ------------------------
# Endpoints
# ------------------------

# 1. Get all books
@app.get("/books", response_model=List[Book])
def get_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return books

# 2. Add a new book
@app.post("/books", response_model=Book)
def add_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

# 3. Delete a book by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"message": f"Book with ID {book_id} deleted successfully"}
