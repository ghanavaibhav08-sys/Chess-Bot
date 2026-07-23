import sys
from app.database.crud import get_user, get_unanalyzed_games, save_moves, mark_analyzed
from app.services.engine_analysis import analyze_pgn

def analyze_games_for_user(username: str):
    user = get_user(username)
    if not user:
        print(f"No user '{username}' found. Import games first.")
        return

    games = get_unanalyzed_games(user.id)
    print(f"Analyzing {len(games)} game(s)...")

    for game in games:
        moves = analyze_pgn(game.pgn)
        save_moves(game.id, moves)
        mark_analyzed(game.id)
        blunders = sum(1 for m in moves if m["classification"] == "blunder")
        print(f"  Game {game.id}: {len(moves)} moves analyzed, {blunders} blunder(s).")

    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_games.py <chess_com_username>")
        sys.exit(1)
    analyze_games_for_user(sys.argv[1])
