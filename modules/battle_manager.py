from .cards import Card, AttackCard, DefenseCard, UtilityCard
from .player import Player
from .enemy import Enemy, Boss
from utils import clear, ascii_bar

class BattleManager:
    def __init__(self, player: Player, enemy: Enemy, xp_threshold: int):
        self.player = player
        self.enemy = enemy
        self.xp_threshold = xp_threshold
        self.turn_count = 1

    def start_battle(self) -> bool:
        """Start the battle and return True if player wins."""
        clear()
        # Show a special header if this is the boss
        if isinstance(self.enemy, Boss):
            enemy_label = f"🚨 BOSS: {self.enemy.name} 🚨"
        else:
            enemy_label = self.enemy.name
        print(f"\n🔔 Battle Start: {self.player.name} vs {enemy_label}!")
        input("Press ENTER to begin…")

        while True:
            # Player's turn
            if not self._player_turn():
                # Player surrendered
                self._end_battle_cleanup()
                print("Redirecting to bunker...")
                return False

            # Check if enemy defeated
            if self.enemy.health <= 0:
                self._handle_victory()
                self._end_battle_cleanup()
                return True

            # Enemy's turn
            if not self._enemy_turn():
                # Rare case: enemy cannot act? treat as loss
                self._end_battle_cleanup()
                print("Redirecting to bunker...")
                return False

            # Check if player is defeated
            if self.player.health <= 0:
                clear()
                print(f"\n💀 {self.player.name} has been defeated!")
                # Restore health and confiscate money
                self.player.health = 5
                self.player.money = 0
                self._end_battle_cleanup()
                print("Redirecting to bunker...")
                return False

            self.turn_count += 1

    def _player_turn(self) -> bool:
        clear()
        self.player.reset_temporary_stats()

        # Clear combo memory
        if hasattr(self.player, "last_card_tag"):
            del self.player.last_card_tag

        if not self.player.hand:
            self.player.draw_cards(3)

        self._render_battle_screen()     

        while True:
            choice = input("\nChoose a card number (or 'q' to surrender): ").strip().lower()
            if choice == 'q':
                return False
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.player.hand):
                    card = self.player.hand[idx]
                    if self.player.energy < card.energy_cost:
                        print("❌ Not enough energy!")
                        continue
                    played = self.player.hand.pop(idx)
                    self._resolve_card(played, self.player, self.enemy)
                    input("\nPress ENTER to end your turn...")
                    break
            print("Invalid choice—please enter a valid card number or 'q'.")

        # End-of-turn effects
        self.player.update_status_effects()
        return True

    def _enemy_turn(self) -> bool:
        clear()
        print(f"\n--- Enemy Turn #{self.turn_count} ---")
        self._render_battle_screen(show_hand=False)

        card = self.enemy.get_next_action(self.player)

        print(f"\n🤖 {self.enemy.name} uses {card.name}!")

        self._resolve_card(card, self.enemy, self.player)

        self.enemy.update_status_effects()
        input("\nPress ENTER to continue…")
        return True

    def _resolve_card(self, card: Card, source, target) -> None:
        if not source.can_act():
            print(f"{source.name} cannot act!")
            return

        if isinstance(source, Player):
            source.energy -= card.energy_cost

        result = card.use(source, target)

        if isinstance(source, Player):
            source.discard_pile.append(card)

        if isinstance(source, Player):
            source.draw_cards(1)

        if isinstance(card, AttackCard):
            raw = card.damage + source.attack
            reduction = target.defense
            print(f"➡️ {card.name} would deal {raw} damage.")
            print(f"🛡️ {target.name} reduces it by {reduction} defense.")
            print(f"💥 {target.name} takes {result} damage.")

        elif isinstance(card, DefenseCard):
            before = source.defense - card.defense  # since defense already updated
            after = source.defense
            print(f"🛡️ {card.name} used.")
            print(f"🔰 {source.name}'s defense increased: {before} -> {after} (+{card.defense})")
        elif isinstance(card, UtilityCard):
            print(f"✨ {source.name} uses {card.name} — {card.description}")

        

    def _handle_victory(self) -> None:
        clear()
        if isinstance(self.enemy, Boss):
            print(f"\n🎉 You have slain the BOSS: {self.enemy.name}!")
        else:
            print(f"\n🏆 {self.enemy.name} has been defeated!")
        leveled = self.player.gain_xp(self.enemy.exp_reward, self.xp_threshold)
        print(f"Gained {self.enemy.exp_reward} XP!")
        if leveled:
            print(f"🎊 Level Up! {self.player.name} is now level {self.player.level}!")
        input("\nPress ENTER to continue…")

    def _end_battle_cleanup(self) -> None:
        """Reset player deck state after battle ends."""
        self.player.status_effects.clear()
        self.enemy.status_effects.clear()

        # Restore all cards back into deck
        self.player.deck.extend(self.player.hand)
        self.player.deck.extend(self.player.discard_pile)
        self.player.hand.clear()
        self.player.discard_pile.clear()


    def _render_battle_screen(self, show_hand: bool = True) -> None:
        print("\n" + "="*50)
        print(f"🎯 Turn {self.turn_count:^44}")
        print("="*50)

        # Player Panel 
        print(f"\n🧍 {self.player.name}")
        print(ascii_bar("HP", self.player.health, self.player.max_health))
        print(ascii_bar("EN", self.player.energy, self.player.max_energy, fill_char="*"))
        status = ", ".join(f"{e.name}({d['duration']})" for e, d in self.player.status_effects.items()) or "None"
        print(f"Status Effects: {status}")
        print(f"🛡️  ATK: {self.player.attack} | DEF: {self.player.defense}")

        # Enemy Panel
        label = f"🚨 BOSS: {self.enemy.name}" if isinstance(self.enemy, Boss) else self.enemy.name
        print(f"\n🤖 {label}")
        print(ascii_bar("HP", self.enemy.health, self.enemy.max_health))
        estatus = ", ".join(f"{e.name}({d['duration']})" for e, d in self.enemy.status_effects.items()) or "None"
        print(f"Status Effects: {estatus}")
        print(f"🛡️  ATK: {self.enemy.attack} | DEF: {self.enemy.defense}")

        # Hand preview
        if show_hand:
            print("\n🃏 Cards in Hand:")
            for i, card in enumerate(self.player.hand, 1):
                lock = "🔒" if self.player.energy < card.energy_cost else ""
                print(f"  {i}. {card.name} (Cost: {card.energy_cost}) {lock} - {card.description}")

        print("="*50)


