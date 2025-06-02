from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, Callable

class CardType(Enum):
    ATTACK  = auto()
    DEFENSE = auto()
    UTILITY = auto()

class Card(ABC):
    def __init__(self, name: str, energy_cost: int, description: str):
        self.name = name
        self.energy_cost = energy_cost
        self.description = description

    @abstractmethod
    def use(self, source: 'Character', target: Optional['Character'] = None):
        pass

class AttackCard(Card):
    def __init__(self, name: str, energy_cost: int, damage: int, description: str, tags: Optional[list] = None):
        super().__init__(name, energy_cost, description)
        self.damage = damage
        self.card_type = CardType.ATTACK
        self.tags = tags or []

    def use(self, source: 'Character', target: 'Character') -> int:
        # Example synergy: bonus if last card had the same tag
        bonus = 0
        if hasattr(source, "last_card_tag"):
            if "strike" in self.tags and source.last_card_tag == "strike":
                bonus += 2  # combo bonus
        final_damage = max(0, self.damage + source.attack + bonus - target.defense)
        target.health = max(0, target.health - final_damage)

        # Record this card's tag for synergy next turn
        if self.tags:
            source.last_card_tag = self.tags[0]
        return final_damage


class DefenseCard(Card):
    def __init__(self, name: str, energy_cost: int, defense: int, description: str):
        super().__init__(name, energy_cost, description)
        self.defense = defense
        self.card_type = CardType.DEFENSE

    def use(self, source: 'Character', target: Optional['Character'] = None) -> None:
        source.defense += self.defense

class UtilityCard(Card):
    def __init__(self, name: str, energy_cost: int, effect: Callable, description: str):
        super().__init__(name, energy_cost, description)
        self.effect = effect
        self.card_type = CardType.UTILITY

    def use(self, source: 'Character', target: Optional['Character'] = None) -> None:
        self.effect(source, target)