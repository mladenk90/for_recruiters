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
    # iniitial count
    count_X = 0
    count_O = 0
    
    # loop through rows
    for row in range(len(board)):
        # loop through columns
        for col in range(len(board[row])):
            # update count per X or O
            if board[row][col] == X:
                count_X += 1
            if board[row][col] == O:
                count_O += 1
    # print X or O in selected slot
    if count_X > count_O:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # variable to return set
    all_actions = set()
    
    # loop through rows
    for row in range(len(board)):
        # loop through columns starting at first column
        for col in range(len(board[0])):
            # check if blank slot
            if board[row][col] == EMPTY:
                # add X or O to (i,j) pair of row,col selected
                all_actions.add((row,col))
                
    return all_actions    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # confirm via actions function that it is a valid action on the board
    if action not in actions(board):
        raise Exception("Invalid Action")
    # confirm via action (i,j) pair selected
    row, col = action
    # deep copy of board
    copy_of_board = copy.deepcopy(board)
    # confirm (i,j) pair for specific user board via player function
    copy_of_board[row][col] = player(board)
    # print deepcopy board
    return copy_of_board
# define function to scan rows to implement in winner function
def scan_row(board, player):
    """
    Scans through rows looking for winning cells
    """
    # loop through rows
    for row in range(len(board)):
        # confirm if 3 aligned rows are matching one player for win
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # if not 3 consecutive rows for player
    return False
# define function to scan columns to implement in winner function
def scan_col(board, player):
    """
    Scans through columns looking for winning cells
    """
    # loop through columns
    for col in range(len(board)):
        # confirm if 3 aligned columns are matching one player for win
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # if not 3 consecutive columns for player
    return False
# define function to scan diagonal results from top to bottom to implement in winner function
def scan_top2botdiag(board, player):
    """
    Scans through diagonal results from top to bottom looking for winning cells
    """
    # initial count
    count = 0
    # loop through rows
    for row in range(len(board)):
        # loop through columns
        for col in range(len(board[row])):
            # check if row and column on board match player
            if row == col and board[row][col] == player:
                # if yes, add one to count
                count +=1
    # if 3 in a row from top to bot diagonal for one player, then winner
    if count == 3:
        return True
    else:
        return False
            
# define function to scan diagonal results from top to bottom to implement in winner function
def scan_bot2topdiag(board, player):
    """
    Scans through diagonal results from bottom to top looking for winning cells
    """
    # initial count
    count = 0
    # loop through rows
    for row in range(len(board)):
        # loop through columns
        for col in range(len(board[row])):
            # check if row and column on board match player
            if (len(board) - row - 1) == col and board[row][col] == player:
                # if yes, add one to count
                count +=1
    # if 3 in a row from top to bot diagonal for one player, then winner
    if count == 3:
        return True
    else:
        return False
    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # implement scan row, column and both diagonal functions for X
    if scan_row(board, X) or scan_col(board, X) or scan_top2botdiag(board, X) or scan_bot2topdiag(board,X):
        return X
    # implement scan row, column and both diagonal functions for O
    elif scan_row(board, O) or scan_col(board, O) or scan_top2botdiag(board, O) or scan_bot2topdiag(board,O):
        return O
    # if no winner
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # implement winner function to check for X
    if winner(board) == X:
        return True
    # implement winner function to check for O
    if winner(board) == O:
        return True
    # loop through remaining cells
    # loop through rows
    for row in range(len(board)):
        # loop through columns
        for col in range(len(board[row])):
            # check if cell is empty
            if board[row][col] == EMPTY:
                return False
    # if game is over
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # implement 1 for winner is X in terminal
    if winner(board) == X:
        return 1
    # implement -1 for winner is O in terminal
    elif winner(board) == O:
        return -1
    # implement 0 for tie in terminal
    else:
        return 0
# def funcntion for max_value using notes
def max_value(board):
    """
    Maximum value function for maximizing player.
    """
    # variable for -∞
    v = -math.inf  
    if terminal(board):
        return utility(board)
    # for maximizing user
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
# def funcntion for min_value using notes
def min_value(board):
    """
    Minimum value function for minimizing player.
    """
    # variable for ∞
    v = math.inf  
    if terminal(board):
        return utility(board)
    # for minimizing user
    for action in actions(board):
        v = max(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # initialize terminal
    if terminal(board):
        return None
    # if player is X(max)
    elif player(board) == X:
        # create empty list for player choices
        player_choice = []
        # loop through possible actions
        for action in actions(board):
            # add player choice list with min_value and action
            player_choice.append([min_value(result(board,action)),action])
        # reverse sort to get next best choice
        return sorted(player_choice, key=lambda x: x[0], reverse=True)[0][1]
    
    # if player is O(min)
    elif player(board) == O:
        # create empty list for player choices
        player_choice = []
        # loop through possible actions
        for action in actions(board):
            # add player choice list with max_value and action
            player_choice.append([max_value(result(board,action)),action])
        # reverse sort to get next best choice
        return sorted(player_choice, key=lambda x: x[0], reverse=True)[0][1]

