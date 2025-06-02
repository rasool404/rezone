import time
from utils import typing, clear, ascii
from modules.battle_manager import BattleManager
from modules.enemy import Boss


def display_enemy_info(enemy):
    is_boss = isinstance(enemy, Boss)
    header = "=== 🚨 BOSS ENEMY ===" if is_boss else "=== Enemy Information ==="
    name_lbl = f"[BOSS] {enemy.name}" if is_boss else enemy.name

    print(f"\n{header}")
    print(f"Name:   {name_lbl}")
    print(f"Health: {enemy.health}/{enemy.max_health}")
    print(f"Attack: {enemy.attack}")
    print(f"Defense: {enemy.defense}")
    print(f"Type:   {'Boss' if is_boss else 'Standard Enemy'}")

    print("\n⚔️ Enemy will use themed actions based on situation (no deck shown).")
    print("-" * 40)



def game_map(engine):
    while engine.state == 'explore':
        clear()
        print("=== Available Locations ===\n")
        locations = engine.location_manager.get_all_locations()

        for idx, location in enumerate(locations, start=1):
            print(f"{idx}. Name: {location.name}")
            print(f"   Level: {location.level}")
            print(f"   Completed: {'Yes' if location.is_completed else 'No'}")
            print("-" * 40)

        print("Enter the number of the location to enter it (or 0 to return to bunker).")
        user_input = input("Your choice: ")

        if user_input == "0":
            engine.state = 'bunker'
            return

        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(locations):
                selected = locations[index]
                result = engine.location_manager.enter_location(selected, engine.player.level)
                if result == "success":
                    while True:
                        clear()
                        info = selected
                        print(f"=== Entered: {info.name} ===")
                        print(f"Level: {info.level}")
                        print(f"Description: {info.description}")
                        print(f"Enemies Defeated: {len(info.enemies_defeated)}/{len(info.enemies)}")
                        print(f"Boss Defeated: {'Yes' if info.boss_defeated else 'No'}")
                        print("-" * 40)

                        next_enemy = selected.get_next_enemy()
                        if not next_enemy:
                            print("\n🎉 Location cleared! Returning to bunker...")
                            engine.state = 'bunker'
                            return

                        display_enemy_info(next_enemy)
                        choice = input("Do you want to [F]ight this enemy or [R]eturn to bunker? ").strip().lower()
                        if choice == 'r':
                            engine.state = 'bunker'
                            return
                        elif choice == 'f':
                            # Use the current location's XP threshold
                            xp_thresh = selected.xp_threshold
                            battle_manager = BattleManager(engine.player, next_enemy, xp_thresh)
                            victory = battle_manager.start_battle()

                            if victory:
                                print(f"\n✅ You defeated {next_enemy.name}!")
                                selected.mark_enemy_defeated(next_enemy)

                                if selected.is_completed:
                                    print("\n🎉 Congratulations! You completed this location!")
                                    input("Press ENTER to return to bunker...")
                                    engine.state = 'bunker'
                                    return
                                else:
                                    next_choice = input("\nDo you want to [C]ontinue to next enemy or [R]eturn to bunker? ").strip().lower()
                                    if next_choice == 'r':
                                        engine.state = 'bunker'
                                        return
                            else:
                                print("\n❌ You were defeated. Returning to bunker...")
                                input("Press ENTER to continue...")
                                engine.state = 'bunker'
                                return
                        else:
                            print("Invalid choice. Please type F or R.")
                            input("Press ENTER to continue...")
                elif result == "level_mismatch":
                    typing(f"You cannot enter {selected.name} yet. Required level: {selected.level}", type="info")
                    input("Press ENTER to continue...")
                elif result == "already_completed":
                    typing(f"You have already completed {selected.name}.", type="info")
                    input("Press ENTER to continue...")
                else:
                    typing("Something went wrong. Please try again.\n", type="info")
                    input("Press ENTER to continue...")
            else:
                print("Invalid location number. Try again.")
                input("Press ENTER to continue...")
        else:
            print("Invalid input. Please enter a number.")
            input("Press ENTER to continue...")