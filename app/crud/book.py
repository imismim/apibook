from sqlalchemy.orm import Session
from ..models.book import Book

def create_book(db: Session, title: str, author: str, description: str = None):
    book = Book(title=title, author=author, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_books(db: Session):
    return db.query(Book).all()

def update_book(db: Session, book_id: int, title: str, author: str, description: str):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.title = title
        book.author = author
        book.description = description
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book
