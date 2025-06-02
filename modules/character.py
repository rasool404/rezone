from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum, auto
import random
from .cards import Card

class StatusEffect(Enum):
    POISONED   = auto()
    BURNED     = auto()
    PARALYZED  = auto()
    ATTACK_UP  = auto()
    DEFENSE_UP = auto()

class Character(ABC):
    def __init__(self, name: str, health: int):
        self.name = name
        self.max_health = health
        self.health = health
        self.alive = True

        # status_effects maps effect → {'duration': int, 'amount': int}
        self.status_effects: Dict[StatusEffect, Dict[str,int]] = {}

        # Base stats
        self.base_attack = 10
        self.base_defense = 5
        # Current stats
        self.attack = self.base_attack
        self.defense = self.base_defense

        
   

    def add_status_effect(
        self,
        effect: StatusEffect,
        duration: int,
        amount: Optional[int] = None
    ) -> None:
        """
        Add or override a status effect.
        - For ATTACK_UP/DEFENSE_UP, `amount` is the buff magnitude.
        - For POISONED/BURNED, `amount` is damage per turn (default 1).
        """
        self.status_effects[effect] = {
            'duration': duration,
            'amount': amount if amount is not None else 1
        }

    def reset_temporary_stats(self) -> None:
        """
        Reset to base stats, then apply any active ATTACK_UP/DEFENSE_UP buffs.
        Call at start of each turn.
        """
        self.attack = self.base_attack
        self.defense = self.base_defense

        for eff, data in self.status_effects.items():
            if eff == StatusEffect.ATTACK_UP:
                self.attack += data['amount']
            elif eff == StatusEffect.DEFENSE_UP:
                self.defense += data['amount']

    def update_status_effects(self) -> None:
        """
        Tick down every effect. For POISONED/BURNED, apply damage first.
        Remove any whose duration reaches zero. Call at end of each turn.
        """
        to_remove = []
        for eff, data in self.status_effects.items():
            # Debuff damage
            if eff == StatusEffect.POISONED or eff == StatusEffect.BURNED:
                self.health = max(0, self.health - data['amount'])

            # Tick down
            data['duration'] -= 1
            if data['duration'] <= 0:
                to_remove.append(eff)

        for eff in to_remove:
            del self.status_effects[eff]

        # Update alive status
        self.alive = self.health > 0

    def can_act(self) -> bool:
        return self.alive and StatusEffect.PARALYZED not in self.status_effects

    def is_alive(self) -> bool:
        return self.health > 0

    def get_stats(self) -> dict:
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'status_effects': {
                eff.name: (data['amount'], data['duration'])
                for eff, data in self.status_effects.items()
            }
        }
    
    def __str__(self):
        return f"{self.name} (HP: {self.health}/{self.max_health})"