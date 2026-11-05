
WINNING_POSITIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]


def create_board():
    return [""] * 9


def check_winner(board):

    for a, b, c in WINNING_POSITIONS:

        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def available_moves(board):
    return [i for i in range(9) if board[i] == ""]
