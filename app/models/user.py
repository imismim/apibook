from sqlalchemy import Column, Integer, String, Enum
from ..database import Base
import enum

class Role(enum.Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.reader)
