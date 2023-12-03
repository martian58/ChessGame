class ChessGame:
    def __init__(self):
        # Initialize the chess game with an 8x8 chessboard, starting player, and game state.
        self.board = self.create_board()
        self.current_player = 'white'
        self.game_over = False

    def create_board(self):
        """Create an 8x8 chessboard with the initial piece positions."""
        return [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]

    def display_board(self):
        """Display the current state of the chessboard."""
        print("\n   a b c d e f g h")
        print(" +----------------")
        for i in range(8):
            print(f'{8 - i}|', end=' ')
            for j in range(8):
                print(self.board[i][j], end=' ')
            print()

    def make_move(self, move):
        """Make a move on the chessboard."""
        start, end = move.split()
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        if self.is_valid_move(start_col, start_row, end_col, end_row):
            # Perform the move
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ' '

            if self.is_checkmate(self.current_player):
                # Check for checkmate
                self.game_over = True
                print("-----------------------------------------")
                print(f"Checkmate! {self.current_player.capitalize()} wins! -")
                print("-----------------------------------------")

            elif self.is_check(self.current_player):
                # Check for check
                print("-----------------------------------------")
                print(f"Check! {self.current_player.capitalize()} is in check.")
                print("-----------------------------------------")

            # Switch players
            self.current_player = 'black' if self.current_player == 'white' else 'white'
        else:
            print("Invalid move. Please try again.")

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """Validate if the move adheres to the rules of chess."""
        piece = self.board[start_row][start_col]
        target_piece = self.board[end_row][end_col] if 0 <= end_row < 8 and 0 <= end_col < 8 else None

        # Check if the move is within the bounds of the board
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Check if the piece at the start position belongs to the current player
        if (self.current_player == 'white' and piece.isupper()) or \
           (self.current_player == 'black' and piece.islower()):
            return False
        # Check if the destination square is occupied by a piece of the same color
        if target_piece and ((self.current_player == 'white' and target_piece.islower()) or \
           (self.current_player == 'black' and target_piece.isupper())):
            return False

        # Implement specific rules for each piece
        if piece.lower() == 'p':
            return self.is_valid_pawn_move(start_col, start_row, end_col, end_row, target_piece)

        elif piece.lower() == ' ':
            return None

        elif piece.lower() == 'n':
            return self.is_valid_knight_move(start_col, start_row, end_col, end_row)

        elif piece.lower() == 'b':
            return self.is_valid_bishop_move(start_col, start_row, end_col, end_row, target_piece)

        elif piece.lower() == 'r':
            return self.is_valid_rook_move(start_col, start_row, end_col, end_row, target_piece)

        elif piece.lower() == 'q':
            return self.is_valid_queen_move(start_col, start_row, end_col, end_row, target_piece)

        elif piece.lower() == 'k':
            return self.is_valid_king_move(start_col, start_row, end_col, end_row, target_piece)

        return False

    def is_valid_pawn_move(self, start_col, start_row, end_col, end_row, target_piece):
        """Validate pawn movement."""
        direction = 1 if self.current_player == 'white' else -1

        if start_col == end_col:  # Moving straight
            if start_row - end_row == direction and target_piece == ' ':
                return True
            elif start_row == 6 or 2 and start_row - end_row == 2 * direction and target_piece == ' ' \
                    and self.board[start_row - direction][start_col] == ' ':
                return True
        elif abs(start_col - end_col) == 1 and start_row - end_row == direction and target_piece.islower() != (
                self.current_player == 'white'):
            return True
        return False

    def is_valid_knight_move(self, start_col, start_row, end_col, end_row):
        """Validate knight movement."""
        return (abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1) \
               or (abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2)

    def is_valid_bishop_move(self, start_col, start_row, end_col, end_row, target_piece):
        """Validate bishop movement."""
        return abs(end_row - start_row) == abs(end_col - start_col) and self.no_obstacles(start_row, start_col,
                                                                                            end_row, end_col)

    def is_valid_rook_move(self, start_col, start_row, end_col, end_row, target_piece):
        """Validate rook movement."""
        return (start_row == end_row or start_col == end_col) and self.no_obstacles(start_row, start_col, end_row,
                                                                                    end_col)

    def is_valid_queen_move(self, start_col, start_row, end_col, end_row, target_piece):
        """Validate queen movement."""
        return (start_row == end_row or start_col == end_col or abs(end_row - start_row) == abs(
            end_col - start_col)) and self.no_obstacles(start_row, start_col, end_row, end_col)

    def is_valid_king_move(self, start_col, start_row, end_col, end_row, target_piece):
        """Validate king movement."""
        return abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1

    def no_obstacles(self, start_row, start_col, end_row, end_col):
        row_step = 0 if start_row == end_row else 1 if start_row < end_row else -1
        col_step = 0 if start_col == end_col else 1 if start_col < end_col else -1

        row, col = start_row + row_step, start_col + col_step
        while row != end_row or col != end_col:
            if self.board[row][col] != ' ':
                return False
            row += row_step
            col += col_step

        return True

    def get_king_position(self, player):
        """Get the position of the king for the specified player."""
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'k' and player == 'white':
                    return i, j
                elif self.board[i][j] == 'K' and player == 'black':
                    return i, j
        return None

    def is_check(self, player):
        """Check if the player's king is in check."""
        king_row, king_col = self.get_king_position(player)

        for i in range(8):
            for j in range(8):
                if self.is_valid_move(j, i, king_col, king_row) and self.board[i][j].lower() == 'k':
                    return True

        return False

    def is_checkmate(self, player):
        """Check if the player is in checkmate."""
        king_row, king_col = self.get_king_position(player)

        # Check if the king can move to any valid square
        for i in range(king_row - 1, king_row + 2):
            for j in range(king_col - 1, king_col + 2):
                if self.is_valid_move(king_col, king_row, j, i) and not self.is_check(player):
                    return False

        # Check if any piece can capture the checking piece
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(j, i, king_col, king_row) and self.board[i][j].lower() == 'k':
                    return False

        return True

    def play_game(self):
        while not self.game_over:
            empty_board=[]
            for i in range(8):
                for j in range(8):
                    a = self.board[i][j]
                    empty_board.append(a)
            if not 'k' in empty_board:
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                print("-----------------------------------------")
                print(f"Checkmate! {self.current_player.capitalize()} wins! -")
                print("-----------------------------------------")
                break
            elif not 'K' in empty_board:
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                print("-----------------------------------------")
                print(f"Checkmate! {self.current_player.capitalize()} wins! -")
                print("-----------------------------------------")
                break
            
            self.display_board()
            move = input(f"Player {self.current_player}, enter your move (e.g., 'e2 e4'): ")
            self.make_move(move)


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.play_game()
