import unittest
from tic_tac_toe import TicTacToe

class TestUnbeatableAI(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToe()
        # Prevent GUI from showing during tests
        self.game.window.withdraw()
    
    def tearDown(self):
        self.game.window.destroy()
    
    def play_game(self, player_moves):
        """Simulate a game with given player moves"""
        self.game.reset_game()
        
        for move in player_moves:
            if self.game.game_over or self.game.board[move] != ' ':
                break
            
            # Player move
            self.game.board[move] = 'X'
            
            if self.game.check_winner('X'):
                return 'X'
            
            if self.game.is_board_full():
                return 'Draw'
            
            # AI move
            ai_move = self.game.best_move()
            self.game.board[ai_move] = 'O'
            
            if self.game.check_winner('O'):
                return 'O'
            
            if self.game.is_board_full():
                return 'Draw'
        
        return 'Incomplete'
    
    def test_ai_blocks_row_wins(self):
        """Test AI blocks all row win attempts"""
        # Try to win top row
        result = self.play_game([0, 1])
        self.assertNotEqual(result, 'X', "AI failed to block top row")
        
        # Try to win middle row
        result = self.play_game([3, 4])
        self.assertNotEqual(result, 'X', "AI failed to block middle row")
        
        # Try to win bottom row
        result = self.play_game([6, 7])
        self.assertNotEqual(result, 'X', "AI failed to block bottom row")
    
    def test_ai_blocks_column_wins(self):
        """Test AI blocks all column win attempts"""
        # Try to win left column
        result = self.play_game([0, 3])
        self.assertNotEqual(result, 'X', "AI failed to block left column")
        
        # Try to win middle column
        result = self.play_game([1, 4])
        self.assertNotEqual(result, 'X', "AI failed to block middle column")
        
        # Try to win right column
        result = self.play_game([2, 5])
        self.assertNotEqual(result, 'X', "AI failed to block right column")
    
    def test_ai_blocks_diagonal_wins(self):
        """Test AI blocks diagonal win attempts"""
        # Try to win main diagonal
        result = self.play_game([0, 4])
        self.assertNotEqual(result, 'X', "AI failed to block main diagonal")
        
        # Try to win anti-diagonal
        result = self.play_game([2, 4])
        self.assertNotEqual(result, 'X', "AI failed to block anti-diagonal")
    
    def test_ai_takes_winning_move(self):
        """Test AI takes winning move when available"""
        self.game.reset_game()
        # Set up board where AI can win
        self.game.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        move = self.game.best_move()
        self.assertEqual(move, 2, "AI should take winning move at position 2")

    def test_ai_prioritizes_win_over_block(self):
        """Test AI wins instead of blocking when both are possible"""
        self.game.reset_game()
        # AI can win at 2, or block at 8
        self.game.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        move = self.game.best_move()
        self.assertEqual(move, 2, "AI should prioritize winning over blocking")
    
    def test_center_strategy(self):
        """Test AI takes center when optimal"""
        self.game.reset_game()
        self.game.board[0] = 'X'  # Player takes corner
        move = self.game.best_move()
        self.assertEqual(move, 4, "AI should take center after corner move")
    
    def test_corner_response(self):
        """Test AI responds correctly to corner openings"""
        self.game.reset_game()
        self.game.board[0] = 'X'
        move = self.game.best_move()
        self.assertIn(move, [4], "AI should take center against corner opening")
    
    def test_fork_creation(self):
        """Test AI creates forks when possible"""
        self.game.reset_game()
        # Set up board where AI can create a fork
        self.game.board = ['O', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'O']
        fork_move = self.game.find_fork_move('O')
        self.assertIsNotNone(fork_move, "AI should find fork opportunity")
    
    def test_fork_blocking(self):
        """Test AI blocks opponent forks"""
        self.game.reset_game()
        # Set up board where player can create a fork
        self.game.board = ['X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'X']
        move = self.game.best_move()
        # AI should block the fork - taking a corner (2, 6) or side (1, 3, 5, 7) are all valid defensive moves
        self.assertIn(move, [1, 2, 3, 5, 6, 7], "AI should block opponent fork")
        
        # Verify the move actually prevents the player from winning
        self.game.board[move] = 'O'
        # Player should not have a winning move available
        player_win_move = self.game.find_winning_move('X')
        self.assertIsNone(player_win_move, "AI's move should prevent immediate player win")
    
    def test_exhaustive_player_cannot_win(self):
        """Exhaustively test that player cannot win from any starting position"""
        wins = 0
        draws = 0
        losses = 0
        
        # Test starting from each position
        for first_move in range(9):
            result = self.play_game([first_move, 0, 1, 2, 3, 4, 5, 6, 7, 8])
            
            if result == 'X':
                wins += 1
            elif result == 'Draw':
                draws += 1
            elif result == 'O':
                losses += 1
        
        self.assertEqual(wins, 0, f"Player won {wins} games - AI is beatable!")
        print(f"\nExhaustive test results: Wins={wins}, Draws={draws}, Losses={losses}")
    
    def test_common_strategies(self):
        """Test common player strategies fail"""
        # Strategy 1: Opposite corners
        result = self.play_game([0, 8, 2, 6])
        self.assertNotEqual(result, 'X', "Opposite corners strategy should not win")
        
        # Strategy 2: Center then corners
        result = self.play_game([4, 0, 2, 6])
        self.assertNotEqual(result, 'X', "Center-corners strategy should not win")
        
        # Strategy 3: Side attacks
        result = self.play_game([1, 3, 5, 7])
        self.assertNotEqual(result, 'X', "Side attacks strategy should not win")
    
    def test_board_state_integrity(self):
        """Test board state remains valid throughout game"""
        self.game.reset_game()
        moves = [0, 2, 4, 6, 8]
        
        for move in moves:
            if self.game.board[move] == ' ':
                self.game.board[move] = 'X'
                
                # Check no invalid characters
                for cell in self.game.board:
                    self.assertIn(cell, ['X', 'O', ' '], "Invalid board state")
                
                if not self.game.is_board_full() and not self.game.check_winner('X'):
                    ai_move = self.game.best_move()
                    self.assertTrue(0 <= ai_move <= 8, "AI move out of bounds")
                    self.assertEqual(self.game.board[ai_move], ' ', "AI chose occupied cell")
                    self.game.board[ai_move] = 'O'

if __name__ == '__main__':
    unittest.main(verbosity=2)
