from utils import clear, ascii_bar
from .deck import deck_preview


def display_player_stats(engine):
    while engine.state == "stats":
        clear()
        player = engine.player

        # Header
        print("=== Player Stats ===\n")

        # Basic Info
        print(f"Name:    {player.name}")
        print(f"Level:   {player.level}")

        # XP Bar
        current_xp = player.xp
        total_xp = player.get_xp_threshold()
        print(ascii_bar("XP", current_xp, total_xp))
        # Health & Energy Bars
        print(ascii_bar("Health", player.health, player.max_health))
        print(ascii_bar("Energy", player.energy, player.max_energy, fill_char="*"))

        # Core Stats
        print(f"\nAttack:  {player.attack}")
        print(f"Defense: {player.defense}")
        print(f"Money:   ${player.money}")


        print("\nOptions:")
        print("1. View Deck")
        print("0. Return to Bunker")

        choice = input("\nYour choice: ").strip()
        if choice == "1":
            deck_preview(engine)
        else:
            engine.state = 'bunker'
