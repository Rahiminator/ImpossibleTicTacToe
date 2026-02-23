import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        # Create main game window
        self.window = tk.Tk()
        self.window.title("Impossible Tic Tac Toe")
        self.window.resizable(False, False) # Prevent window resizing
        
        # Internal board representation (9 cells)
        self.board = [' '] * 9

        # Store button widgets for UI updates
        self.buttons = []

        # Track whether the game has ended
        self.game_over = False
        
        # Build the UI board
        self.create_board()
        
    def create_board(self):
        # Frame to hold the 3x3 grid
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10)
        
        # Create 9 buttons for the board
        for i in range(9):
            btn = tk.Button(
                frame, 
                text=' ', 
                font=('Arial', 40), 
                width=5, 
                height=2,
                command=lambda idx=i: self.player_move(idx)) # Handle player click
            
            # Position button in 3x3 grid
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)

            # Store reference for later updates
            self.buttons.append(btn)
        
        # New Game button
        reset_btn = tk.Button(
            self.window, 
            text='New Game', 
            font=('Arial', 14),
            command=self.reset_game
        )
        reset_btn.pack(pady=5)
        
    def player_move(self, pos):
        # Ignore move if game is over or cell is occupied
        if self.game_over or self.board[pos] != ' ':
            return
        
        # Apply player move
        self.board[pos] = 'X'
        self.buttons[pos].config(text='X', fg='blue')
        
        # Check win
        if self.check_winner('X'):
            self.end_game("You won! (This shouldn't happen...)")
            return
        
        # Check draw
        if self.is_board_full():
            self.end_game("It's a draw!")
            return
        
        # AI turn
        self.ai_move()
        
    def ai_move(self):
        # Get best move from AI logic
        move = self.best_move()

        # Apply AI move
        self.board[move] = 'O'
        self.buttons[move].config(text='O', fg='red')
        
        # Check win
        if self.check_winner('O'):
            self.end_game("I win! Better luck next time.")
            return
        
        # Check draw
        if self.is_board_full():
            self.end_game("It's a draw!")
            return

    def best_move(self):
        # 1. Win if possible
        move = self.find_winning_move('O')
        if move is not None:
            return move
        
        # 2. Block opponent win
        move = self.find_winning_move('X')
        if move is not None:
            return move
        
        # 3. Create fork
        move = self.find_fork_move('O')
        if move is not None:
            return move
        
        # 4. Block opponent fork
        move = self.block_fork('X')
        if move is not None:
            return move
        
        # 5. Take center
        if self.board[4] == ' ':
            return 4
        
        # 6. Take opposite corner
        corners = [(0, 8), (2, 6), (6, 2), (8, 0)]
        for corner, opposite in corners:
            if self.board[corner] == 'X' and self.board[opposite] == ' ':
                return opposite
        
        # 7. Take any corner
        for corner in [0, 2, 6, 8]:
            if self.board[corner] == ' ':
                return corner
        
        # 8. Take any side
        for side in [1, 3, 5, 7]:
            if self.board[side] == ' ':
                return side
        
        return 0
    
    def find_winning_move(self, player):
        # All possible winning line combinations
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        
        for line in lines:
            values = [self.board[i] for i in line]
            if values.count(player) == 2 and values.count(' ') == 1:
                return line[values.index(' ')]
        
        return None
    
    # Check each line for 2 marks + 1 empty
    def find_fork_move(self, player):
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = player
                winning_moves = 0
                
                # Count resulting winning paths
                for j in range(9):
                    if self.board[j] == ' ':
                        self.board[j] = player
                        if self.check_winner(player):
                            winning_moves += 1
                        self.board[j] = ' '
                
                # Reset simulation
                self.board[i] = ' '
                
                if winning_moves >= 2:
                    return i
        
        return None
    
    def block_fork(self, opponent):
        # Reuse fork detection to block opponent
        fork_pos = self.find_fork_move(opponent)
        if fork_pos is not None:
            return fork_pos
        return None

    def check_winner(self, player):
        # Same win line combinations
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        # Check if any line is fully occupied by player
        for line in lines:
            if all(self.board[i] == player for i in line):
                return True
        
        return False
    
    def is_board_full(self):
        # Draw condition
        return ' ' not in self.board
    
    def end_game(self, message):
        # Stop further moves
        self.game_over = True

        # Show popup message
        messagebox.showinfo("Game Over", message)
    
    def reset_game(self):
        # Reset board state
        self.board = [' '] * 9
        self.game_over = False

        # Clear UI buttons
        for btn in self.buttons:
            btn.config(text=' ', fg='black')
    
    def run(self):
        # Start Tkinter event loop
        self.window.mainloop()

# Entry point
if __name__ == "__main__":
    game = TicTacToe()
    game.run()