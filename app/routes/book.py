from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.book import BookCreate, BookUpdate, BookOut
from ..crud import book as crud_book
from ..models.user import Role
from ..auth.dependencies import require_role

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db), user=Depends(require_role(Role.writer, Role.admin))):
    return crud_book.create_book(db, book.title, book.author, book.description, book.rating)

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return crud_book.get_books(db)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db), user=Depends(require_role(Role.writer, Role.admin))):
    updated = crud_book.update_book(db, book_id, book.title, book.author, book.description, book.rating)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(require_role(Role.admin))):
    deleted = crud_book.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
