from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text)
    average_rating = Column(Float, default=0.0)
    ratings = relationship("BookRating", back_populates="book")

class BookRating(Base):
    __tablename__ = "book_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    score = Column(Float, nullable=False)

    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="unique_user_book_rating"),
    )