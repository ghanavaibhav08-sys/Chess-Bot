from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from app.database.base import Base

class Move(Base):
    __tablename__ = "moves"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    ply_number = Column(Integer)              # 1, 2, 3... (half-moves)
    move_san = Column(String)
    fen_before = Column(Text)
    eval_cp = Column(Float)                   # centipawn eval after the move (from white's POV)
    best_move_san = Column(String)
    best_eval_cp = Column(Float)
    eval_swing = Column(Float)                # drop in eval caused by this move
    classification = Column(String)           # "best" | "good" | "inaccuracy" | "mistake" | "blunder"
    is_white_move = Column(Integer)           # 1 or 0
