#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys  
from queue import PriorityQueue
import copy

ROWS=5
COLS=5


def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# return a list of possible successor states
def successors(state):
    moves = []

    for k in range (0,ROWS):
        moves.append((rotate_right(copy.deepcopy(state), k), "R"+str(k+1)))
        moves.append((rotate_left(copy.deepcopy(state), k), "L"+str(k+1)))
        moves.append((rotate_Up(copy.deepcopy(state), k), "U"+str(k+1)))
        moves.append((rotate_Down(copy.deepcopy(state), k), "D"+str(k+1)))

    moves.append((outer_rotate_clock(copy.deepcopy(state)), "Oc"))
    moves.append((outer_rotate_counter_clock(copy.deepcopy(state)), "Occ"))
    moves.append((inner_rotate_clock(copy.deepcopy(state)), "Ic"))
    moves.append((inner_rotate_counter_clock(copy.deepcopy(state)), "Icc"))

    return moves

#Rotate the ith row of the board to right
def rotate_right(map_cur, i):
    boardR=map_cur
    boardR[i] = boardR[i][-1:] + boardR[i][:-1]
    return boardR

#Rotate the ith row of the board to left
def rotate_left(map_cur, i):
    boardL=map_cur
    boardL[i] = boardL[i][1:] + boardL[i][:1]
    return boardL

#Rotate the ith column of the board up
#Finding the transpose of the board and performing row rotation to left
def rotate_Up(map_cur, i):
    col_up_board = [list(col) for col in zip(*map_cur)]
    col_up_board[i] = list(col_up_board[i][1:]) + [col_up_board[i][0]]
    col_up_board = [list(col) for col in zip(*col_up_board)]
    return col_up_board

#Rotate the ith column of the board down
#Finding the transpose of the board and performing the row rotation to right
def rotate_Down(map_cur, i):
    col_down_board = [list(col) for col in zip(*map_cur)]
    col_down_board[i] = [col_down_board[i][-1]] + list(col_down_board[i][:-1])
    col_down_board = [list(col) for col in zip(*col_down_board)]
    return col_down_board

#Rotating the outer ring elements of the board clock wise by one tile
#Referance: https://www.codeproject.com/Questions/5299028/
#Taking the elements of outer ring into a list, rotate the list and assign back rotated values to the board
def outer_rotate_clock(map_cur):
    values = map_cur[0][:-1] + [x[-1] for x in map_cur][:-1] + map_cur[-1][::-1][:-1] + [x[0] for x in map_cur][::-1][:-1]
    values = values[-1:] + values[:-1]
    idxs = [(0, j) for j in range(COLS)][:-1] + [(i, COLS - 1) for i in range(ROWS)][:-1] + [(ROWS - 1, j) for j in range(COLS)][::-1][:-1] + [(i, 0) for i in range(ROWS)][::-1][:-1]
    output = map_cur
    idx = 0
    for i, j in idxs:
        output[i][j] = values[idx]
        idx += 1
    return output

#Rotating the outer ring elements of the board counter clock wise by one tile
def outer_rotate_counter_clock(map_cur):
    values = map_cur[0][:-1] + [x[-1] for x in map_cur][:-1] + map_cur[-1][::-1][:-1] + [x[0] for x in map_cur][::-1][:-1]
    values = values[1:] + values[0:]
    idxs = [(0, j) for j in range(COLS)][:-1] + [(i, COLS - 1) for i in range(ROWS)][:-1] + [(ROWS - 1, j) for j in range(COLS)][::-1][:-1] + [(i, 0) for i in range(ROWS)][::-1][:-1]
    output = map_cur
    idx = 0
    for i, j in idxs:
        output[i][j] = values[idx]
        idx += 1
    return output

#Rotating the inner ring elements of the board clock wise by one tile
def inner_rotate_clock(map_cur_ic):
    inner_values_ic = map_cur_ic[1][1:-2] + [x[-2] for x in map_cur_ic][1:-2] + map_cur_ic[-2][::-1][1:-2] + [x[1] for x in map_cur_ic][::-1][1:-2]
    inner_values_ic = inner_values_ic[-1:] + inner_values_ic[:-1]
    inner_op = map_cur_ic
    inner_idxs = [(1, j+1) for j in range(COLS-1)][:-1] + [(i+1, COLS - 2) for i in range(ROWS)][1:-2] + [(ROWS - 2, j-1) for j in range(COLS-1)][::-1][:-2] + [(i, 1) for i in range(ROWS-2)][::-1][:-2]
    in_idx =0
    for m,n in inner_idxs:
        inner_op[m][n] = inner_values_ic[in_idx]
        in_idx = in_idx +1
    return inner_op

