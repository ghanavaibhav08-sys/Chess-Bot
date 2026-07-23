import io
import chess.pgn

def parse_pgn_headers(pgn_text: str) -> dict:
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        return {}
    h = game.headers
    return {
        "white": h.get("White", ""),
        "black": h.get("Black", ""),
        "result": h.get("Result", ""),
        "opening": h.get("Opening", ""),
        "eco": h.get("ECO", ""),
        "date": h.get("UTCDate") or h.get("Date", ""),
    }
