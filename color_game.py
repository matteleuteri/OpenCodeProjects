import random
import sys

COLORS = {
    'red': '\033[41m',
    'green': '\033[42m',
    'blue': '\033[44m',
    'yellow': '\033[43m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
}
RESET = '\033[0m'
GRID_SIZE = 20

def main():
    color_names = list(COLORS.keys())
    cells = [random.choice(color_names) for _ in range(GRID_SIZE * GRID_SIZE)]
    most_common = max(set(color_names), key=lambda c: cells.count(c))

    # Display grid
    for i, color in enumerate(cells):
        if i % GRID_SIZE == 0:
            sys.stdout.write('\n')
        sys.stdout.write(COLORS[color] + ' ' + RESET)

    sys.stdout.flush()
    color_options = ', '.join(COLORS.keys())
    print(f'\n\nWhat was the most common color? ({color_options}): ', end='')
    guess = input().lower()

    if guess == most_common:
        print(f'\033[1mCorrect! It was {most_common}.\033[0m')
    else:
        print(f'Wrong, it was {most_common}.')

if __name__ == '__main__':
    main()