
import streamlit as st

from game.board import create_board, check_winner
from game.ai import ai_move
from game.logic import make_move


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)


# -----------------------------
# LOAD CSS
# -----------------------------

def load_css():

    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()


# -----------------------------
# SESSION STATE
# -----------------------------

if "board" not in st.session_state:
    st.session_state.board = create_board()

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "scores" not in st.session_state:
    st.session_state.scores = {
        "X": 0,
        "O": 0,
        "Draw": 0
    }

if "player" not in st.session_state:
    st.session_state.player = "X"

if "human_symbol" not in st.session_state:
    st.session_state.human_symbol = "X"

if "ai_symbol" not in st.session_state:
    st.session_state.ai_symbol = "O"

if "mode" not in st.session_state:
    st.session_state.mode = "Human vs AI"

if "message" not in st.session_state:
    st.session_state.message = ""


# -----------------------------
# RESET GAME
# -----------------------------

def reset_game():

    st.session_state.board = create_board()
    st.session_state.player = "X"
    st.session_state.game_over = False
    st.session_state.message = ""


# -----------------------------
# CHECK RESULT
# -----------------------------

def update_result():

    result = check_winner(st.session_state.board)

    if result is not None:

        st.session_state.game_over = True

        st.session_state.scores[result] += 1

        if result == "Draw":

            st.session_state.message = "🤝 Game Draw!"

        else:

            st.session_state.message = (
                f"🏆 Player {result} Wins!"
            )


# -----------------------------
# GAME TITLE
# -----------------------------

st.title("🎮 AI TIC-TAC-TOE")

st.caption(
    "Play with your friend or challenge Artificial Intelligence"
)


# -----------------------------
# GAME MODE
# -----------------------------

mode = st.selectbox(
    "Choose Game Mode",
    ["Human vs AI", "Human vs Human"],
    key="game_mode"
)

if mode != st.session_state.mode:

    st.session_state.mode = mode
    reset_game()


# -----------------------------
# SYMBOL SELECTION
# -----------------------------

st.subheader("Choose Your Symbol")

if not st.session_state.game_over:

    if mode == "Human vs AI":

        human_symbol = st.radio(
            "Select your symbol:",
            ["X", "O"],
            horizontal=True,
            key="human_choice"
        )

        st.session_state.human_symbol = human_symbol

        st.session_state.ai_symbol = (
            "O" if human_symbol == "X" else "X"
        )

        st.info(
            f"You are {human_symbol} | AI is {st.session_state.ai_symbol}"
        )

    else:

        player1_symbol = st.radio(
            "Player 1: Select your symbol:",
            ["X", "O"],
            horizontal=True,
            key="human_choice"
        )

        player2_symbol = (
            "O" if player1_symbol == "X" else "X"
        )

        st.info(
            f"Player 1: {player1_symbol} | Player 2: {player2_symbol}"
        )


# -----------------------------
# SCOREBOARD
# -----------------------------

st.subheader("📊 Scoreboard")

c1, c2, c3 = st.columns(3)

c1.metric("Player X", st.session_state.scores["X"])
c2.metric("Player O", st.session_state.scores["O"])
c3.metric("Draws", st.session_state.scores["Draw"])

st.divider()


# -----------------------------
# CURRENT TURN
# -----------------------------

if not st.session_state.game_over:

    st.subheader("🎯 Game Board")

    if mode == "Human vs AI":

        if st.session_state.player == st.session_state.human_symbol:
            st.write(f"Your Turn: {st.session_state.human_symbol}")
        else:
            st.write("AI is playing...")

    else:

        st.write(f"Current Turn: {st.session_state.player}")


# -----------------------------
# GAME BOARD
# -----------------------------

cols = st.columns(3)

for i in range(9):

    with cols[i % 3]:

        symbol = st.session_state.board[i]

        ai_turn = (
            mode == "Human vs AI"
            and st.session_state.player == st.session_state.ai_symbol
        )

        if st.button(
            symbol if symbol else " ",
            key=f"cell_{i}",
            use_container_width=True,
            disabled=(
                st.session_state.game_over
                or symbol != ""
                or ai_turn
            )
        ):

            if mode == "Human vs AI":

                # HUMAN MOVE

                make_move(
                    st.session_state.board,
                    i,
                    st.session_state.human_symbol
                )

                update_result()

                # AI MOVE

                if not st.session_state.game_over:

                    move = ai_move(
                        st.session_state.board,
                        st.session_state.ai_symbol
                    )

                    if move is not None:

                        make_move(
                            st.session_state.board,
                            move,
                            st.session_state.ai_symbol
                        )

                    update_result()

            else:

                # HUMAN VS HUMAN

                current = st.session_state.player

                make_move(
                    st.session_state.board,
                    i,
                    current
                )

                update_result()

                if not st.session_state.game_over:

                    st.session_state.player = (
                        "O" if current == "X" else "X"
                    )

            st.rerun()


# -----------------------------
# RESULT DISPLAY
# -----------------------------

if st.session_state.game_over:

    st.success(st.session_state.message)

    st.balloons()


# -----------------------------
# GAME CONTROLS
# -----------------------------

st.divider()

c1, c2 = st.columns(2)

with c1:

    if st.button("🔄 New Game", use_container_width=True):

        reset_game()
        st.rerun()

with c2:

    if st.button("🗑️ Reset Scores", use_container_width=True):

        st.session_state.scores = {
            "X": 0,
            "O": 0,
            "Draw": 0
        }

        reset_game()
        st.rerun()

