import json
from typing import Dict, Optional, Any
from pathlib import Path
from .exceptions import DataManagerError

class DataManager:
    def __init__(self, save_file: str = "saves/progress.json"):
        self.save_file = save_file
        # ensure the directory exists
        Path(self.save_file).parent.mkdir(parents=True, exist_ok=True)

    def has_saved_game(self) -> bool:
        """Return True if save file exists."""
        return Path(self.save_file).is_file()

    def save_progress(
        self,
        player_data: Dict[str, Any],
        location_states: Dict[int, Dict[str, Any]]
    ) -> bool:
        """
        Save full game state: player plus location progress.

        Args:
            player_data: your existing player_data dict
            location_states: mapping from location_id to that location’s
                             completion info, e.g.
                             { 1: {"defeated_enemies": [...],
                                  "boss_defeated": True,
                                  "is_completed": True}, … }
        """
        game_state = {
            "player": player_data,
            "locations": location_states
        }
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(game_state, f, indent=4)
            return True
        except Exception as e:
            raise DataManagerError(f"Error saving progress: {e}")

    def load_progress(self) -> Optional[Dict[str, Any]]:
        """
        Load full game state. Returns a dict with keys:
            - "player": Dict of player_data
            - "locations": Dict of location_states
        or None if no save exists.
        """
        path = Path(self.save_file)
        if not path.is_file():
            return None

        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            raise DataManagerError(f"Error loading progress: {e}")
