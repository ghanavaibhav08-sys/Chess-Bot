from app.database.connection import SessionLocal
from app.models.insight import Insight
from app.models.move import Move
from app.models.game import Game
from app.models.recommendation import Recommendation, TrainingPosition

def generate_recommendations(user_id: int):
    db = SessionLocal()
    insights = db.query(Insight).filter(Insight.user_id == user_id).all()

    recs = []

    phase_insights = [i for i in insights if i.category == "phase_blunders"]
    if phase_insights:
        worst = max(phase_insights, key=lambda i: i.value)
        if worst.value > 5:
            recs.append((1, f"Your blunder rate is highest in the {worst.label} "
                             f"({worst.value}% of moves). Focus your study time there."))

    opening_insights = [i for i in insights if i.category == "opening_performance" and i.sample_size >= 3]
    if opening_insights:
        worst_opening = min(opening_insights, key=lambda i: i.value)
        if worst_opening.value < 40:
            recs.append((2, f"You score only {worst_opening.value}% with {worst_opening.label}. "
                             f"Consider reviewing theory or switching openings."))

    db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()
    for priority, text in recs:
        db.add(Recommendation(user_id=user_id, text=text, priority=priority))
    db.commit()
    db.close()

def collect_training_positions(user_id: int, limit: int = 20):
    db = SessionLocal()
    game_ids = [g.id for g in db.query(Game).filter(Game.user_id == user_id).all()]
    blunders = (
        db.query(Move)
        .filter(Move.game_id.in_(game_ids), Move.classification == "blunder")
        .order_by(Move.eval_swing.desc())
        .limit(limit)
        .all()
    )

    db.query(TrainingPosition).filter(TrainingPosition.user_id == user_id).delete()
    for b in blunders:
        db.add(TrainingPosition(
            user_id=user_id,
            game_id=b.game_id,
            fen=b.fen_before,
            played_move_san=b.move_san,
            best_move_san=b.best_move_san,
            eval_swing=int(b.eval_swing * 100),
        ))
    db.commit()
    db.close()
