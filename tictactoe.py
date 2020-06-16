"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter = {"X":0, "O":0}

    for i in board:
        for j in i:
            if j is not None:
                counter[j] +=1
            
    return X if counter['X'] == counter['O'] else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in board:
        for j in i:
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    
    if result_board[action[0]][action[1]] == EMPTY:
        next_player = player(board)
        result_board[action[0]][action[1]] = next_player
        return result_board
    else:    
        raise ImpossibleMoveError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for indexes in win_indexes(len(board)):
        if all(board[r][c] == X for r, c in indexes):
            return X
        if all(board[r][c] == O for r, c in indexes):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in board:
        if i.count(EMPTY) > 0:
            return False

    # no more moves
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player is None:
        return 0
    
    return 1 if winner_player == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


def win_indexes(n):
    # Rows
    for r in range(n):
        yield [(r, c) for c in range(n)]
    # Columns
    for c in range(n):
        yield [(r, c) for r in range(n)]
    # Diagonal top left to bottom right
    yield [(i, i) for i in range(n)]
    # Diagonal top right to bottom left
    yield [(i, n - 1 - i) for i in range(n)]
