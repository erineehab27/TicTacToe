
import tkinter as tk
import subprocess
import sys

def open_program(program_path):
    try:
        subprocess.run([sys.executable, program_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the program: {e}")

# Create the main window
window = tk.Tk()
window.title("Button Window")

# Define paths for each program
program_paths = [
    r"D:\AI Project\AI\tictactoe.py",
    r"D:\AI Project\AI\Alpha_beta.py",
    r"D:\AI Project\AI\minimax by heuristic fun(winning moves).py",
    r"D:\AI Project\AI\distance_improve.py",
    r"D:\AI Project\AI\symmtry.py",
    r"D:\AI Project\AI\BF_Search.py",
]

# Create six buttons with corresponding program paths
buttons = []
for i, program_path in enumerate(program_paths, start=1):
    button_text = f"Button {i} ({program_path})"
    button = tk.Button(window, text=button_text, command=lambda path=program_path: open_program(path))
    button.pack(pady=10)
    buttons.append(button)

# Run the application
window.mainloop()

