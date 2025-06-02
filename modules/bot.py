import time
import random

from .npc import NPC
from .lore_manager import LoreManager

class Bot(NPC):
    def __init__(self):
        super().__init__(name="ARIA")
        self.topics_discussed = set()
        self.lore_manager = LoreManager("data/lore.json")
    
    def share_random_lore(self):
        """Share random lore when player checks inventory or during quiet moments"""
        all_entries = self.lore_manager.get_all_entries("ai_random_lore")
        unused_entries = [entry for entry in all_entries 
                         if entry.trigger not in self.topics_discussed]
        
        if unused_entries:
            entry = random.choice(unused_entries)
            self.speak(f"Did you know? {entry.content}")
            self.topics_discussed.add(entry.trigger)
        else:
            self.speak("I've shared all the lore I know for now.")
    
    def speak(self, message: str, delay: float = 1.5):
        print(f"\n[🤖 {self.name}]: ", end="", flush=True)
        for char in message:
            print(char, end="", flush=True)
            time.sleep(0.07)
        print()
        time.sleep(delay)
