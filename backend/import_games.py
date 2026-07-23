import sys
from app.services.chess_com_client import get_archives, get_games_from_archive
from app.services.pgn_parser import parse_pgn_headers
from app.database.crud import get_user, create_user, game_exists, create_game

def import_games_for_user(username: str):
    user = get_user(username) or create_user(username)
    archives = get_archives(username)
    imported = 0

    for archive_url in archives:
        for g in get_games_from_archive(archive_url):
            game_id = str(g.get("url", "")).split("/")[-1]
            if not game_id or game_exists(game_id):
                continue
            pgn = g.get("pgn", "")
            parsed = parse_pgn_headers(pgn)
            create_game(user_id=user.id, chess_com_game_id=game_id, pgn=pgn, parsed=parsed)
            imported += 1

    print(f"Imported {imported} new games for {username}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_games.py <chess_com_username>")
        sys.exit(1)
    import_games_for_user(sys.argv[1])
