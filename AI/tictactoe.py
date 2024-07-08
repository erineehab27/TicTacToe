import copy
import os
import sys
import time
from tkinter import messagebox

import pygame
import random
import numpy as np
import psutil
from constants import *

# --- PYGAME SETUP ---

pygame.init()
# gam_sound = pygame.mixer.Sound(r"D:\AI Project\tectactoe\mixkit-game-level-music-689.wav")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI MinMax Basic')
screen.fill(BG_COLOR)


             # ----------------Game Instructions-------------------
                   #    ---------press 'g' to change gamemode (pvp or ai)---------
                  # --------- press '0' to change ai level to 0 (random)-----
                    #    ---------press '1' to change ai level to 1 (MINMAX Algorithm)-----
                    #      -----------press 'r' to restart the game ------

# --- CLASSES ---

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROW, COL) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # return 0 if no win , return 1 if player 1 is win ,return 2 if palyer 2 is win


        # vertical wins
        for col in range(COL):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIR_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROW):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIR_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIR_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIR_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
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
                    empty_sqrs.append( (row, col) )

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        self.nodes_expanded = 0
        self.total_nodes_expanded = 0
        # --- RANDOM ---

    # this fun responsible of know empty square and choose random index to play in it
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # return empty square in the postion of index (some row and some colums)

    # --- MINIMAX ---
    def reset_expanded_nodes(self):
        total_expanded =+ self.nodes_expanded
        # self.total_nodes_expanded = total_expanded  # Update total nodes expanded
        self.nodes_expanded = 0
        return total_expanded
    def minimax(self, board, maximizing):

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                self.nodes_expanded += 1
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            self.nodes_expanded += 1

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    # --- MAIN FUNCTION OF AI CLASS  ---
    # this function used to determine if we play with random choice or with minmax algorithm
    def eval(self, main_board):
        # use  rnd function to move in random place which is empty
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minmax algorithm choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  #player 1= crosses   # player 2= circles
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()
        self.total_nodes_expanded = 0  # New attribute to track the total nodes expanded
        self.nodes_expanded_printed = False

    # --- DRAW METHODS ---
    def reset(self):

            total_expanded = self.ai.reset_expanded_nodes()  # Reset and get total expanded nodes
            print(f"Sum of Expanded Nodes: {total_expanded}")  # Print the total expanded nodes
            self.__init__()

    def show_lines(self):
        # bg
        screen.fill( BG_COLOR )

        # verticale
        #  line(surface, color, start_pos, end_pos, width=1) -> Rect
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIR_COLOR, center, RADUIS, CIR_WIDTH)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        total_expanded = self.ai.reset_expanded_nodes()  # Reset and get total expanded nodes
        print(f"Sum of Expanded Nodes: {total_expanded}")  # Print the total expanded nodes
        self.__init__()

def main():

    # --- OBJECTS ---
    # tracemalloc.start()
    total_nodes_expanded = 0
    total_time_elapsed = 0
    total_memory_used = 0
    num_rounds = 2

    for _ in range(num_rounds):
        # --- OBJECTS ---
        game = Game()
        board = game.board
        ai = game.ai

        # --- GAME LOOP ---
        start_time = time.time()
        while not game.isover():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        game.change_gamemode()

                    if event.key == pygame.K_r:
                        game.reset()
                        board = game.board
                        ai = game.ai

                    if event.key == pygame.K_0:
                        ai.level = 0

                    if event.key == pygame.K_1:
                        ai.level = 1

                    if event.key == pygame.K_2:
                        ai.level = 2

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    if board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)

                        if game.isover():
                            game.running = False

            if game.gamemode == 'ai' and game.player == ai.player and game.running:
                row, col = game.ai.eval(game.board)
                game.make_move(row, col)

                if game.isover():
                    game.running = False

                print(f"Nodes Expanded: {ai.nodes_expanded}")

            pygame.display.update()
        start_time = time.time()

        # Simulate some time-consuming operations
        for _ in range(1000000):
            _ = 2 * 2

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Elapsed Time: {elapsed_time} seconds")
        memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # in MB
        print(f"memory_used:{memory_used}")

        # Accumulate values for averaging
        total_nodes_expanded += ai.nodes_expanded
        total_time_elapsed += elapsed_time
        total_memory_used += memory_used

        # Display result for this round
        print("Game Over!")
        winner = game.board.final_state(show=True)
        if winner == 1:
            print("Player 1 wins!")
        elif winner == 2:
            print("Player 2 (or AI) wins!")
        else:
            print("It's a draw!")

        # Reset nodes_expanded for the next round
        ai.nodes_expanded = 0

        # Calculate averages
    avg_nodes_expanded = total_nodes_expanded / num_rounds
    avg_time_elapsed = total_time_elapsed / num_rounds
    avg_memory_used = total_memory_used / num_rounds

    print(f"\nAverage Nodes Expanded: {avg_nodes_expanded}")
    print(f"Average Time Elapsed: {avg_time_elapsed} seconds")
    print(f"Average Memory Used: {avg_memory_used} MB")

    pygame.quit()
    sys.exit()


main()

#     def time_profile_example():
#         start_time = time.time()
#
#         # Simulate some time-consuming operations
#         for _ in range(1000000):
#             _ = 2 * 2
#
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#         print(f"Elapsed Time: {elapsed_time}seconds")
#     game = Game()
#     board = game.board
#     ai = game.ai
#
#     # --- MAINLOOP ---
#     while True:
#
#
#         # pygame events
#         for event in pygame.event.get():
#             # gam_sound.play(-1)
#              # quit event
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             # keydown event
#             if event.type == pygame.KEYDOWN:
#                 # g-gamemode
#                 if event.key == pygame.K_g:
#                     game.change_gamemode()
#                 # r-restart
#                 if event.key == pygame.K_r:
#                     game.reset()
#                     board = game.board
#                     ai = game.ai
#                 # 0-random ai
#                 if event.key == pygame.K_0:
#                     ai.level = 0
#                 # 1-random ai
#                 if event.key == pygame.K_1:
#                     ai.level = 1
#             # click event
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = event.pos
#                 row = pos[1] // SQSIZE
#                 col = pos[0] // SQSIZE
#                 # human mark sqr
#                 if board.empty_sqr(row, col) and game.running:
#                     game.make_move(row, col)
#
#                     if game.isover():
#                         game.running = False
#                         if not game.nodes_expanded_printed:
#                             print(f"Nodes Expanded: {ai.nodes_expanded}")
#                             game.nodes_expanded_printed = True
#
#
#         # AI initial call
#         if game.gamemode == 'ai' and game.player == ai.player and game.running:
#             row, col = ai.eval(board)
#             game.make_move(row, col)
#
#             if game.isover():
#                 game.running = False
#                 process = psutil.Process()
#                 memory_info = process.memory_info()
#                 rss = memory_info.rss  # resident set size (memory used by the process)
#                 print(f"Memory used by process: {rss / 1024 ** 2:.2f} MB")
#                 print(f"Nodes Expanded: {ai.nodes_expanded}")
#                 game.nodes_expanded_printed = True
#                 ai.reset_expanded_nodes()
#                 print(f"sum of expanded :{ai.reset_expanded_nodes()}")
#                 Time = time_profile_example()
#
#             # print(f"Nodes Expanded: {ai.nodes_expanded}")
#
#         pygame.display.update()
#
#
# pygame.time.Clock().tick(60)
#
#
#
#
# main()
