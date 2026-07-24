from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text)
    priority = Column(Integer)   # 1 = highest
    created_at = Column(DateTime, default=datetime.utcnow)

class TrainingPosition(Base):
    __tablename__ = "training_positions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    fen = Column(Text)
    played_move_san = Column(String)
    best_move_san = Column(String)
    eval_swing = Column(Integer)
