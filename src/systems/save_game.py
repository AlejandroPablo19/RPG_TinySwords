"""Sistema de guardado local mediante archivos JSON."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAVE_PATH = ROOT / "saves" / "save.json"


def save_game(player):
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "player": {
            "x": player.position.x,
            "y": player.position.y,
        }
    }

    with SAVE_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Partida guardada correctamente.")


def load_game():
    if not SAVE_PATH.exists():
        return None

    try:
        with SAVE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        player_data = data["player"]

        return {
            "x": float(player_data["x"]),
            "y": float(player_data["y"]),
        }

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("El archivo de guardado no es válido.")
        return None