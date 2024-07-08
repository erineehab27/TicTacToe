import tkinter as tk
import random
from tkinter import messagebox
import time

import psutil
#
# def time_profile_example():
#     start_time = time.time()
#
#     # Simulate some time-consuming operations
#     for _ in range(1000000):
#         _ = 2 * 2
#
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#
#     print(f"Elapsed Time: {elapsed_time}seconds")


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

def bfs_heuristic(board, player):
    # You can define your heuristic function for BFS here
    # For example, prioritize center and corners
    heuristic_value = 0
    if board[1][1] == player:
        heuristic_value += 2
    for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[i][j] == player:
            heuristic_value += 1
    return heuristic_value

def bfs_move(board, player,counter):
    empty_positions = get_empty_positions(board)
    random.shuffle(empty_positions)  # Shuffle for randomness

    # Check if the computer can win in the next move
    for position in empty_positions:
        i, j = position
        board[i][j] = player
        counter[0] += 1
        if check_winner(board, player):
            board[i][j] = ' '  # Undo the move
            return position
        board[i][j] = ' '  # Undo the move

    # Check if the opponent can win in the next move and block them
    opponent = 'X' if player == 'O' else 'O'
    for position in empty_positions:
        i, j = position
        board[i][j] = opponent
        counter[0] += 1
        if check_winner(board, opponent):
            board[i][j] = ' '  # Undo the move
            return position
        board[i][j] = ' '  # Undo the move

    # If no immediate threat or opportunity, use the original BFS heuristic
    best_move = None
    best_heuristic = float('-inf')

    for position in empty_positions:
        i, j = position
        board[i][j] = player
        counter[0] += 1
        heuristic_value = bfs_heuristic(board, player)
        board[i][j] = ' '  # Undo the move

        if heuristic_value > best_heuristic:
            best_heuristic = heuristic_value
            best_move = position

    return best_move

# In the TicTacToeGUI class

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.current_player = 'X'

        self.buttons = {}  # Store buttons in a dictionary
        self.search_space_counter = [0]
        self.root.bind('r', lambda event: self.restart_game())
        self.search_space_Sum=[0]
        self.game_count=[0]
        self.total_elapsed_time = [0]
        self.total_memory=[0]

        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)] = tk.Button(root, text='', font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[(i, j)].grid(row=i, column=j)



    def show_winner_message(self, player):
        messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        print(f"Player {self.current_player} wins!")
        self.reset_game()
        print(f"Search Space Explored: {self.search_space_counter[0]}")
        self.search_space_Sum[0] += self.search_space_counter[0]
        self.game_count[0] += 1
        average_search_space = self.search_space_Sum[0] / self.game_count[0]

        print(f"Average Search Space Explored: {average_search_space:.2f}")
        # print(f"Average memory {average_memory:.2f}")

        process = psutil.Process()
        memory_info = process.memory_info()
        rss = memory_info.rss  # resident set size (memory used by the process)
        memory = rss / 1024 ** 2
        print(f"Memory used by process: {memory:.2f} MB")
        self.total_memory[0] += memory
        average_memory = self.total_memory[0] / self.game_count[0]
        print(f"Average memory {average_memory:.2f} MB")
        self.search_space_counter[0] = 0
        start_time = time.time()

        # Simulate some time-consuming operations
        for _ in range(1000000):
            _ = 2 * 2

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.total_elapsed_time[0] += elapsed_time
        average_time = self.total_elapsed_time[0] / self.game_count[0]
        print(f"Elapsed Time: {elapsed_time} seconds")
        print(f" Average Elapsed Time: {average_time} seconds")

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



    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[(row, col)].config(text=self.current_player, state='disabled', disabledforeground='black')

            if check_winner(self.board, self.current_player):
                self.show_winner_message(self.current_player)
            elif check_draw(self.board):
                print("It's a draw!")
                print(f"Search Space Explored: {self.search_space_counter[0]}")
                self.search_space_Sum[0] += self.search_space_counter[0]

                self.game_count[0] += 1
                average_search_space = self.search_space_Sum[0] /self.game_count[0]
                print(f"Average Search Space Explored: {average_search_space:.2f}")

                process = psutil.Process()
                memory_info = process.memory_info()
                rss = memory_info.rss  # resident set size (memory used by the process)
                memory = rss / 1024 ** 2
                print(f"Memory used by process: {memory:.2f} MB")
                self.total_memory[0] += memory
                average_memory = self.total_memory[0] / self.game_count[0]
                print(f"Average memory {average_memory:.2f} MB")

                start_time = time.time()

                # Simulate some time-consuming operations
                for _ in range(1000000):
                    _ = 2 * 2

                end_time = time.time()
                elapsed_time = end_time - start_time
                self.total_elapsed_time[0]+=elapsed_time
                average_time= self.total_elapsed_time[0]/self.game_count[0]
                print(f"Elapsed Time: {elapsed_time} seconds")
                print(f" Average Elapsed Time: {average_time} seconds")
                self.search_space_counter[0] = 0
                self.reset_game()
            else:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                if self.current_player == 'O':
                    self.computer_move()

    def computer_move(self):
        if all(self.board[i][j] == ' ' for i in range(3) for j in range(3)):
            # If it's the first move of the game, choose a random corner position
            row, col = random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
        else:
            row, col = bfs_move(self.board, self.current_player,self.search_space_counter)
        self.make_move(row, col)

    def end_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[(i, j)].config(state='disabled')
                self.search_space_Sum += self.search_space_counter

    # Time = time_profile_example()

# Get memory usage of the Python process

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()