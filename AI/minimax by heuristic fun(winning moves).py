import tkinter as tk
from tkinter import messagebox

class SearchSpaceStats:
    def __init__(self):
        self.nodes_explored_with_pruning = 0
        self.nodes_explored_without_pruning = 0

def get_possible_moves(board):
    # Returns a list of indices corresponding to empty spaces on the board
    return [i for i, val in enumerate(board) if val == ' ']

def check_winner(board, player):
    # Checks if the given player has won on the current board
    # Returns True if the player wins, False otherwise

    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == player:
            return True

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == player:
            return True

    # Check diagonals
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True

    # No winner found
    return False

def has_winning_move(board, player):
    for move in get_possible_moves(board):
        # Try the move for the current player
        board[move] = player

        # Check if the current player wins with this move
        if check_winner(board, player):
            # Undo the move and return True
            board[move] = ' '  # Undo the move
            return True

        # Undo the move for the next iteration
        board[move] = ' '

    # No winning move found
    return False

def evaluate_winning_moves(board, player, stats):
    # Check if the current player has a winning move
    if has_winning_move(board, player):
        winning_moves_score = 1  # Assign a high positive score for winning moves
    else:
        winning_moves_score = 0  # No winning move found, return a neutral score

    print(f"Winning Move Score for {player}: {winning_moves_score}")
    return winning_moves_score

def evaluate_board(board, stats):
    # Evaluation function for the minimax algorithm
    # Add more heuristics as needed
    winning_moves_score = evaluate_winning_moves(board, 'O', stats)  # AI is 'O'
    return winning_moves_score

class TicTacToeGUI:
    def __init__(self, stats):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.stats = stats  # Search space statistics

        # Create a 3x3 grid of buttons
        self.buttons = [[tk.Button(self.root, text=' ', font=('Helvetica', 24), width=5, height=2,
                                   command=lambda row=row, col=col: self.make_move(row, col))
                         for col in range(3)] for row in range(3)]

        # Place the buttons in the grid
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].grid(row=row, column=col)

        # Initialize the game state
        self.board = [' '] * 9
        self.current_player = 'X'

    def make_move(self, row, col):
        # Check if the selected move is valid
        if self.board[row * 3 + col] == ' ':
            # Update the board and display the move for the human player
            self.board[row * 3 + col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            # Check if the human player wins
            if check_winner(self.board, self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            else:
                # Switch to the AI's turn
                self.current_player = 'O'

                # AI makes a move using minimax with alpha-beta pruning
                ai_move = self.get_ai_move()
                if ai_move is not None:
                    self.board[ai_move] = 'O'
                    row, col = divmod(ai_move, 3)
                    self.buttons[row][col].config(text='O')

                    # Check if the AI wins
                    if check_winner(self.board, 'O'):
                        messagebox.showinfo("Game Over", "AI wins!")
                        self.reset_game()
                    else:
                        # Switch back to the human player's turn
                        self.current_player = 'X'

    def get_ai_move(self):
        # AI's move using the minimax algorithm with alpha-beta pruning
        best_score = float('-inf')
        best_move = None

        alpha = float('-inf')
        beta = float('inf')

        for move in get_possible_moves(self.board):
            self.board[move] = 'O'  # Assume AI makes the move
            self.stats.nodes_explored_with_pruning += 1
            score = self.minimax(self.board, 0, False, alpha, beta)
            self.board[move] = ' '  # Undo the move

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cut-off

        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        # Minimax algorithm with alpha-beta pruning
        if check_winner(board, 'X'):  # Human wins
            return -1
        elif check_winner(board, 'O'):  # AI wins
            return 1
        elif ' ' not in board:  # Tie
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for move in get_possible_moves(board):
                board[move] = 'O'
                self.stats.nodes_explored_with_pruning += 1
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                board[move] = ' '  # Undo the move

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in get_possible_moves(board):
                board[move] = 'X'
                self.stats.nodes_explored_with_pruning += 1
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                board[move] = ' '  # Undo the move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return min_eval

    def reset_game(self):
        # Reset the board and buttons for a new game
        for row in range(3):
            for col in range(3):
                self.board[row * 3 + col] = ' '
                self.buttons[row][col].config(text=' ')
        self.current_player = 'X'

    def run(self):
        self.root.mainloop()

# Create an instance of the TicTacToeGUI class and run the game
search_stats = SearchSpaceStats()
tic_tac_toe_game = TicTacToeGUI(search_stats)
tic_tac_toe_game.run()

# After the game is finished, print the search space statistics
print("Nodes Explored with Pruning:", search_stats.nodes_explored_with_pruning)

