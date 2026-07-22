from app.database.connection import SessionLocal
from app.models.user import User

def create_user(username):
    db = SessionLocal()
    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_user(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user
