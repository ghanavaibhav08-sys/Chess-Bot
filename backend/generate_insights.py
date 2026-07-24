import sys
from app.database.crud import get_user, save_insight, clear_insights
from app.services.pattern_detector import compute_phase_blunder_rates, compute_opening_performance
from app.services.recommender import generate_recommendations,collect_training_positions
def generate_insights_for_user(username: str):
    user = get_user(username)
    if not user:
        print(f"No user '{username}' found.")
        return

    clear_insights(user.id)

    phase_rates = compute_phase_blunder_rates(user.id)
    for phase, stats in phase_rates.items():
        save_insight(user.id, "phase_blunders", phase, stats["blunder_rate"], stats["sample_size"])

    openings = compute_opening_performance(user.id)
    for o in openings:
        total = o["wins"] + o["losses"] + o["draws"]
        win_rate = round(100 * o["wins"] / total, 1) if total else 0
        save_insight(user.id, "opening_performance", f"{o['opening']} ({o['eco']})", win_rate, total)

    print("Generating recommendations and training positions...")
    generate_recommendations(user.id)
    collect_training_positions(user.id) 
    print("Insights and Recommendations generated.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_insights.py <chess_com_username>")
        sys.exit(1)
    generate_insights_for_user(sys.argv[1])
