
from modules.game_engine import Game
from utils import clear

def main():
    try:
        game = Game()
        game.start_game()

    except KeyboardInterrupt:
        clear()
        game.save_game()
        print(f"\n\n\n[INFO]: Application was interrupted by user. Data saved")

if __name__ == "__main__":
    main()
