import random
import time
import sys
from pyfiglet import Figlet

def ascii(text, 
          font='doom', 
          noise_level=0.03, 
          erosion_level=0.01, 
          crack_count=3, 
          animate=True, 
          delay=0.05):
    """
    Generate a post-apocalyptic-style ASCII art from input text.

    Args:
        text (str): The text to render.
        font (str): A pyfiglet font name.
        noise_level (float): Fraction of chars to turn into noise.
        erosion_level (float): Fraction of chars to erase.
        crack_count (int): Number of cracks to overlay.
        animate (bool): Whether to animate the output.
        delay (float): Delay in seconds between lines.
    """
    fig = Figlet(font=font)
    raw = fig.renderText(text).splitlines()

    noisy = []
    noise_chars = ['#', '%', '@', '&', '?', '/', '\\', '|']
    for line in raw:
        new_line = []
        for ch in line:
            r = random.random()
            if r < erosion_level:
                new_line.append(' ')
            elif r < erosion_level + noise_level:
                new_line.append(random.choice(noise_chars))
            else:
                new_line.append(ch)
        noisy.append(new_line)

    height = len(noisy)
    width = max(len(row) for row in noisy)

    for row in noisy:
        row.extend(' ' * (width - len(row)))

    for _ in range(crack_count):
        y = random.randrange(height)
        x = random.randrange(width)
        length = random.randint(3, max(3, width // 10))
        direction = random.choice(['h', 'v', 'd1', 'd2'])
        for i in range(length):
            yy, xx = y, x
            if direction == 'h':
                xx = x + i
            elif direction == 'v':
                yy = y + i
            elif direction == 'd1':
                yy = y + i; xx = x + i
            else:
                yy = y + i; xx = x - i
            if 0 <= yy < height and 0 <= xx < width:
                noisy[yy][xx] = random.choice(['/', '\\', '|', '-'])

    if animate:
        for row in noisy:
            print("".join(row))
            time.sleep(delay)
    else:
        print("\n".join("".join(row) for row in noisy))
