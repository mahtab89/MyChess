import piece


class Rules:
    @staticmethod
    def find_king(board, color):
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None and (
                    piece.color == color and piece.__class__.__name__ == "King"
                ):
                    return (row, col)

        return None

    @staticmethod
    def is_in_check(board, color):
        king_pos = Rules.find_king(board, color)

        if king_pos is None:
            return False

        enemy_color = "black" if color == "white" else "white"

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None and piece.color == enemy_color:
                    attacks = piece.get_attacks(board, (row, col))

                    if king_pos in attacks:
                        return True

        return False

    @staticmethod
    def is_legal_move(board, start, end, color):
        piece = board.board[start[0]][start[1]]

        if piece is None:
            return False

        if piece.color != color:
            return False

        if end not in piece.get_moves(board, start):
            return False

        move = board.move_piece(start, end)

        if move is None:
            return False

        in_check = Rules.is_in_check(board, color)

        board.undo_move(move)

        return not in_check

    @staticmethod
    def get_legal_moves(board, position, color):
        piece = board.board[position[0]][position[1]]

        if piece is None:
            return []

        if piece.color != color:
            return []

        possible_moves = piece.get_moves(board, position)
        legal_moves = []

        for move in possible_moves:
            if Rules.is_legal_move(board, position, move, color):
                legal_moves.append(move)

        return legal_moves
