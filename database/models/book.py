from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    isbn: str = Field(unique=True, index=True)
    published_year: int
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    available: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(SQLModel):
    title: str
    author: str
    isbn: str
    published_year: int
    price: float
    stock: int = 0

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    available: Optional[bool] = None
