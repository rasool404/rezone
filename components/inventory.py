from utils import clear
from .deck import deck_preview
from .card_shop import card_shop
from modules.items import CardItem

def inventory(engine):
    player = engine.player

    while engine.state == "inventory":
        clear()
        print("=== Inventory & Shop ===")
        print(f"Player: {player.name}")
        print(f"Health: {player.health}/{player.max_health} HP")
        print(f"Money: ${player.money}\n")

        if player.health >= player.max_health:
            print("Your health is already full. No healing items needed.")

        print("\nOptions:")
        print("1. Buy Health Item")
        print("2. Open Card Shop")
        print("3. View Deck")
        print("4. Manage Deck")
        print("0. Return to Bunker")

        choice = input("\nYour choice: ").strip()

        if choice == "0":
            engine.state = "bunker"
            break

        elif choice == "1":
            if player.health >= player.max_health:
                print("You’re already at full health.")
                input("Press ENTER to continue...")
                continue

            marketplace_items = [
                ("Small Health Potion", 10, 10),
                ("Medium Health Potion", 25, 20),
                ("Large Health Potion", 45, 30),
            ]
            for i, (name, cost, restore) in enumerate(marketplace_items, 1):
                print(f"{i}. {name} - ${cost}, Restores {restore} HP")
            print("0. Cancel")

            sub = input("\nChoose item: ").strip()
            if sub == "0":
                continue
            if sub.isdigit():
                idx = int(sub) - 1
                if 0 <= idx < len(marketplace_items):
                    name, cost, restore = marketplace_items[idx]
                    if player.money >= cost:
                        player.spend_money(cost)
                        player.health = min(player.max_health, player.health + restore)
                        print(f"✅ You used {name}.")
                    else:
                        print("Not enough money.")
                else:
                    print("Invalid option.")
            input("Press ENTER to continue...")

        elif choice == "2":
            card_shop(engine)

        elif choice == "3":
            deck_preview(engine)

        elif choice == "4":
            manage_deck(engine)

        else:
            print("Invalid input.")
            input("Press ENTER to continue...")


def manage_deck(engine):
    player = engine.player
    inv_manager = player.inventory_manager

    while True:
        clear()
        print("=== Manage Deck ===")

        print("\nDeck:")
        for i, card in enumerate(player.deck, 1):
            print(f"{i}. {card.name} - {card.description}")

        print("\nInventory (Card Items):")
        card_items = inv_manager.get_items_by_type(CardItem)
        for i, item in enumerate(card_items, 1):
            print(f"{i}. {item.card.name} - {item.card.description}")

        print("\nOptions:")
        print("1. Add card from inventory to deck")
        print("2. Remove card from deck to inventory")
        print("0. Done")

        choice = input("\nChoose an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            if not card_items:
                input("No cards in inventory. Press ENTER to continue...")
                continue
            idx = input("Enter inventory card number to add: ").strip()
            if idx.isdigit():
                idx = int(idx) - 1
                if 0 <= idx < len(card_items):
                    item = card_items[idx]
                    player.deck.append(item.card)
                    inv_manager.remove_item(item)
                    print(f"✅ {item.card.name} added to deck.")
                else:
                    print("Invalid selection.")
            input("Press ENTER to continue...")

        elif choice == "2":
            if not player.deck:
                input("Deck is empty. Press ENTER to continue...")
                continue
            idx = input("Enter deck card number to remove: ").strip()
            if idx.isdigit():
                idx = int(idx) - 1
                if 0 <= idx < len(player.deck):
                    card = player.deck.pop(idx)
                    inv_manager.add_item(CardItem(card))
                    print(f"✅ {card.name} moved to inventory.")
                else:
                    print("Invalid selection.")
            input("Press ENTER to continue...")

        else:
            print("Invalid input.")
            input("Press ENTER to continue...")
