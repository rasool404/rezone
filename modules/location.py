from typing import List, Dict, Optional
from .enemy import Enemy, Boss, Raider, Mutant
import json

class Location:
    def __init__(
        self,
        name: str,
        level: int,
        description: str,
        enemies: List[Enemy],
        boss: Boss,
        xp_threshold: int
    ):
        self.name = name
        self.level = level
        self.description = description
        self.enemies = enemies
        self.boss = boss
        self.xp_threshold = xp_threshold

        self.enemies_defeated: List[Enemy] = []
        self.boss_defeated = False
        self.is_completed = False

    def get_next_enemy(self) -> Optional[Enemy]:
        remaining = [e for e in self.enemies if e not in self.enemies_defeated]
        if remaining:
            return remaining[0]
        if not self.boss_defeated:
            return self.boss
        return None

    def mark_enemy_defeated(self, enemy: Enemy) -> None:
        if enemy is self.boss:
            self.boss_defeated = True
        else:
            self.enemies_defeated.append(enemy)

        if len(self.enemies_defeated) == len(self.enemies) and self.boss_defeated:
            self.is_completed = True

    def get_completion_status(self) -> dict:
        return {
            'total_enemies': len(self.enemies),
            'defeated_enemies': len(self.enemies_defeated),
            'boss_defeated': self.boss_defeated,
            'is_completed': self.is_completed
        }


class LocationManager:
    def __init__(self, json_path="locations.json"):
        self.locations: Dict[int, Location] = {}
        self.current_location: Optional[Location] = None
        self.load_locations_from_json(json_path)

    def load_locations_from_json(self, json_path: str) -> None:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for loc in data:
            loc_id      = loc["id"]
            name        = loc["name"]
            level       = loc_id
            description = loc["description"]
            xp_thresh   = loc.get("xp_threshold", level * 100)

            # regular enemies
            enemies: List[Enemy] = []
            for ed in loc.get("enemies", []):
                t = ed["type"].lower()
                if t == "raider":
                    enemies.append(Raider(ed["name"], ed["health"], ed["attack"], ed["defense"], ed["exp_reward"]))
                elif t == "mutant":
                    enemies.append(Mutant(ed["name"], ed["health"], ed["attack"], ed["defense"], ed["exp_reward"]))

            # boss
            bd = loc["boss"]
            bt = bd["type"].lower()
            if bt == "raider":
                boss = Raider(bd["name"], bd["health"], bd["attack"], bd["defense"], bd["exp_reward"])
            elif bt == "mutant":
                boss = Mutant(bd["name"], bd["health"], bd["attack"], bd["defense"], bd["exp_reward"])
            else:
                boss = Boss(bd["name"], bd["health"], bd["attack"], bd["defense"], bd["exp_reward"])

            self.locations[loc_id] = Location(name, level, description, enemies, boss, xp_thresh)

    def get_all_locations(self) -> List[Location]:
        return list(self.locations.values())

    def get_available_locations(self, player_level: int) -> List[Location]:
        return [loc for loc in self.locations.values()
                if loc.level <= player_level and not loc.is_completed]

    def enter_location(self, location: Location, player_level: int) -> str:
        if location.level > player_level:
            return "level_mismatch"
        if location.is_completed:
            return "already_completed"
        self.current_location = location
        return "success"

    def get_current_location(self) -> Optional[Location]:
        return self.current_location

    def get_current_enemy(self) -> Optional[Enemy]:
        if self.current_location:
            return self.current_location.get_next_enemy()
        return None