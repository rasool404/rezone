# 🎴 RE:ZONE – A Post-Apocalyptic Deckbuilder RPG

RE:ZONE is a text-based, deckbuilding RPG built entirely in Python. It combines real-world task management, classic deckbuilding combat, and a rich post-apocalyptic world driven by dynamic AI and immersive lore.

# 🚀 How to Run

## Installation & Setup

1. **Clone or download the project**
   ```bash
   git clone https://github.com/rasool404/rezone
   cd rezone
   ```

2. **Install dependencies**
   ```bash
   pip install -r reqs.txt
   ```
   Required libraries:
   - `pyfiglet` (ASCII art generation)

3. **Run the game**
   ```bash
   python main.py
   ```

4. **First time setup**
   - The game will create save directories automatically
   - Enter your character name when prompted
   - Enjoy the prologue and start your post-apocalyptic adventure!

## Controls
- Use number keys to select menu options
- Follow on-screen prompts for combat and navigation
- Access the task manager GUI through the bunker menu

---

# 🌟 Overview

- **Genre:** Deckbuilding RPG (text-based, ASCII visuals)
- **Setting:** A world devastated by nuclear war, with survivors scraping by in bunkers
- **Core Loop:**
  1. Explore dangerous zones
  2. Battle enemies and bosses
  3. Return to the bunker to rest, buy cards/potions, and manage real-life tasks
  4. Level up and build your ultimate deck

---

# 🧠 Major Game Features

### ✅ Card-Based Combat
- Players hold a hand of 3 cards, drawing 1 new card at the start of each turn
- Cards cost energy (stamina)
- Use cards wisely—if you run out of energy, retreat to the bunker to rest!
- **Card types:**
  - **Attack:** Deal direct damage
  - **Defense:** Temporary, 1-turn shields
  - **Utility:** Buffs, debuffs, status effects

### ✅ Zone Exploration
- Zones are defined in `locations.json`
- Each zone has a unique theme, enemies, and a final boss
- Enemies adapt their actions based on your health and theirs

### ✅ Inventory & Shop
- Buy cards, health potions, and manage your loadout
- Health potions come in small, medium, and large, restoring different amounts of HP

### ✅ Real-Life Task Manager
- A gamified task manager (using `TaskManagerGUI`) for real-world productivity
- Completing real tasks rewards you with in-game money
- Missing tasks costs you HP!

### ✅ Player Progression
- Earn XP to level up
- Each level grants new cards to unlock
- Stats increase (+2 ATK, +2 DEF, +10 HP) per level

### ✅ ASCII Visuals
- All text output uses ASCII art and effects for immersion

### ✅ Save/Load
- Game state is saved in JSON (`progress.json`, `tasks.json`) and auto-loaded

### ✅ Immersive Lore
- Rich backstory and world-building in `lore.json`
- The AI bot "ARIA" shares random lore snippets dynamically

---

# 🏗️ Project Structure & Flow

```
rezone/
├── main.py                 # Starts the game, main loop
├── modules/                # Core logic & data models
│   ├── game_engine.py      # Main game engine
│   ├── player.py           # Player stats, deck, progression
│   ├── enemy.py            # Enemies, including raiders, mutants, bosses
│   ├── battle_manager.py   # Combat loop and interactions
│   ├── inventory_manager.py# Item handling, adding/removing items
│   ├── location.py         # Zone definitions, enemy rotations
│   ├── data_manager.py     # Saving/loading game progress
│   ├── cards.py            # Card classes: Attack, Defense, Utility
│   ├── items.py            # Inventory items (CardItems, Consumables)
│   ├── lore_manager.py     # Loading and serving lore snippets
│   ├── task_manager.py     # Real-life task handling
│   ├── task_base.py        # Abstract task definition
│   ├── simple_task.py      # Single-instance tasks
│   ├── daily_task.py       # Daily recurring tasks
│   ├── task_manager_gui.py # Tkinter-based GUI for task management
│   ├── bot.py              # AI bot ARIA
│   └── exceptions.py       # Custom error classes
├── components/             # Bunker, map, inventory, start flow
├── utils/                  # ASCII effects, terminal tools
├── data/                   # JSON data: lore, locations, ASCII art
├── saves/                  # Save files
├── reqs.txt                # Required libraries (pyfiglet)
└── README.md               # This file!
```

# ⚙️ Core Gameplay Systems & Code Flow

### 🔥 Game Loop (`game_engine.py` → `Game` class)

The heart of the game:
- Starts with `start_game()`, showing the prologue and getting your name
- **Main loop:** Controlled by the `self.state` variable. States include:
  - `bunker`
  - `explore`
  - `task-manager`
  - `stats`
  - `inventory`
  - `bed`
