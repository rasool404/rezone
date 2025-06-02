import time
import sys

def progress_bar(total=100, width=50):
    for i in range(total + 1):
        filled = int(width * i / total)
        bar = '█' * filled + '-' * (width - filled)
        sys.stdout.write(f'\r|{bar}| {i}%')
        sys.stdout.flush()
        time.sleep(0.02)
    print()
