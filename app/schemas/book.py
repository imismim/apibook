from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookRatingCreate(BaseModel):
    score: float = Field(..., ge=0.0, le=5.0)  

class BookRatingResponse(BaseModel):
    book_id: int
    average_score: float
    ratings_count: int

    class Config:
        orm_mode = True