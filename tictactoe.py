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
    possible_actions = actions(board)
    if cur_player == X:
        # first move - return rand move
        if len(possible_actions) == 9:
            i = random.randrange(len(board) -1)
            j = random.randrange(len(board) -1)
            return (i, j)

        # max player 
        for action in possible_actions:
            next_board = result(board, action)
            if min_value(next_board) == 1:
                return action #optimal move
        for action in possible_actions:
            next_board = result(board, action)
            if min_value(next_board) == 0:
                return action #neutral move    
        return action[0] #no good/neutral moves, return the first possible
    else:
        # min player 
        for action in possible_actions:
            next_board = result(board, action)
            if max_value(next_board) == -1:
                return action #optimal move
        for action in possible_actions:
            next_board = result(board, action)
            if max_value(next_board) == 0:
                return action #neutral move    
        return action[0] #no good/neutral moves, return the first possible
            

def min_value(board):
    # no more moves 
    if terminal(board):
        return utility(board)

    best_val = 2
    possible_actions = actions(board)
    for action in possible_actions:
        next_board = result(board, action)
        best_val = min(best_val, max_value(next_board))
    return best_val  

def max_value(board):
    # no more moves 
    if terminal(board):
        return utility(board)

    best_val = -2
    possible_actions = actions(board)
    for action in possible_actions:
        next_board = result(board, action)
        best_val = max(best_val, min_value(next_board))
    return best_val  



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

# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     # no more moves 
#     if terminal(board):
#         return None

#     # get the current player
#     cur_player = player(board)

#     # get players goal (1 or -1)
#     goal = player_goal(cur_player)

#     # find best action out of the available ones
#     possible_actions = actions(board)
#     neutral_action = set()
#     non_optimal_action = set()

#     for action in possible_actions:
#         # get actions result
#         next_board = result(board, action)
#         move_result = utility(next_board)
    
#         if move_result == 0:
#             neutral_action.add(action)
#         else:
#             if move_result == goal:
#                 #  good move found
#                 return action
#             else:   
#                 non_optimal_action.add(action)

#     if len(neutral_action) > 0:
#         # return first neutral move
#         return neutral_action.pop()
#     else:
#         # no good/neutral moves, return what's left
#         return non_optimal_action.pop()
             