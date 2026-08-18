from engine.game import Game
from engine.piece import King, Pawn, Queen, Rook


def test_kingside_castling_through_game():
    game = Game()

    game.board.board[7][5] = None
    game.board.board[7][6] = None

    king = game.board.board[7][4]
    rook = game.board.board[7][7]

    result = game.make_move((7, 4), (7, 6))

    assert result is True

    assert game.board.board[7][6] is king
    assert game.board.board[7][5] is rook

    assert game.board.board[7][4] is None
    assert game.board.board[7][7] is None

    assert king.has_moved is True
    assert rook.has_moved is True

    assert game.current_turn == "black"


def test_queenside_castling_through_game():
    game = Game()

    # Clear squares between king and rook
    game.board.board[7][1] = None
    game.board.board[7][2] = None
    game.board.board[7][3] = None

    king = game.board.board[7][4]
    rook = game.board.board[7][0]

    result = game.make_move((7, 4), (7, 2))

    assert result is True

    assert game.board.board[7][2] is king
    assert game.board.board[7][3] is rook

    assert game.board.board[7][4] is None
    assert game.board.board[7][0] is None

    assert king.has_moved is True
    assert rook.has_moved is True

    assert game.current_turn == "black"


def test_pawn_promotion_through_game():
    game = Game()

    for row in range(8):
        for col in range(8):
            game.board.board[row][col] = None

    pawn = Pawn("white")
    game.board.board[1][4] = pawn

    game.current_turn = "white"

    result = game.make_move((1, 4), (0, 4), "queen")

    assert result is True
    assert isinstance(game.board.board[0][4], Queen)
    assert game.board.board[1][4] is None
    assert game.current_turn == "black"


def test_halfmove_clock_starts_at_zero():
    game = Game()

    assert game.halfmove_clock == 0


def test_halfmove_clock_increments_after_quiet_move():
    game = Game()

    result = game.make_move((7, 1), (5, 2))

    assert result is True
    assert game.halfmove_clock == 1


def test_halfmove_clock_resets_after_pawn_move():
    game = Game()

    # Knight move
    assert game.make_move((7, 1), (5, 2)) is True
    assert game.halfmove_clock == 1

    # Black pawn move
    assert game.make_move((1, 0), (2, 0)) is True
    assert game.halfmove_clock == 0


def test_halfmove_clock_resets_after_capture():
    game = Game()

    # Clear the board
    for row in range(8):
        for col in range(8):
            game.board.board[row][col] = None

    white_rook = Rook("white")
    black_pawn = Pawn("black")

    game.board.board[4][4] = white_rook
    game.board.board[4][7] = black_pawn

    game.current_turn = "white"
    game.halfmove_clock = 10

    assert game.make_move((4, 4), (4, 7)) is True

    assert game.halfmove_clock == 0


def test_position_history_tracks_positions():
    game = Game()

    assert len(game.position_history) == 1

    initial_position = game.position_history[0]

    # White knight b1 → c3
    assert game.make_move((7, 1), (5, 2)) is True

    # Black knight b8 → c6
    assert game.make_move((0, 1), (2, 2)) is True

    # White knight c3 → b1
    assert game.make_move((5, 2), (7, 1)) is True

    # Black knight c6 → b8
    assert game.make_move((2, 2), (0, 1)) is True

    assert len(game.position_history) == 5
    assert game.position_history[-1] == initial_position


def test_game_status_playing():
    game = Game()

    assert game.get_game_status() == "playing"


def test_game_status_insufficient_material():
    game = Game()

    for row in range(8):
        for col in range(8):
            game.board.board[row][col] = None

    game.board.board[7][4] = King("white")
    game.board.board[0][4] = King("black")

    assert game.get_game_status() == "draw_insufficient_material"


def test_game_status_fifty_move_draw():
    game = Game()

    game.halfmove_clock = 100

    assert game.get_game_status() == "draw_fifty_move"


def test_game_status_threefold_draw():
    game = Game()

    position = game.get_position_key()

    game.position_history = [
        position,
        ("other", "black"),
        position,
        ("another", "white"),
        position,
    ]

    assert game.get_game_status() == "draw_threefold"


def test_game_status_checkmate():
    game = Game()
    board = game.board
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    board.board[0][0] = King("black")
    board.board[1][1] = Queen("white")
    board.board[2][2] = King("white")

    game.current_turn = "black"

    assert game.get_game_status() == "checkmate_white"


def test_game_status_stalemate():
    game = Game()

    board = game.board
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    board.board[0][0] = King("black")
    board.board[1][2] = Queen("white")
    board.board[2][2] = King("white")

    game.current_turn = "black"

    assert game.get_game_status() == "stalemate"
