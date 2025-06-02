# 🎴 RE:ZONE – A Post-Apocalyptic Deckbuilder RPG

**RE:ZONE** is a text-based, deckbuilding RPG built in Python. In a world devastated by nuclear fire, you are one of the few survivors sealed in a bunker. With only a deck of cards, your wits, and an unstable AI companion, you must explore the surface, complete tasks, and fight your way to survival.

---
 ## 🧠 Game Features

- 🃏 **Card-Based Combat** – Use Attack, Defense, and Utility cards.
- 📦 **Inventory Management** – Collect items and cards, build your loadout.
- 👾 **Zone Exploration** – Battle raiders, mutants, and rogue AI in multiple locations.
- 🤖 **AI Lore Companion** – Get immersive, sarcastic lore from a bot.
- 🧾 **Real-Time Tasks** – Complete terminal tasks to earn in-game resources.
- 💾 **Save & Load** – Your progress is automatically saved and loaded via JSON.

---

## 🧱 Object-Oriented Programming (OOP) Concepts

| Principle       | Implementation |
|-----------------|----------------|
| **Abstraction** | Abstract base classes: `Card`, `Character`, `Item`, `Task` |
| **Encapsulation** | Controlled access to attributes and internal state |
| **Inheritance** | Deep hierarchy (e.g., `Character` → `Player`, `Enemy`, etc.) |
| **Polymorphism** | Overridden methods like `use()`, `__str__()`, `get_next_action()` |
| **Operator Overloading** | Example: `__str__()` in `Character`, `Player`, `Enemy` classes |
---

## 🗂️ Project Structure

```
 rezone/
├── components/         # UI flows (bunker, deck, inventory, map)
├── modules/            # OOP structure: characters, cards, tasks, managers
├── utils/              # Terminal helpers: ascii art, typing effect, progress bar
├── data/               # JSON lore, map data, ascii art
├── saves/              # Auto-generated game saves (JSON)
├── main.py             # Entry point
├── README.md           # You're here
├── reqs.txt            # Dependencies (if any)
```
---

## 🚀 How to Run the Game

1. **Install dependencies**:
```bash
pip install -r reqs.txt
```
2. **Start the game**:
```bash
python main.py
```

---

## 📁 Save System
Game state is automatically:
- **Loaded** on startup
- **Saved** on exit
- Save files are in the `/saves/` folder:
    - `progress.json`
    - `tasks.json`

    ---

## 🧠 Design Overview

- **Modular code** with clean separation by feature
- **OOP architecture** with 30+ classes across systems
- **Data-driven design** (locations, enemies, and lore come from JSON)
- **Real-time interaction** via typing and task simulation
- **ASCII UI** for a retro-futuristic feel

---

## 🧪 Testing & Error Handling

- Custom exceptions (`DataManagerError`, `TaskManagerError`)
- Graceful shutdown with auto-saving
- Input validation and error recovery included

---

## 🎓 Educational Purpose

This project was developed as part of a group assignment in **Object-Oriented Programming** using Python. It demonstrates:
- Solid class design
- Inheritance and abstraction
- Polymorphism and operator overloading
- Modular file organization
- File-based persistence

---

## 👥 Authors

- *Khalimov Rasuljon* (12244991)
- *Ibragimov Asadbek* (12245008) 
- *Naizabekov Asfendiyar* (12245009)
- *Bolk Ankhbayar* (12245013)
- *Shurenbayev Orazbek* (12245021)