- Each state triggers a different UI component from `components/` (e.g., `bunker.py` for safehouse actions)

---

### ⚔️ Combat System (`battle_manager.py`)

Starts with `start_battle()`:

1. **Player turn:**
   - Pick a card by index
   - Check energy/stamina
   - Use it (resolves damage, healing, or buffs)

2. **Enemy turn:**
   - Uses enemy-specific AI in `enemy.py`
   - Can attack, defend, or (for bosses) use Utility cards

**Combat mechanics:**
- Cards cost energy. Run out → go back to bunker
- **Dynamic enemy AI:**
  - **Raider:** Defends more at low HP
  - **Mutant:** More aggressive as it weakens
  - **Boss:** Can buff itself or burn/poison you
- Defense only lasts 1 turn—reset at the start of each turn
- **Victory:** Gain XP and level up if threshold met (`gain_xp()` in `player.py`)
- **Death:** Respawn with 5 HP and zero balance

---

### 🃏 Deck & Card System (`cards.py`, `player.py`)

- 3-card hand at a time
- After playing a card → draw 1 new card from deck
- Deck reshuffles from discard pile when empty
- Starter deck includes strikes, guards, and utilities (like Focus and Regenerate)
- Level-up unlocks new cards (e.g., Overclock, Exploit Weakness)

---

### 🛍️ Inventory & Shop (`inventory.py`, `card_shop.py`)

- Buy health potions (small/medium/large)
- Card shop sells new cards once unlocked by level
- Manage deck: Move cards in/out of your deck

---

### 🛌 Bunker & Bed Rest (`bunker.py`)

- If stamina is 0, go to bed
- Bed fully restores your stamina
- Return to battle-ready!

---

### 💀 Enemies (`enemy.py`)

- **Base:** `Enemy` (inherits `Character`)
- **Raiders:** Use "Brace" defense at low HP
- **Mutants:** Use "Frenzy" for higher damage at low HP
- **Bosses:**
  - Use `UtilityCards` like "Battle Roar" for +3 ATK for 3 turns
  - Use "Corrosive Shout" to poison the player

---

### 🧾 Real-Life Task System (`task_manager.py` + `task_manager_gui.py`)

- **Add real-life tasks:**
  - Simple Tasks (can expire)
  - Daily Tasks (reset each day)
- Completing tasks gives in-game money!
- Missing tasks costs 10 HP
- **GUI built with Tkinter:**
  - View tasks
  - Mark as complete
  - See task stats (completed/pending/expired)

---

### 💾 Save & Load (`data_manager.py`)

- Auto-saves on exit
- **Tracks:**
  - Player stats, deck, money
  - Location completion (boss defeated?)
  - Task progress
- Data stored in JSON (`progress.json`, `tasks.json`)

---

### 📚 Immersive Lore (`lore_manager.py`, `lore.json`)

- Prologue on first launch (text-based cinematic)
- Random lore snippets shared by ARIA (the AI bot) when bored
- **Categories in JSON:**
  - `intro_lore`: Opening world story
  - `ai_random_lore`: ARIA's sarcastic commentary

---

### 🎨 ASCII Art & Visuals (`ascii_text.py`, `ascii_bar.py`)

- Uses `pyfiglet` for ASCII banners (`ascii()` function)
- Adds noise & cracks for a post-apocalyptic effect
- ASCII progress bars for HP, energy, and XP
- All UI is in the terminal—no graphics—but immersive!

---

# 🧱 Object-Oriented Programming (OOP) Concepts

| Principle | Implementation |
|-----------|----------------|
| **Abstraction** | Abstract base classes: `Card`, `Character`, `Item`, `Task` |
| **Encapsulation** | Controlled access to attributes and internal state |
| **Inheritance** | Deep hierarchy (e.g., `Character` → `Player`, `Enemy`, etc.) |
| **Polymorphism** | Overridden methods like `use()`, `__str__()`, `get_next_action()` |
| **Operator Overloading** | Example: `__str__()` in `Character`, `Player`, `Enemy` classes |
| **Data-Driven** | Zones, enemies, and lore loaded from JSON |
| **State Pattern** | Game state transitions (bunker, explore, etc.) control flow |
| **Factory Pattern** | Card creation in the shop uses factory-like lambda functions |
| **Strategy Pattern** | Enemy AI adapts to player/enemy HP (different `get_next_action()` methods) |
| **Observer Pattern** | Task manager uses event handlers for task updates |
| **Template Method** | Abstract `Card.use()` method, implemented by each card type |

---

# 👥 Authors

- Khalimov Rasuljon (12244991)
- Ibragimov Asadbek (12245008)
- Naizabekov Asfendiyar (12245009)
- Bolk Ankhbayar (12245013)
- Shurenbayev Orazbek (12245021)