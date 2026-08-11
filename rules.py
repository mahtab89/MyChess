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
    def is_square_attacked(board, square, defending_color):
        enemy_color = "black" if defending_color == "white" else "white"

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None and piece.color == enemy_color:
                    attacks = piece.get_attacks(board, (row, col))

                    if square in attacks:
                        return True

        return False

    @staticmethod
    def is_in_check(board, color):
        king_pos = Rules.find_king(board, color)

        if king_pos is None:
            return False

        return Rules.is_square_attacked(board, king_pos, color)

    @staticmethod
    def is_legal_move(board, start, end, color):
        piece = board.board[start[0]][start[1]]

        if piece is None:
            return False

        if piece.color != color:
            return False

        possible_moves = piece.get_moves(board, start)
        if piece.__class__.__name__ == "King":
            possible_moves += Rules.get_castling_moves(board, start, color)

        if end not in possible_moves:
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

        if piece.__class__.__name__ == "King":
            possible_moves += Rules.get_castling_moves(board, position, color)

        legal_moves = []

        for move in possible_moves:
            if Rules.is_legal_move(board, position, move, color):
                legal_moves.append(move)

        return legal_moves

    @staticmethod
    def is_checkmate(board, color):
        if not Rules.is_in_check(board, color):
            return False

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None and piece.color == color:
                    legal_moves = Rules.get_legal_moves(board, (row, col), color)

                    if legal_moves:
                        return False

        return True

    @staticmethod
    def is_stalemate(board, color):
        if Rules.is_in_check(board, color):
            return False

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None and piece.color == color:
                    legal_moves = Rules.get_legal_moves(board, (row, col), color)

                    if legal_moves:
                        return False

        return True

    @staticmethod
    def get_castling_moves(board, position, color):
        moves = []

        king = board.board[position[0]][position[1]]

        if (
            king is None
            or king.__class__.__name__ != "King"
            or king.color != color
            or king.has_moved
            or Rules.is_in_check(board, color)
        ):
            return moves

        row = position[0]

        # king side castling
        rook = board.board[row][7]
        if (
            rook is not None
            and rook.__class__.__name__ == "Rook"
            and not rook.has_moved
            and board.board[row][5] is None
            and board.board[row][6] is None
            and not Rules.is_square_attacked(board, (row, 5), color)
            and not Rules.is_square_attacked(board, (row, 6), color)
        ):
            moves.append((row, 6))

        # Queen side castling
        rook = board.board[row][0]
        if (
            rook is not None
            and rook.__class__.__name__ == "Rook"
            and not rook.has_moved
            and board.board[row][1] is None
            and board.board[row][2] is None
            and board.board[row][3] is None
            and not Rules.is_square_attacked(board, (row, 3), color)
            and not Rules.is_square_attacked(board, (row, 2), color)
        ):
            moves.append((row, 2))

        return moves
