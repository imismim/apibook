from fastapi import FastAPI
from .database import Base, engine
from .models import user, book
from .auth import routes as auth_routes
from .routes import book as book_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ApiBook")

app.include_router(auth_routes.router)
app.include_router(book_routes.router)
