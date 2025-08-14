from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    rating: float = Field(default=0, ge=0, le=10)

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True