#Rotating the inner ring elements of the board counter clock wise by one tile
def inner_rotate_counter_clock(map_cur):
    inner_values = map_cur[1][1:-2] + [x[-2] for x in map_cur][1:-2] + map_cur[-2][::-1][1:-2] + [x[1] for x in map_cur][::-1][1:-2]
    inner_values = inner_values[1:] + inner_values[0:]
    inner_op = map_cur
    inner_idxs = [(1, j+1) for j in range(COLS-1)][:-1] + [(i+1, COLS - 2) for i in range(ROWS)][1:-2] + [(ROWS - 2, j-1) for j in range(COLS-1)][::-1][:-2] + [(i, 1) for i in range(ROWS-2)][::-1][:-2]
    in_idx =0
    for m,n in inner_idxs:
        inner_op[m][n] = inner_values[in_idx]
        in_idx = in_idx +1
    return inner_op

#Cost1- Manhattan distance without wrapping around
#Cost2- Manhattan distance with row and column wrapping around
#Cost3- Manhattan distance considering row wrap around
#Cost4- Manhattan distance considering column wrap around
def tiles_dist(x1,x2):
    len = abs(x1[0] - x2[0])
    height = abs(x1[1] - x2[1])
    #On board distance without wrapping aroing
    cost1 = len+height
    #Possible distances considering the R, L, U, D, WrapAround rotations
    cost2 = (COLS-len)+(ROWS-height)
    cost3 = (COLS-len)+height
    cost4 = len + (ROWS-height)
    return min(cost1, cost2, cost3, cost4)

#Fn to calculate the manhattan distance of given to its goal position
def heuristic_cost(curr_map, positions):
    dist_mh = 0
    for i in range(len(curr_map)):
        for j in range(len(curr_map[0])):
            if positions[curr_map[i][j]-1] != (i,j):
                dist_mh += tiles_dist((i,j), (positions[curr_map[i][j]-1]))
    return dist_mh

#Function to calculate the manhattan cost to the goal state
def heuristic_cost_rotate(curr_map, positions, rotation):
    dist_mh = 0
    dir = rotation[0]
    denom = 1
    if dir == 'R' or dir == 'L' or dir == 'U' or dir == 'D': 
        num = int(rotation[1:])
        denom = 5
    if dir == 'O' : denom = 16
    if dir == 'I' : denom = 8
    if dir == 'R' or dir == 'L':
        for j in range(COLS): dist_mh += tiles_dist((num-1,j), (positions[curr_map[num-1][j]-1]))
    elif dir == 'U' or dir == 'D':
        for i in range(COLS): dist_mh += tiles_dist((i,num-1), (positions[curr_map[i][num-1]-1]))
    if dir == 'O':
        idxs = [(0, j) for j in range(COLS)][:-1] + [(i, COLS - 1) for i in range(ROWS)][:-1] + [(ROWS - 1, j) for j in range(COLS)][::-1][:-1] + [(i, 0) for i in range(ROWS)][::-1][:-1]
        for m,n in idxs:
            dist_mh += tiles_dist((m,n), (positions[curr_map[m][n]-1]))
    elif dir == 'I':
        inner_idxs = [(1, j+1) for j in range(COLS-1)][:-1] + [(i+1, COLS - 2) for i in range(ROWS)][1:-2] + [(ROWS - 2, j-1) for j in range(COLS-1)][::-1][:-2] + [(i, 1) for i in range(ROWS-2)][::-1][:-2]
        for m,n in inner_idxs:
            dist_mh += tiles_dist((m,n), (positions[curr_map[m][n]-1]))

    return dist_mh


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    initial_board = list(initial_board)
    initial_state= []
    for i in range(5):
        initial_state.append(initial_board[5*i:5*(i+1)])
    print("-----",initial_state)
    final_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    
    
    fringe = PriorityQueue()
    fringe.put((0, initial_state, []))
    states_visited = []

    while fringe:
        (cost, state, moves_taken)=fringe.get()
        states_visited.append(state)

        #Check if the goal state is reached
        if state == final_state : return  moves_taken
        
        for move in successors(state):
            if move[0] not in states_visited:
                #Calculating the Heuristic Fns (Weighted Manhattan diatance)
                rotation = move[1]
                dir = rotation[0]
                denom = 1
                #Denominators to calculate the weighted average for each sliding operation
                #R,L,U,D operations are applied on 5 tiles at a time
                #Occ,Oc operations are applied on 16 tiles
                #Icc, Ic operations are applied on 8 tiles
                if dir == 'R' or dir == 'L' or dir == 'U' or dir == 'D': 
                    num = int(rotation[1:])
                    denom = 5
                if dir == 'O' : denom = 16
                if dir == 'I' : denom = 8

                rot_cost = heuristic_cost_rotate(move[0], positions, rotation)
                per_rot_cost = rot_cost/denom
                rem_cost = (heuristic_cost(move[0], positions) - rot_cost)/(25-denom)#h(s)
                cost = rot_cost+rem_cost+len(moves_taken)/25#h(s)+g(s), g(s) is the path traversed per tile so far
                fringe.put((cost, move[0], moves_taken + [move[1]]))

    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
