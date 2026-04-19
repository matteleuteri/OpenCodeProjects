import curses
import random
import time
import sys

PLAYER1_KEYS = ['a', 's', 'd', 'f']
PLAYER2_KEYS = ['j', 'k', 'l', ';']
ALL_KEYS = PLAYER1_KEYS + PLAYER2_KEYS

class KeyObj:
    def __init__(self, key, start_x, speed):
        self.key = key
        self.x = start_x
        self.speed = speed
        self.hit = False
        self.hit_wrong = False
        self.missed = False
        self.hit_time = 0

    def move(self):
        self.x += self.speed

def spawn_key(speed, width):
    key = random.choice(ALL_KEYS)
    return KeyObj(key, 3, speed)

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

    height, width = stdscr.getmaxyx()

    score1 = 0
    score2 = 0
    speed = 0.5
    last_spawn = time.time()
    keys = []
    game_over = False
    

    while True:
        stdscr.erase()
        stdscr.addstr(0, 2, "KEY RUSH - Player 1: asdf | Player 2: jkl;")
        stdscr.addstr(1, 2, "=" * (width - 4))
        
        stdscr.addstr(2, 2, f"Player 1 (asdf): {score1}")
        stdscr.addstr(3, 2, f"Player 2 (jkl;): {score2}")
        
        stdscr.addstr(height - 3, 2, "=" * (width - 4))
        draw_y = height // 2
        
        
        
        for k in keys:
            display_x = int(k.x)
            if 4 <= display_x <= width - 4:
                if k.hit:
                    if time.time() - k.hit_time < 1.0:
                        stdscr.addstr(draw_y, display_x - 1, f"[HIT!]", curses.A_BOLD)
                elif k.hit_wrong:
                    if time.time() - k.hit_time < 1.0:
                        stdscr.addstr(draw_y, display_x - 1, f"[MISS]", curses.A_DIM)
                elif k.missed:
                    if display_x < width - 2:
                        stdscr.addstr(draw_y, display_x - 1, f"[MISS]", curses.A_DIM)
                else:
                    stdscr.addstr(draw_y, display_x - 1, f"[{k.key}]", curses.A_STANDOUT | curses.A_BOLD)

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
                    if not k.hit and not k.missed:
                        if pressed == k.key:
                            k.hit = True
                            k.hit_time = time.time()
                            if player == 1:
                                score1 += 1
                            else:
                                score2 += 1
                            speed = min(4.0, speed * 1.1)
                            hit = True
                            keys.append(spawn_key(speed, width))
                            break
                if not hit:
                    for k in keys:
                        if not k.hit and not k.hit_wrong and not k.missed:
                            k.hit_wrong = True
                            k.hit_time = time.time()
                            keys.append(spawn_key(speed, width))
                            break
                    if player == 1:
                        score1 -= 1
                    else:
                        score2 -= 1

        now = time.time()
        if len(keys) == 0 and now - last_spawn > 2.0:
            keys.append(spawn_key(speed, width))
            last_spawn = now

        for k in keys:
            if k.hit or k.hit_wrong or k.missed:
                continue
            k.move()
            if k.x > width - 4:
                k.missed = True
                game_over = True

        for k in keys:
            if k.hit or k.hit_wrong or not k.missed:
                continue
            display_x = int(k.x)
            if 4 <= display_x <= width + 2:
                stdscr.addstr(draw_y, display_x - 1, f"[MISS]", curses.A_DIM)

        if game_over:
            break

        curses.napms(30)

    return score1, score2

if __name__ == '__main__':
    s1, s2 = curses.wrapper(main)
    sys.__stdout__.write(f"\n=== GAME OVER ===\n")
    sys.__stdout__.write(f"Player 1 (asdf): {s1}\n")
    sys.__stdout__.write(f"Player 2 (jkl;): {s2}\n")
    sys.__stdout__.flush()