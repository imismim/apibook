
from sqlalchemy import func
from models.book import BookRating, Book

def update_average_rating(db, book_id):
    avg = db.query(func.avg(BookRating.score)).filter(BookRating.book_id == book_id).scalar()
    book = db.query(Book).get(book_id)
    book.average_rating = avg
    db.commit()
