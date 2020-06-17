"""
Tic Tac Toe Player
"""

import math
import copy
import random 

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
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    
    if action is not None and result_board[action[0]][action[1]] == EMPTY:
        next_player = player(board)
        result_board[action[0]][action[1]] = next_player
        return result_board
    else:    
        raise ImpossibleMoveError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_states = win_indexes(len(board))
    for indexes in win_states:
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
    
    return player_goal(winner_player)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # no more moves 
    if terminal(board):
        return None

    # get the current player
    cur_player = player(board)
    # best found option for max player (init opposite val)
    alpha = -2 
    # best found option for min player (init opposite val)
    beta = 2

    possible_actions = actions(board)
    if cur_player == X:
        # first move - return rand move
        if len(possible_actions) == 9:
            return get_random_move(len(board) -1)

        # max player 
        (b, best_move) = max_value(board, alpha, beta)
    else:
        # min player 
        (b, best_move) = min_value(board, alpha, beta)
    return best_move 
            

def min_value(board, alpha, beta):

    best_move = None

    # no more moves 
    if terminal(board):
        return (utility(board), best_move)

    best_min_val = 2

    possible_actions = actions(board)
    for action in possible_actions:
        next_board = result(board, action)
        (res_val, res_move) = max_value(next_board, alpha, beta)
        if best_min_val > res_val:
            best_min_val = res_val
            best_move = action

        #the alpha beta prunning part:
        if best_min_val <= alpha:
            return (best_min_val, best_move)

        if best_min_val < beta:
            beta = best_min_val

    return (best_min_val, best_move)  


def max_value(board, alpha, beta):

    best_move = None

    # no more moves 
    if terminal(board):
        return (utility(board), best_move)

    best_max_val = -2

    possible_actions = actions(board)
    for action in possible_actions:
        next_board = result(board, action)
        (res_val, res_move) = min_value(next_board, alpha, beta)
        if best_max_val < res_val:
            best_max_val = res_val
            best_move = action

        #the alpha beta prunning part:
        if best_max_val >= beta:
            return (best_max_val, best_move)

        if best_max_val > alpha:
            alpha = best_max_val

    return (best_max_val, best_move)  



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


def player_goal(player):
     return 1 if player == X else -1

def get_random_move(max):
    i = random.randrange(max)
    j = random.randrange(max)
    return (i, j)