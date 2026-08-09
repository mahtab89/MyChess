class Piece:
    def __init__(self, color):
        self.color = color

    def get_moves(self, board, position):
        raise NotImplementedError

    def get_sliding_moves(self, board, position, directions):
        moves = []

        row, col = position

        for row_dir, col_dir in directions:
            current_row = row + row_dir
            current_col = col + col_dir

            while 0 <= current_row < 8 and 0 <= current_col < 8:
                piece = board.board[current_row][current_col]

                if piece is None:
                    moves.append((current_row, current_col))
                else:
                    if piece.color != self.color:
                        moves.append((current_row, current_col))
                    break

                current_row += row_dir
                current_col += col_dir

        return moves

    def get_attacks(self, board, position):
        return self.get_moves(board, position)


class Pawn(Piece):
    def get_moves(self, board, position):
        moves = []
        row, col = position

        if self.color == "white":
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        new_row = row + direction

        if 0 <= new_row < 8 and board.board[new_row][col] is None:
            moves.append((new_row, col))

            if row == start_row:
                new_row = row + (2 * direction)

                if board.board[new_row][col] is None:
                    moves.append((new_row, col))

        for col_dir in (-1, 1):
            new_col = col + col_dir
            new_row = row + direction

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = board.board[new_row][new_col]

                if piece is not None and piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves

    def get_attacks(self, board, position):
        attacks = []

        row, col = position
        if self.color == "white":
            direction = -1
        else:
            direction = 1

        for col_dir in (-1, 1):
            new_row = row + direction
            new_col = col + col_dir

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                attacks.append((new_row, new_col))

        return attacks


class Rook(Piece):
    def get_moves(self, board, position):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.get_sliding_moves(board, position, directions)


class Knight(Piece):
    def get_moves(self, board, position):
        moves = []
        row, col = position

        directions = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for row_dir, col_dir in directions:
            new_row = row + row_dir
            new_col = col + col_dir

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = board.board[new_row][new_col]

                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves


class Bishop(Piece):
    def get_moves(self, board, position):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_sliding_moves(board, position, directions)


class Queen(Piece):
    def get_moves(self, board, position):
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        return self.get_sliding_moves(board, position, directions)


class King(Piece):
    def get_moves(self, board, position):
        moves = []
        row, col = position

        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row_dir, col_dir in directions:
            new_row = row + row_dir
            new_col = col + col_dir

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = board.board[new_row][new_col]

                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
