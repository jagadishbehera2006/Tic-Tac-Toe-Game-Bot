from game.board import check_winner, available_moves


def minimax(board, is_maximizing, ai_symbol, human_symbol):

    winner = check_winner(board)

    if winner == ai_symbol:
        return 1

    if winner == human_symbol:
        return -1

    if winner == "Draw":
        return 0

    if is_maximizing:

        best_score = float("-inf")

        for move in available_moves(board):

            board[move] = ai_symbol

            score = minimax(
                board, False, ai_symbol, human_symbol
            )

            board[move] = ""

            best_score = max(best_score, score)

        return best_score

    else:

        best_score = float("inf")

        for move in available_moves(board):

            board[move] = human_symbol

            score = minimax(
                board, True, ai_symbol, human_symbol
            )

            board[move] = ""

            best_score = min(best_score, score)

        return best_score


def ai_move(board, ai_symbol="O"):

    human_symbol = "X" if ai_symbol == "O" else "O"

    best_score = float("-inf")
    best_move = None

    for move in available_moves(board):

        board[move] = ai_symbol

        score = minimax(
            board, False, ai_symbol, human_symbol
        )

        board[move] = ""

        if score > best_score:

            best_score = score
            best_move = move

    return best_move