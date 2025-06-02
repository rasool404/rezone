from abc import ABC

class NPC(ABC):
    def __init__(self, name: str):
        self.name = name
        
    def speak(self):
        pass
