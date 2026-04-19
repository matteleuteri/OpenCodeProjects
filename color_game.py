import random
import sys
import time
from collections import Counter

COLORS = {
    'red': '\033[41m',
    'green': '\033[42m',
    'blue': '\033[44m',
    'yellow': '\033[43m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
}
RESET = '\033[0m'

def get_grid_size():
    print("Select difficulty:")
    print("1. Easy (10x10)")
    print("2. Medium (20x20)")
    print("3. Hard (30x30)")
    choice = input("Choice (1-3): ").strip()
    
    sizes = {'1': 10, '2': 20, '3': 30}
    if choice in sizes:
        return sizes[choice]
    return 20

def main():
    grid_size = get_grid_size()
    color_names = list(COLORS.keys())
    cells = [random.choice(color_names) for _ in range(grid_size * grid_size)]
    
    color_counts = Counter(cells)
    most_common = color_counts.most_common(1)[0][0]

    for i, color in enumerate(cells):
        if i % grid_size == 0:
            sys.stdout.write('\n')
        sys.stdout.write(COLORS[color] + ' ' + RESET)

    sys.stdout.flush()
    color_options = ', '.join(COLORS.keys())
    print(f'\n\nWhat was the most common color? ({color_options}): ', end='')
    guess = input().lower()

    counts_str = ', '.join(f"{color}: {count}" for color, count in sorted(color_counts.items()))
    
    sorted_colors = [c for c, _ in color_counts.most_common()[::-1]]
    
    if guess == most_common:
        result = f'\033[1mCorrect! It was {most_common}.\033[0m'
    else:
        result = f'Wrong, it was {most_common}.'
    
    print('\x1b[2J\x1b[H', end='')
    print(result)
    print("Revealing...\n")
    
    blacked_out = set()
    for color in sorted_colors[:-1]:
        blacked_out.add(color)
        sys.stdout.write('\x1b[2J\x1b[H')
        sys.stdout.write(result + '\n')
        sys.stdout.write("Revealing...\n\n")
        for i, c in enumerate(cells):
            if i % grid_size == 0:
                sys.stdout.write('\n')
            if c in blacked_out:
                sys.stdout.write('\033[40m' + ' ' + RESET)
            else:
                sys.stdout.write(COLORS.get(c, '') + ' ' + RESET)
        sys.stdout.flush()
        time.sleep(0.5)
    
    print(f"\n\nCounts: {counts_str}")

if __name__ == '__main__':
    main()
