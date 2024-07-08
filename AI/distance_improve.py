import copy
import sys
import time
import pygame
import numpy as np
import psutil

# Constants
WIDTH, HEIGHT = 600, 600
SQSIZE = WIDTH // 3
ROW, COL = 5, 5
OFFSET = 15
LINE_WIDTH = 15
CROSS_WIDTH = 25
CIR_WIDTH = 15
RADUIS = SQSIZE // 3

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CROSS_COLOR = (255, 0, 0)
CIR_COLOR = (0, 0, 255)

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)  # Diagonals
]

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

# Classes
class Board:
    def __init__(self):
        self.squares = np.zeros((ROW, COL))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
        self.player = 1

    def final_state(self, show=False):
        for line in WINNING_LINES:
            if all(self.squares.flatten()[i] == 1 for i in line):
                return 1
            elif all(self.squares.flatten()[i] == 2 for i in line):
                return 2

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROW):
            for col in range(COL):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        self.nodes_expanded = 0

    def minimax_heuristic(self, board, maximizing, depth=0, alpha=float('-inf'), beta=float('inf')):
        case = board.final_state()

        if case == 1:
            return 10 - depth, None
        elif case == 2:
            return depth - 10, None
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = float('-inf')
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                self.nodes_expanded += 1
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval, _ = self.minimax_heuristic(temp_board, False, depth + 1, alpha, beta)
                distance = self.distance_heuristic(row, col)
                eval += distance
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        elif not maximizing:
            min_eval = float('inf')
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                self.nodes_expanded += 1
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval, _ = self.minimax_heuristic(temp_board, True, depth + 1, alpha, beta)
                distance = self.distance_heuristic(row, col)
                eval -= distance
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def distance_heuristic(self, row, col):
        center_row, center_col = ROW // 2, COL // 2
        return abs(row - center_row) + abs(col - center_col)

    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax_heuristic(main_board, False, alpha=float('-inf'), beta=float('inf'))

        if move is not None:
            row, col = move
            distance = self.distance_heuristic(row, col)
            print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval} and distance: {distance}')

        return move

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = np.random.choice(len(empty_sqrs))
        return empty_sqrs[idx]

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
    +    if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIR_COLOR, center, RADUIS, CIR_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                if game.board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False

        if game.player == game.ai.player and game.running:
            row, col = game.ai.eval(game.board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
                process = psutil.Process()
                memory_info = process.memory_info()
                rss = memory_info.rss
                print(f"Memory used by process: {rss / 1024 ** 2:.2f} MB")

            print(f"Nodes Expanded: {game.ai.nodes_expanded}")

        pygame.display.update()

if __name__ == "__main__":
    main()
