import random
from .character import Character, StatusEffect
from .cards import AttackCard, DefenseCard, UtilityCard

class Enemy(Character):
    def __init__(self, name: str, health: int, attack: int, defense: int, exp_reward: int):
        super().__init__(name, health)
        self.base_attack = attack
        self.base_defense = defense
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward

    def get_next_action(self, player: Character) -> AttackCard:
        """Fallback behavior: always attack"""
        return AttackCard("Basic Attack", 0, self.attack, f"{self.name} attacks.")
    
    def __str__(self):
        return (f"[Enemy] {self.name} | HP: {self.health} | "
            f"ATK: {self.attack} | DEF: {self.defense}")

class Raider(Enemy):
    def get_next_action(self, player: Character):
        if self.health < self.max_health * 0.4:
            # 70% chance to defend, 30% chance to attack
            if random.random() < 0.7:
                return DefenseCard("Brace", 0, 2, "Defends in desperation.")
        return AttackCard("Slash", 0, self.attack, "A slashing attack.")

class Mutant(Enemy):
    def get_next_action(self, player: Character):
        if player.health > player.max_health * 0.5:
            # 60% chance to use powerful attack, 40% to use normal
            if random.random() < 0.6:
                return AttackCard("Frenzy", 0, int(self.attack * 1.5), "A wild, frenzied attack.")
        return AttackCard("Contaminate", 0, self.attack, "A toxic hit.")

class Boss(Enemy):
    def get_next_action(self, player: Character):
        # 20% chance to use a utility card each turn
        if random.random() < 0.2:
            return random.choice(self._utility_cards(player))

        # 50% chance to defend if player is too tanky
        if player.defense > self.attack and random.random() < 0.5:
            return DefenseCard("Iron Shell", 0, self.defense + 4, "Fortifies defenses.")

        return AttackCard("Devastating Blow", 0, self.attack * 2, "A powerful strike.")

    def _utility_cards(self, player):
        # List of utility cards bosses can use
        return [
            UtilityCard(
                "Battle Roar", 0,
                lambda s, t: s.add_status_effect(StatusEffect.ATTACK_UP, duration=3, amount=3),
                "Boosts its attack power for 3 turns."
            ),
            UtilityCard(
                "Toxic Pulse", 0,
                lambda s, t: t.add_status_effect(StatusEffect.BURNED, duration=3, amount=2),
                "Applies burn for 3 turns (2 dmg/turn)."
            ),
            UtilityCard(
                "Corrosive Shout", 0,
                lambda s, t: t.add_status_effect(StatusEffect.POISONED, duration=2, amount=3),
                "Poisons the player for 2 turns."
            )
        ]