import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Impossible Tic Tac Toe")
        self.window.resizable(False, False)
        
        self.board = [' '] * 9
        self.buttons = []
        self.game_over = False
        
        self.create_board()
        
    def create_board(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10)
        
        for i in range(9):
            btn = tk.Button(frame, text=' ', font=('Arial', 40), width=5, height=2,
                          command=lambda idx=i: self.player_move(idx))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
        
        reset_btn = tk.Button(self.window, text='New Game', font=('Arial', 14),
                             command=self.reset_game)
        reset_btn.pack(pady=5)
        
    def player_move(self, pos):
        if self.game_over or self.board[pos] != ' ':
            return
        
        self.board[pos] = 'X'
        self.buttons[pos].config(text='X', fg='blue')
        
        if self.check_winner('X'):
            self.end_game("You won! (This shouldn't happen...)")
            return
        
        if self.is_board_full():
            self.end_game("It's a draw!")
            return
        
        self.ai_move()
        
    def ai_move(self):
        move = self.best_move()
        self.board[move] = 'O'
        self.buttons[move].config(text='O', fg='red')
        
        if self.check_winner('O'):
            self.end_game("I win! Better luck next time.")
            return
        
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
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for line in lines:
            values = [self.board[i] for i in line]
            if values.count(player) == 2 and values.count(' ') == 1:
                return line[values.index(' ')]
        
        return None
    
    def find_fork_move(self, player):
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = player
                winning_moves = 0
                
                for j in range(9):
                    if self.board[j] == ' ':
                        self.board[j] = player
                        if self.check_winner(player):
                            winning_moves += 1
                        self.board[j] = ' '
                
                self.board[i] = ' '
                
                if winning_moves >= 2:
                    return i
        
        return None
    
    def block_fork(self, opponent):
        fork_pos = self.find_fork_move(opponent)
        if fork_pos is not None:
            return fork_pos
        return None

    def check_winner(self, player):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for line in lines:
            if all(self.board[i] == player for i in line):
                return True
        
        return False
    
    def is_board_full(self):
        return ' ' not in self.board
    
    def end_game(self, message):
        self.game_over = True
        messagebox.showinfo("Game Over", message)
    
    def reset_game(self):
        self.board = [' '] * 9
        self.game_over = False
        for btn in self.buttons:
            btn.config(text=' ', fg='black')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
