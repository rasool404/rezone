from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, source, target):
        pass

class CardItem(Item):
    def __init__(self, card):
        super().__init__(card.name, card.description)
        self.card = card

    def use(self, source, target):
        return None

class ConsumableItem(Item):
    def __init__(self, name: str, description: str, effect_func):
        super().__init__(name, description)
        self.effect_func = effect_func

    def use(self, source, target):
        return self.effect_func(source, target)

