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
