import curses
import random
import time
import sys

PLAYER1_KEYS = ['a', 's', 'd', 'f']
PLAYER2_KEYS = ['j', 'k', 'l', ';']
ALL_KEYS = PLAYER1_KEYS + PLAYER2_KEYS

def load_ascii_art():
    ascii_art = {}
    for key in ALL_KEYS:
        if key == ';':
            filename = 'ascii_semicolon'
        else:
            filename = 'ascii_' + key
        try:
            with open(filename, 'r') as f:
                lines = [line.rstrip('\n') for line in f]
            ascii_art[key] = lines
        except FileNotFoundError:
            ascii_art[key] = [key]
    return ascii_art

ASCII_ART = load_ascii_art()
TARGET_HEIGHT = 25

class KeyObj:
    def __init__(self, key, start_x, speed, art):
        self.key = key
        self.x = start_x
        self.speed = speed
        self.hit = False
        self.hit_wrong = False
        self.missed = False
        self.hit_time = 0
        self.art = art
        self.art_width = max(len(line) for line in art)

    def move(self):
        self.x += self.speed

def spawn_key(speed):
    key = random.choice(ALL_KEYS)
    art = ASCII_ART[key]
    return KeyObj(key, 3, speed, art)

def get_player(key):
    if key in PLAYER1_KEYS:
        return 1
    elif key in PLAYER2_KEYS:
        return 2
    return None

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.keypad(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()

    score1 = 0
    score2 = 0
    lives1 = 10
    lives2 = 10
    speed = 0.5
    last_spawn = time.time()
    keys = []
    game_over = False
    

    while True:
        stdscr.erase()
        stdscr.addstr(0, 2, "KEY RUSH - Player 1: asdf | Player 2: jkl;")
        stdscr.addstr(1, 2, "=" * (width - 4))
        
        stdscr.addstr(2, 2, f"Player 1 (asdf): {score1}  Lives: {lives1}")
        stdscr.addstr(3, 2, f"Player 2 (jkl;): {score2}  Lives: {lives2}")
        
        stdscr.addstr(height - 3, 2, "=" * (width - 4))
        draw_y = (height // 2) - 12
        
        
        
        for k in keys:
            display_x = int(k.x)
            if 4 <= display_x <= width - 4:
                if k.hit:
                    if time.time() - k.hit_time < 1.0:
                        stdscr.addstr(draw_y + 3, display_x - 1, f"[HIT!]", curses.A_BOLD)
                elif k.hit_wrong:
                    if time.time() - k.hit_time < 1.0:
                        stdscr.addstr(draw_y + 3, display_x - 1, f"[MISS]", curses.A_DIM)
                elif k.missed:
                    if display_x < width - 2:
                        stdscr.addstr(draw_y + 3, display_x - 1, f"[MISS]", curses.A_DIM)
                else:
                    for row_idx, row in enumerate(k.art):
                        if draw_y + row_idx >= height - 3:
                            continue
                        out_row = ''
                        for c in row:
                            if c == ' ':
                                out_row += '█'
                            else:
                                out_row += ' '
                        if display_x + len(out_row) <= width - 1:
                            stdscr.addstr(draw_y + row_idx, display_x, out_row, curses.A_STANDOUT)

        stdscr.refresh()

        c = stdscr.getch()
        if c != -1:
            try:
                pressed = chr(c).lower()
            except:
                pressed = None

            if pressed in ALL_KEYS:
                player = get_player(pressed)
                hit = False
                wrong_key = None
                for k in keys:
                    if not k.hit and not k.missed and not k.hit_wrong:
                        key_center = int(k.x) + k.art_width // 2
                        if pressed == k.key:
                            k.hit = True
                            k.hit_time = time.time()
                            if player == 1:
                                score1 += 1
                            else:
                                score2 += 1
                            speed = min(4.0, speed * 1.1)
                            hit = True
                            keys.append(spawn_key(speed))
                            break
                if not hit:
                    for k in keys:
                        if not k.hit and not k.hit_wrong and not k.missed:
                            k.hit_wrong = True
                            k.hit_time = time.time()
                            keys.append(spawn_key(speed))
                            break
                    if player == 1:
                        lives1 -= 1
                    else:
                        lives2 -= 1

        now = time.time()
        if len(keys) == 0 and now - last_spawn > 2.0:
            keys.append(spawn_key(speed))
            last_spawn = now

        for k in keys:
            if k.hit or k.hit_wrong or k.missed:
                continue
            k.move()
            if k.x > width - 4 - k.art_width:
                k.missed = True
                player = get_player(k.key)
                if player == 1:
                    lives1 -= 1
                else:
                    lives2 -= 1
                keys.append(spawn_key(speed))

        for k in keys:
            if k.hit or k.hit_wrong or not k.missed:
                continue
            display_x = int(k.x)
            if 4 <= display_x <= width + 2:
                stdscr.addstr(draw_y + 3, display_x - 1, f"[MISS]", curses.A_DIM)

        if lives1 <= 0 or lives2 <= 0:
            game_over = True

        if game_over:
            break

        curses.napms(30)

    return score1, score2, lives1, lives2

if __name__ == '__main__':
    s1, s2, l1, l2 = curses.wrapper(main)
    sys.__stdout__.write(f"\n=== GAME OVER ===\n")
    if l1 <= 0:
        sys.__stdout__.write(f"Player 2 Wins! (Player 1 ran out of lives)\n")
    elif l2 <= 0:
        sys.__stdout__.write(f"Player 1 Wins! (Player 2 ran out of lives)\n")
    sys.__stdout__.write(f"Player 1 (asdf): {s1}  Lives: {l1}\n")
    sys.__stdout__.write(f"Player 2 (jkl;): {s2}  Lives: {l2}\n")
    sys.__stdout__.flush()