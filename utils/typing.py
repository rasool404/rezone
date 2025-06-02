import sys
import time

def typing(text, type="narration", delay=0.05):
    label = "[INFO]: " if type.lower() == "info" else "[NARRATION]: "
    sys.stdout.write(label)
    sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  
