import sys
sys.path.append(r"C:\Users\User\Desktop\bookstore-api")
from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Session, select, SQLModel
from typing import List, Optional
from datetime import datetime

from database.session import engine, get_session
from database.models.book import Book, BookCreate, BookUpdate

app = FastAPI(title="Bookstore Inventory API", version="1.0.0")

# Automatically create the database tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# =====================================================================
# BOOKSTORE CRUD ENDPOINTS
# =====================================================================

# 1. Create a new book (POST /books)
@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Book).where(Book.isbn == book.isbn)).first()
    if existing:
        raise HTTPException(status_code=400, detail="A book with this ISBN already exists")
    
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# 2. List all books with optional filters (GET /books)
@app.get("/books", response_model=List[Book])
def list_books(
    author: Optional[str] = None,
    available: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    query = select(Book)
    if author:
        query = query.where(Book.author.contains(author))
    if available is not None:
        query = query.where(Book.available == available)
        
    return session.exec(query).all()

# 3. Search books by title or author (GET /books/search)
@app.get("/books/search", response_model=List[Book])
def search_books(q: str, session: Session = Depends(get_session)):
    query = select(Book).where(
        (Book.title.contains(q)) | (Book.author.contains(q))
    )
    return session.exec(query).all()

# 4. Get a specific book by ID (GET /books/{book_id})
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    product = session.get(Book, book_id)
    if not product:
        raise HTTPException(status_code=404, detail="Book not found")
    return product

# 5. Update a book (PATCH /books/{book_id})
@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
        
    db_book.updated_at = datetime.utcnow()
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# 6. Delete a book (DELETE /books/{book_id})
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    session.delete(db_book)
    session.commit()
    return None
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
