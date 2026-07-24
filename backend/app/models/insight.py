from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)      # "phase_blunders" | "opening_weakness" | "overall"
    label = Column(String)         # e.g. "endgame", "Sicilian Defense (B20)"
    value = Column(Float)          # e.g. blunder rate as a percentage
    sample_size = Column(Integer)  # how many games/moves this is based on
    created_at = Column(DateTime, default=datetime.utcnow)
