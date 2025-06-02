from utils import clear, typing
from modules.lore_manager import LoreManager
import time

def show_intro(lore_path="data/lore.json"):
    clear()
    lore_manager = LoreManager(lore_path)
    intro_lines = lore_manager.get_entries_by_category("into_lore")

    print("=" * 60)
    print("🌍  WELCOME  🌍".center(60))
    print("=" * 60)

    while True:
        choice = input("\nWould you like to watch the prologue? (Y/n): ").strip().lower()
        if choice in ("", "y", "yes"):
            break
        elif choice in ("n", "no"):
            print("\nSkipping prologue...\n")
            time.sleep(1)
            clear()
            return
        else:
            print("Please enter Y or N.")

    input("\n[Press ENTER to begin the prologue...]\n")

    for entry in intro_lines:
        if entry.content.strip() == "":
            print()
            time.sleep(1)
        else:
            typing(entry.content, type="narration", delay=0.030)
            time.sleep(1.3)

    print("\n" + "-" * 60)
    input("🧠 Remember: survival is earned. Press ENTER to continue...")
    clear()
