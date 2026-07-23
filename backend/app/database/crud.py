from app.models.game import Game
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.move import Move

def save_moves(game_id: int, moves: list[dict]):
    db = SessionLocal()
    for m in moves:
        db.add(Move(game_id=game_id, **m))
    db.commit()
    db.close()
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
def game_exists(chess_com_game_id: str) -> bool:
    db = SessionLocal()
    exists = db.query(Game).filter(Game.chess_com_game_id == chess_com_game_id).first() is not None
    db.close()
    return exists

def create_game(user_id: int, chess_com_game_id: str, pgn: str, parsed: dict):
    db = SessionLocal()
    game = Game(
        user_id=user_id,
        chess_com_game_id=chess_com_game_id,
        white=parsed.get("white"),
        black=parsed.get("black"),
        result=parsed.get("result"),
        opening=parsed.get("opening"),
        eco=parsed.get("eco"),
        pgn=pgn,
        analyzed=False,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    db.close()
    return game

def get_unanalyzed_games(user_id: int):
    db = SessionLocal()
    games = db.query(Game).filter(Game.user_id == user_id, Game.analyzed == False).all()
    db.close()
    return games

def mark_analyzed(game_id: int):
    db = SessionLocal()
    game = db.query(Game).filter(Game.id == game_id).first()
    game.analyzed = True
    db.commit()
    db.close()
