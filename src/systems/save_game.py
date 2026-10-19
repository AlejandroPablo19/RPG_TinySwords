"""Guardado local sencillo en JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAVE_FILE = ROOT / "saves" / "save.json"

def save_player(player):
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"player_x": player.position.x, "player_y": player.position.y}
    SAVE_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")

def load_player(default_x, default_y):
    if not SAVE_FILE.exists():
        return default_x, default_y
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        return float(data.get("player_x", default_x)), float(data.get("player_y", default_y))
    except (OSError, ValueError, TypeError):
        return default_x, default_y
