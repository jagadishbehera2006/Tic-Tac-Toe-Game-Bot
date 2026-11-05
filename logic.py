from game.board import check_winner


def make_move(board, position, player):

    if board[position] != "":
        return False

    if check_winner(board) is not None:
        return False

    board[position] = player

    return True


def get_game_result(board):
    return check_winner(board)


def is_game_over(board):
    return check_winner(board) is not None
