import curses
import random
import time

# Tetromino shapes as lists of (x, y) offsets
SHAPES = {
    'I': [(0,1), (1,1), (2,1), (3,1)],
    'O': [(0,0), (1,0), (0,1), (1,1)],
    'T': [(1,0), (0,1), (1,1), (2,1)],
    'S': [(1,0), (2,0), (0,1), (1,1)],
    'Z': [(0,0), (1,0), (1,1), (2,1)],
    'J': [(0,0), (0,1), (1,1), (2,1)],
    'L': [(2,0), (0,1), (1,1), (2,1)]
}

WIDTH = 10
HEIGHT = 20

class Piece:
    def __init__(self, shape):
        self.shape = SHAPES[shape]
        self.x = WIDTH // 2 - 2
        self.y = 0

    def rotate(self):
        self.shape = [(-y, x) for x, y in self.shape]

    def cells(self):
        return [(self.x + x, self.y + y) for x, y in self.shape]

class Board:
    def __init__(self):
        self.grid = [[0]*WIDTH for _ in range(HEIGHT)]
        self.piece = Piece(random.choice(list(SHAPES.keys())))
        self.game_over = False
        self.score = 0

    def collision(self, cells):
        for x, y in cells:
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                return True
            if self.grid[y][x]:
                return True
        return False

    def freeze(self):
        for x, y in self.piece.cells():
            self.grid[y][x] = 1
        self.clear_lines()
        self.piece = Piece(random.choice(list(SHAPES.keys())))
        if self.collision(self.piece.cells()):
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if not all(row)]
        cleared = HEIGHT - len(new_grid)
        self.score += cleared
        for _ in range(cleared):
            new_grid.insert(0, [0]*WIDTH)
        self.grid = new_grid

    def move(self, dx, dy):
        self.piece.x += dx
        self.piece.y += dy
        if self.collision(self.piece.cells()):
            self.piece.x -= dx
            self.piece.y -= dy
            return False
        return True

    def rotate(self):
        old_shape = self.piece.shape[:]
        self.piece.rotate()
        if self.collision(self.piece.cells()):
            self.piece.shape = old_shape

    def step(self):
        if not self.move(0, 1):
            self.freeze()

    def draw(self, stdscr):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                ch = '#'
                if self.grid[y][x]:
                    stdscr.addch(y, x*2, ch)
                    stdscr.addch(y, x*2+1, ch)
                else:
                    stdscr.addch(y, x*2, ' ')
                    stdscr.addch(y, x*2+1, ' ')
        for x, y in self.piece.cells():
            if 0 <= y < HEIGHT:
                stdscr.addch(y, x*2, 'X')
                stdscr.addch(y, x*2+1, 'X')
        stdscr.addstr(0, WIDTH*2 + 2, f"Score: {self.score}")


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    board = Board()
    while not board.game_over:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            board.move(-1, 0)
        elif key == curses.KEY_RIGHT:
            board.move(1, 0)
        elif key == curses.KEY_DOWN:
            board.step()
        elif key == curses.KEY_UP:
            board.rotate()
        board.step()
        stdscr.clear()
        board.draw(stdscr)
        stdscr.refresh()
        time.sleep(0.05)
    stdscr.clear()
    stdscr.addstr(HEIGHT//2, WIDTH, "Game Over!")
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
