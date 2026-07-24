from collections import defaultdict
from app.database.connection import SessionLocal
from app.models.game import Game
from app.models.move import Move

def game_phase(ply_number: int) -> str:
    if ply_number <= 20:
        return "opening"
    if ply_number <= 60:
        return "middlegame"
    return "endgame"

def compute_phase_blunder_rates(user_id: int) -> dict:
    db = SessionLocal()
    game_ids = [g.id for g in db.query(Game).filter(Game.user_id == user_id).all()]
    moves = db.query(Move).filter(Move.game_id.in_(game_ids)).all()
    db.close()

    phase_totals = defaultdict(int)
    phase_blunders = defaultdict(int)

    for m in moves:
        phase = game_phase(m.ply_number)
        phase_totals[phase] += 1
        if m.classification == "blunder":
            phase_blunders[phase] += 1

    return {
        phase: {
            "blunder_rate": round(100 * phase_blunders[phase] / phase_totals[phase], 1)
            if phase_totals[phase] else 0,
            "sample_size": phase_totals[phase],
        }
        for phase in phase_totals
    }

def compute_opening_performance(user_id: int) -> list[dict]:
    db = SessionLocal()
    games = db.query(Game).filter(Game.user_id == user_id).all()
    db.close()

    by_eco = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "opening": ""})

    for g in games:
        entry = by_eco[g.eco or "unknown"]
        entry["opening"] = g.opening or "Unknown opening"
        result = (g.result or "").lower()
        if result in ("1-0",) and g.white:  # simplistic; refine with the user's actual color
            entry["wins"] += 1
        elif result in ("0-1",):
            entry["losses"] += 1
        else:
            entry["draws"] += 1

    return [
        {"eco": eco, **stats}
        for eco, stats in by_eco.items()
    ]
