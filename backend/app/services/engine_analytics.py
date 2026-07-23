import io
import chess
import chess.pgn
import chess.engine
import os
from dotenv import load_dotenv

load_dotenv()
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")

ANALYSIS_DEPTH = 14   # raise to 18-20 for stronger/slower analysis

def classify_swing(swing_cp: float) -> str:
    """swing_cp = how much the position got worse for the player who just moved."""
    if swing_cp >= 300:
        return "blunder"
    if swing_cp >= 150:
        return "mistake"
    if swing_cp >= 60:
        return "inaccuracy"
    if swing_cp <= 10:
        return "best"
    return "good"

def analyze_pgn(pgn_text: str) -> list[dict]:
    """Returns a list of per-move analysis dicts, in order."""
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        return []

    board = game.board()
    results = []

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        prev_eval_white_pov = 0.0

        for ply, move in enumerate(game.mainline_moves(), start=1):
            fen_before = board.fen()
            is_white_move = board.turn == chess.WHITE

            # Best move + eval BEFORE this move is played
            info_before = engine.analyse(board, chess.engine.Limit(depth=ANALYSIS_DEPTH))
            best_move = info_before["pv"][0] if "pv" in info_before else None
            best_move_san = board.san(best_move) if best_move else None

            move_san = board.san(move)
            board.push(move)

            info_after = engine.analyse(board, chess.engine.Limit(depth=ANALYSIS_DEPTH))
            score_after = info_after["score"].white().score(mate_score=10000)
            eval_after_white_pov = (score_after or 0) / 100.0

            # Swing from the mover's perspective
            if is_white_move:
                swing = prev_eval_white_pov - eval_after_white_pov
            else:
                swing = eval_after_white_pov - prev_eval_white_pov
            swing = max(swing, 0)  # only penalize moves that make things worse

            results.append({
                "ply_number": ply,
                "move_san": move_san,
                "fen_before": fen_before,
                "eval_cp": eval_after_white_pov,
                "best_move_san": best_move_san,
                "eval_swing": swing,
                "classification": classify_swing(swing * 100),
                "is_white_move": 1 if is_white_move else 0,
            })

            prev_eval_white_pov = eval_after_white_pov

    return results
