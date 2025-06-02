from typing import List, Dict
from .items import Item, ConsumableItem

class InventoryManager:
    def __init__(self, player):
        self.player = player
        self.items: List[Item] = []

    def add_item(self, item: Item):
        self.items.append(item)
        self.player.inventory.setdefault("items", []).append({
            "type": type(item).__name__,
            "name": item.name,
            "description": item.description
        })

    def remove_item(self, item_obj: Item) -> bool:
        if item_obj in self.items:
            self.items.remove(item_obj)
            # Sync removal from player's inventory dict
            self.player.inventory["items"] = [
                i for i in self.player.inventory.get("items", [])
                if i["name"] != item_obj.name
            ]
            return True
        return False

    def use_item(self, item_name: str, context=None) -> str:
        for item in self.items:
            if item.name == item_name:
                result = item.use(context)
                if isinstance(item, ConsumableItem):
                    self.items.remove(item)
                return result
        return f"❌ Item '{item_name}' not found in inventory."

    def list_items(self) -> List[Dict[str, str]]:
        return [{"name": item.name, "description": item.description} for item in self.items]

    def get_item_names(self) -> List[str]:
        return [item.name for item in self.items]
    
    def get_items_by_type(self, item_type):
        return [item for item in self.items if isinstance(item, item_type)]
