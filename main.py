from game import Game

game = Game()
board = game.board


def display_board(board):
    for row in board.board:
        for piece in row:
            if piece is None:
                print(".", end=" ")
            else:
                print(type(piece).__name__[0], end=" ")
        print()


print("Turn:", game.current_turn)

game.make_move((6, 4), (4, 4))
game.make_move((1, 4), (3, 4))
game.make_move((7, 6), (5, 5))
game.make_move((7, 6), (3, 5))

for move in game.move_history:
    print(move.start, "->", move.end)

display_board(board)
