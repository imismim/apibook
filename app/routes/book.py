from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..schemas.book import BookCreate, BookUpdate, BookOut, BookRatingCreate, BookRatingResponse
from ..crud import book as crud_book
from ..models.user import Role, User
from ..auth.dependencies import require_role, get_current_user
from ..models.book import BookRating, Book

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db), user=Depends(require_role(Role.writer, Role.admin))):
    return crud_book.create_book(db, book.title, book.author, book.description)

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return crud_book.get_books(db)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db), user=Depends(require_role(Role.writer, Role.admin))):
    updated = crud_book.update_book(db, book_id, book.title, book.author, book.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(require_role(Role.admin))):
    deleted = crud_book.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

@router.post("/{book_id}/rate", response_model=BookRatingResponse)
def rate_book(
    book_id: int,
    rating_data: BookRatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    existing_rating = (
        db.query(BookRating)
        .filter_by(book_id=book_id, user_id=current_user.id)
        .first()
    )

    if existing_rating:
        raise HTTPException(status_code=400, detail="You already rated this book")

    new_rating = BookRating(
        user_id=current_user.id,
        book_id=book_id,
        score=rating_data.score
    )
    db.add(new_rating)
    db.commit()

    avg_score = db.query(func.avg(BookRating.score)).filter(BookRating.book_id == book_id).scalar() or 0
    ratings_count = db.query(func.count(BookRating.id)).filter(BookRating.book_id == book_id).scalar()

    # Якщо хочеш зберігати в самій таблиці books
    book.average_rating = avg_score
    db.commit()

    return {
        "book_id": book_id,
        "average_score": round(avg_score, 2),
        "ratings_count": ratings_count
    }
