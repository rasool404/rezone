import time
import tkinter as tk
from utils import typing, clear, ascii
from components import start, bunker, game_map, display_player_stats, inventory, show_intro
from .bot import Bot
from .lore_manager import LoreManager
from .player import Player
from .data_manager import DataManager
from .task_manager import TaskManager
from .location import LocationManager
from .task_manager_gui import TaskManagerGUI

class Game:
    def __init__(self):
        # Initialize core systems
        self.data_manager = DataManager()
        self.lore_manager = LoreManager("data/lore.json")
        self.task_manager = TaskManager("saves/tasks.json")
        self.location_manager = LocationManager("data/locations.json")

        self.player: Player = None
        self.bot = Bot()

        # Determine whether to load an existing save
        self.first_run = not self.data_manager.has_saved_game()
        if not self.first_run:
            self.load_game()

        self.running = True
        self.state = "bunker"

    def start_game(self):
        start() # Show loader and game logo
        if self.first_run: # If player does not have saved progress then this part of the code executes
            show_intro(self.lore_manager.json_path)
            name = input("\nEnter your character's name: ").strip()
            if not name:
                print("Name cannot be empty.")
                return
            self.player = Player(name)
            self.bot.speak(f"Hello, {self.player.name}. Welcome to the bunker!")
        else:
            print("\n\n\n")
            self.bot.speak(f"Welcome back, {self.player.name}")

        self.game_loop()

    def save_game(self):
        """Save player progress and location states"""
        if self.player is None:
            print("No player data to save.")
            return False

        # Gather player data
        player_data = {
            "name": self.player.name,
            "level": self.player.level,
            "xp": self.player.xp,
            "health": self.player.health,
            "max_health": self.player.max_health,
            "attack": self.player.attack,
            "defense": self.player.defense,
            "energy": self.player.energy,
            "money": self.player.money,
            "inventory": self.player.inventory,
            "unlocked_cards": list(self.player.unlocked_cards),
        }

        # Gather location progress
        location_states = {}
        for loc_id, loc in self.location_manager.locations.items():
            status = loc.get_completion_status()
            status["defeated_enemy_names"] = [e.name for e in loc.enemies_defeated]
            location_states[loc_id] = status

        return self.data_manager.save_progress(player_data, location_states)

    def load_game(self):
        """Load player progress and restore location states"""
        saved = self.data_manager.load_progress()
        if not saved:
            return False

        # Restore player
        player_data = saved.get("player", {})
        if self.player is None:
            self.player = Player(player_data.get("name", "Survivor"))

        self.player.name = player_data.get("name", self.player.name)
        self.player.level = player_data.get("level", self.player.level)
        self.player.xp = player_data.get("xp", self.player.xp)
        self.player.health = player_data.get("health", self.player.health)
        self.player.max_health = player_data.get("max_health", self.player.max_health)
        self.player.attack = player_data.get("attack", self.player.attack)
        self.player.defense = player_data.get("defense", self.player.defense)
        self.player.energy = player_data.get("energy", self.player.energy)
        self.player.money = player_data.get("money", self.player.money)
        self.player.inventory = player_data.get("inventory", self.player.inventory)
        self.player.unlocked_cards = set(player_data.get("unlocked_cards", []))

        # Restore location states
        saved_locations = saved.get("locations", {})
        for loc_id_str, state in saved_locations.items():
            try:
                loc_id = int(loc_id_str)
            except ValueError:
                continue
            loc = self.location_manager.locations.get(loc_id)
            if not loc:
                continue
            defeated_names = state.get("defeated_enemy_names", [])
            loc.enemies_defeated = [e for e in loc.enemies if e.name in defeated_names]
            loc.boss_defeated = state.get("boss_defeated", loc.boss_defeated)
            loc.is_completed = state.get("is_completed", loc.is_completed)

        return True

    def game_loop(self):
        """Main game loop"""
        print("\nStarting game loop...")
        while self.running:
            if self.state == 'bunker':
                bunker(self)
            elif self.state == 'explore':
                clear()
                print("\n\n")
                ascii("M A P", font="doom")
                time.sleep(2)
                game_map(self)
            elif self.state == 'task-manager':
                clear()
                print("\n\nRunning computer...")
                root = tk.Tk()
                gui = TaskManagerGUI(root, self.task_manager, self)
                root.mainloop()
                self.state = 'bunker'
            elif self.state == 'stats':
                clear()
                display_player_stats(self)
            elif self.state == 'inventory':
                clear()
                print("\n\n")
                ascii("I N V E N T O R Y", font="doom")
                time.sleep(2)
                inventory(self)
            elif self.state == 'bed':
                clear()
                print("\n\n\n")
                typing("🛌 You rest in bed and your energy level is fully restored!")
                self.player.energy = self.player.max_energy
                input("Press ENTER to leave bed and return to bunker...")
                self.state = 'bunker'
            elif self.state == 'quit':
                break

        typing("Quitting and Saving game....", type="info")
        self.save_game()
        print("Game saved!")
        time.sleep(2)
        clear()
