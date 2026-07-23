import requests

BASE_URL = "https://api.chess.com/pub/player"

def get_archives(username: str) -> list[str]:
    url = f"{BASE_URL}/{username}/games/archives"
    resp = requests.get(url, headers={"User-Agent": "ChessCoachApp/1.0"})
    resp.raise_for_status()
    return resp.json()["archives"]

def get_games_from_archive(archive_url: str) -> list[dict]:
    resp = requests.get(archive_url, headers={"User-Agent": "ChessCoachApp/1.0"})
    resp.raise_for_status()
    return resp.json()["games"]
