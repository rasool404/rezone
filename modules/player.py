import random
from typing import Dict, Optional, List
from .character import Character, StatusEffect
from .cards import Card, AttackCard, DefenseCard, UtilityCard
from .inventory_manager import InventoryManager 

class Player(Character):
    XP_THRESHOLDS = [110, 180, 250]  # Custom thresholds for first few levels
    DEFAULT_XP_THRESHOLD = 300       # Default threshold for levels beyond defined ones

    CARD_UNLOCKS = {
        2: [
            AttackCard("Lunge", 1, 7, "Deal 7 damage. Cheap and fast.", tags=["strike"]),
            UtilityCard("Adrenaline", 1, lambda s, t: setattr(s, "energy", min(s.max_energy, s.energy + 20)), "Gain 20 energy."),
        ],
        3: [
            DefenseCard("Fortify", 2, 10, "Gain 10 defense."),
            UtilityCard("Overclock", 2, lambda s, t: s.add_status_effect(StatusEffect.ATTACK_UP, 3, 3), "Boost attack +3 for 3 turns."),
        ],
        4: [
            AttackCard("Exploit Weakness", 2, 6, "Deal 6 damage and Burn if enemy has less defense.", tags=["tactic"]),
        ]
    }

    def __init__(self, name: str):
        super().__init__(name, health=100)
        self.level = 1
        self.xp = 0
        self.money = 0
        self.energy = 100
        self.max_energy = 100
        self.inventory: Dict = {}
        self.inventory_manager = InventoryManager(self)

        self.hand: List[Card] = []
        self.deck: List[Card] = []
        self.discard_pile: List[Card] = []

        self.unlocked_cards: set[str] = set()  

        self.initialize_starter_deck()


    def initialize_starter_deck(self) -> None:
        def focus_effect(source, _):
            source.add_status_effect(StatusEffect.ATTACK_UP, duration=2, amount=2)

        def regen_effect(source, _):
            source.add_status_effect(StatusEffect.DEFENSE_UP, duration=2, amount=2)

        def precision_effect(source, target):
            if target and target.health > source.health:
                target.add_status_effect(StatusEffect.BURNED, duration=2, amount=1)

        self.deck = [
            AttackCard("Strike", 12, 6, "Deal 6 damage. [strike]", tags=["strike"]),
            AttackCard("Combo Slash", 14, 5, "Deal 5 damage. +2 if last card was a strike.", tags=["strike"]),
            AttackCard("Heavy Blow", 22, 10, "Big hit. Costly but strong.", tags=["power"]),

            DefenseCard("Guard", 10, 5, "Gain +5 defense."),
            DefenseCard("Iron Wall", 18, 8, "Gain +8 defense."),

            UtilityCard("Focus", 15, lambda s, t: s.add_status_effect(StatusEffect.ATTACK_UP, 2, 2), "Gain +2 attack for 2 turns."),
            UtilityCard("Regenerate", 15, lambda s, t: s.add_status_effect(StatusEffect.DEFENSE_UP, 2, 2), "Gain +2 defense for 2 turns."),
            UtilityCard("Precision", 24, lambda s, t: t.add_status_effect(StatusEffect.BURNED, 2, 1) if t and t.health > s.health else None, "Burn target if it has more HP than you."),
        ]
        random.shuffle(self.deck)

    
    def draw_cards(self, count: int) -> None:
        needed = count
        existing = {c.name for c in self.hand}

        while needed > 0 and (self.deck or self.discard_pile):
            if not self.deck:
                self.deck = self.discard_pile.copy()
                self.discard_pile.clear()
                random.shuffle(self.deck)

            for i, card in enumerate(self.deck):
                if card.name not in existing:
                    self.hand.append(self.deck.pop(i))
                    existing.add(card.name)
                    needed -= 1
                    break
            else:
                break


    def get_xp_threshold(self) -> int:
        if self.level - 1 < len(Player.XP_THRESHOLDS):
            return Player.XP_THRESHOLDS[self.level - 1]
        return Player.DEFAULT_XP_THRESHOLD

    def gain_xp(self, amount: int, threshold: Optional[int] = None) -> bool:
        """
        Add XP and level up when xp >= threshold (either custom or based on level).
        Any excess XP carries over toward the next level.
        """
        xp_thresh = threshold if threshold is not None else self.get_xp_threshold()
        self.xp += amount
        leveled = False
        while self.xp >= xp_thresh:
            self.xp -= xp_thresh
            self.level_up()
            xp_thresh = self.get_xp_threshold()  # Update threshold for next level
            leveled = True
        return leveled

    def level_up(self) -> None:
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.base_attack += 2
        self.base_defense += 2
        self.reset_temporary_stats()
        print(f"🎉 {self.name} reached level {self.level}! +2 ATK, +2 DEF.")

        # Unlock new cards if any
        if self.level in Player.CARD_UNLOCKS:
            self.offer_card_choice(Player.CARD_UNLOCKS[self.level])

    def offer_card_choice(self, options: list):
        # Filter out cards already unlocked
        new_options = [c for c in options if c.name not in self.unlocked_cards]
        if not new_options:
            print("\n🎁 No new cards available at this level. You've unlocked them all.")
            return

        print("\n📦 Choose one of the following new cards to add to your deck:\n")
        for i, card in enumerate(new_options, 1):
            print(f"{i}. {card.name} - {card.description} (Cost: {card.energy_cost})")

        while True:
            choice = input("Enter the number of the card to add: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(new_options):
                selected = new_options[int(choice) - 1]
                self.deck.append(selected)
                self.unlocked_cards.add(selected.name)  # Track unlock
                print(f"✅ Added {selected.name} to your deck!")
                break
            else:
                print("Invalid choice. Try again.")



    def earn_money(self, amount: int) -> None:
        self.money += amount

    def spend_money(self, amount: int) -> bool:
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def xp_left_to_level_up(self) -> int:
        if self.level - 1 < len(Player.XP_THRESHOLDS):
            return Player.XP_THRESHOLDS[self.level - 1]
        return Player.DEFAULT_XP_THRESHOLD
    
    def __str__(self):
        return (f"[Player] {self.name} | HP: {self.health}/{self.max_health} | "
            f"Energy: {self.energy}/{self.max_energy} | Level: {self.level}")

