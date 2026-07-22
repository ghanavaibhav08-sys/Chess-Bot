from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database.base import Base

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chess_com_game_id = Column(String, unique=True)
    white = Column(String)
    black = Column(String)
    result = Column(String)
    opening = Column(String)
    eco = Column(String)
    pgn = Column(Text)
    date = Column(DateTime)
    analyzed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
