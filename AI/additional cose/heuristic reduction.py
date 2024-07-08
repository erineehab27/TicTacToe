

import tkinter as tk
import random
from tkinter import messagebox
import time

def time_profile_example():
    start_time = time.time()

    # Simulate some time-consuming operations
    for _ in range(1000000):
        _ = 2 * 2

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
                all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
            all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def get_empty_positions(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, depth, maximizing_player, alpha, beta, player, counter):
    counter[0] += 1  # Increment the search space counter

    if check_winner(board, 'X'):
        return -1
    elif check_winner(board, 'O'):
        return 1
    elif check_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_empty_positions(board):
            i, j = move
            board[i][j] = player
            eval = minimax(board, depth - 1, False, alpha, beta, 'X' if player == 'O' else 'O', counter)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_empty_positions(board):
            i, j = move
            board[i][j] = player
            eval = minimax(board, depth - 1, True, alpha, beta, 'X' if player == 'O' else 'O', counter)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, player, counter):
    best_val = float('-inf')
    best_move = None

    for move in get_empty_positions(board):
        i, j = move
        board[i][j] = player
        move_val = minimax(board, 2, False, float('-inf'), float('inf'), 'X' if player == 'O' else 'O', counter)
        board[i][j] = ' '

        if move_val > best_val:
            best_move = move
            best_val = move_val

    return best_move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.current_player = 'X'

        self.buttons = {}  # Store buttons in a dictionary

        self.search_space_counter = [0]  # Counter for the search space
        self.root.bind('r', lambda event: self.restart_game())
        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)] = tk.Button(root, text='', font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[(i, j)].grid(row=i, column=j)

    def show_winner_message(self, player):
        messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        print(f"Player {self.current_player} wins!")

        # Print the search space counter
        print(f"Search Space Explored: {self.search_space_counter[0]}")

        self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)].config(state='disabled')

    def restart_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[(i, j)].config(text='', state='normal')

        self.current_player = 'X'  # Reset to 'X' for a new game
        self.search_space_counter = [0]  # Reset the search space counter

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[(row, col)].config(text=self.current_player, state='disabled', disabledforeground='black')

            if check_winner(self.board, self.current_player):
                self.show_winner_message(self.current_player)
                self.end_game()
            elif check_draw(self.board):
                print("It's a draw!")
                self.end_game()
            else:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                if self.current_player == 'O':
                    self.computer_move()

    def computer_move(self):
        if all(self.board[i][j] == ' ' for i in range(3) for j in range(3)):
            # If it's the first move of the game, choose a random corner position
            row, col = random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
        else:
            row, col = find_best_move(self.board, self.current_player, self.search_space_counter)
        self.make_move(row, col)

    def end_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)].config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

