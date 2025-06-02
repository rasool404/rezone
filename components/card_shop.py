from utils import clear
from modules.cards import AttackCard, UtilityCard, DefenseCard
from modules.player import StatusEffect
from modules.items import CardItem

def card_shop(engine):
    player = engine.player
    inv_manager = player.inventory_manager

    all_shop_cards = [
        ("Slice", 15, "Deal 7 damage.", lambda: AttackCard("Slice", 1, 7, "Deal 7 damage.")),
        ("Adrenaline", 25, "Gain 2 energy.", lambda: UtilityCard("Adrenaline", 1, lambda s, t: setattr(s, "energy", min(s.max_energy, s.energy + 2)), "Gain 2 energy.")),
        ("Shield Boost", 20, "Gain 8 defense.", lambda: DefenseCard("Shield Boost", 1, 8, "Gain 8 defense.")),
        ("Toxic Slash", 30, "Deal 6 damage and apply poison.", lambda: UtilityCard("Toxic Slash", 2, lambda s, t: t.add_status_effect(StatusEffect.POISONED, 2, 2), "Deal 6 damage and poison.")),
    ]

    available = [c for c in all_shop_cards if c[0] not in player.unlocked_cards]
    if not available:
        print("🛒 No new cards available. You've unlocked all shop cards.")
        input("Press ENTER to return...")
        engine.state = 'bunker'
        return

    clear()
    print("=== Card Shop ===")
    print(f"Money: ${player.money}")
    print("Available cards:")

    for i, (name, cost, desc, _) in enumerate(available, 1):
        print(f"{i}. {name} (${cost}) - {desc}")
    print("0. Return to bunker")

    choice = input("Choose a card number to buy: ").strip()
    if choice == "0":
        engine.state = 'bunker'
        return

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(available):
            name, cost, desc, factory = available[index]
            if player.money < cost:
                print("❌ Not enough money!")
            else:
                card = factory()
                item = CardItem(card)
                inv_manager.add_item(item)
                player.unlocked_cards.add(name)
                player.spend_money(cost)
                print(f"✅ You purchased {name}! It’s added to your inventory.")
        else:
            print("Invalid choice.")
    else:
        print("Invalid input.")

    input("Press ENTER to return to bunker...")
    engine.state = 'bunker'
