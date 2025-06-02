import json
from typing import List, Optional, Dict

class LoreEntry:
    def __init__(self, trigger: str, content: str, category: str):
        self.trigger = trigger
        self.content = content
        self.category = category

    def to_dict(self) -> Dict:
        return {
            "trigger": self.trigger,
            "content": self.content,
            "category": self.category
        }

    def __str__(self):
        return f"[{self.category} (Trigger: {self.trigger})\n{self.content}"

class LoreManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.entries: List[LoreEntry] = []
        self._load_entries()

    def _load_entries(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for category, lore_list in data.items():
                    for i, entry in enumerate(lore_list):
                        if isinstance(entry, dict):
                            self.entries.append(LoreEntry(
                                trigger=entry.get("trigger", f"{category}_{i}"),
                                content=entry["content"],
                                category=category
                            ))
                        elif isinstance(entry, str):
                            self.entries.append(LoreEntry(
                                trigger=f"{category}_{i}",
                                content=entry,
                                category=category
                            ))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading lore: {e}")


    def get_all_entries(self, category: Optional[str] = None) -> List[LoreEntry]:
        if category:
            return [entry for entry in self.entries if entry.category == category]
        return self.entries

    def get_entries_by_category(self, category: str) -> List[LoreEntry]:
        """Returns all lore entries that match a specific category."""
        return [entry for entry in self.entries if entry.category == category]

    def get_by_trigger(self, trigger: str) -> Optional[LoreEntry]:
        return next((entry for entry in self.entries if entry.trigger == trigger), None)

    def search_by_keyword(self, keyword: str, category: Optional[str] = None) -> List[LoreEntry]:
        keyword = keyword.lower()
        return [
            entry for entry in self.get_all_entries(category)
            if keyword in entry.content.lower()
        ]
