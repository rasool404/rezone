from utils import clear, ascii
from data.ascii_art import bunker_inside
import time

import sys
import time
import os

if os.name == 'nt':
    import msvcrt

    def getch():
        return msvcrt.getch().decode('utf-8')

    def kbhit():
        return msvcrt.kbhit()

else:
    import tty
    import termios
    import select

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def kbhit():
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(dr)


def bunker(engine):
    while engine.state == 'bunker':
        clear()
        print(bunker_inside)
        print("[INFO]: Press a key to interact...")
        print("[INFO]: This program is better run in full screen (Alt + Enter on Windows)")

        while True:
            if kbhit():
                key = getch().lower()
                if key == 'b':
                    engine.state = "bed"
                    return
                elif key == 'r':
                    engine.bot.share_random_lore()
                    time.sleep(1)
                    break
                elif key == 's':
                    engine.state = "stats"
                    return
                elif key == 'e':
                    engine.state = "explore"
                    return
                elif key == 'i':
                    engine.state = "inventory"
                    return
                elif key == 'c':
                    engine.state = "task-manager"
                    return
                elif key == 'q':
                    engine.running = False
                    return
