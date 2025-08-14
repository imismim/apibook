from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.hashing import hash_password

def create_user(db: Session, username: str, password: str, role):
    hashed = hash_password(password)
    user = User(username=username, password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
