from utils import clear
from modules.cards import CardType

def deck_preview(engine):
    player = engine.player
    clear()
    print("=== Deck Preview ===")
    
    if not player.deck:
        print("Your deck is empty.")
        input("\nPress ENTER to return...")
        engine.state = "bunker"
        return

    print(f"{len(player.deck)} cards in deck:\n")

    # Group cards by name and show details
    card_summary = {}
    for card in player.deck:
        if card.name not in card_summary:
            card_summary[card.name] = {
                "count": 1,
                "description": card.description,
                "cost": card.energy_cost,
                "type": getattr(card, "card_type", CardType.UTILITY).name.title()
            }
        else:
            card_summary[card.name]["count"] += 1

    for name, data in card_summary.items():
        print(f"{name} x{data['count']}")
        print(f"   Type: {data['type']}, Cost: {data['cost']}")
        print(f"   {data['description']}\n")

    input("Press ENTER to return...")
    engine.state = "bunker"
