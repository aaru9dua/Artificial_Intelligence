#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Aarushi Dua AND aarudua]
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

#Function for heurisitc cost
def manhattan(position, goal):
    xy1 = position
    xy2 = goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


#In which direction is pichu moving, this function takes previous direction list, coordinates of pichu's current and previous location
def direction(dir1,curr_move,prev_move):

        #if X coordinate of current move is greater than previous, it has move down
        if curr_move[0]> prev_move[0]:
                dir1.append('D')
        #if X coordinate of current move is less than previous, it has move UP
        elif curr_move[0]<prev_move[0]:
                dir1.append('U')
        #if Y coordinate of current move is greater than previous, it has move Right
        elif curr_move[1]>prev_move[1]:
                dir1.append('R')
        #if Y coordinate of current move is less than previous, it has move Left
        elif curr_move[1]<prev_move[1]:
                dir1.append('L')
        return dir1

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):

        visited = [] # List to keep track of visited nodes.
        
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        #print(pichu_loc)

        # Find the goal position, in our case it's the coordinate of @
        goal_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        #print(goal_loc)

        #Add pichu's possible location to fringe with it's cost
        #IN MY CASE, THE COST FOR MOVING = g(X)+H(X) ,(where X :Current Location of Pichu)
        # where, g(x)=COST OF PICHU'S CURRENT LOCATION from start location(pichu_loc), where each movement cost us 1 unit.
        #h(x)= DISTANCE of PICHU'S CURRENT LOCATION from GOAL(goal_loc)

        fringe=[(pichu_loc,0)]
        

        #Store current location to previous, so that pichu can move to new one
        prev_move= pichu_loc

        #List for tracking pichu's direction
        dir=[]

        #Loop through all possible points in the node
        while fringe:

                #POP the top node and store the coordinates and distance
                (curr_move, curr_dist)=fringe.pop()

                #Mark the curr_move as visited
                visited.append(curr_move)

                #check in which direction it has moved
                dir=direction(dir,curr_move,prev_move)
               
                #Calculate g cost of pichu's possible location
                g=manhattan(curr_move,pichu_loc)
                
                #what will be the next move from curr_move which has least cost
                for move in moves(house_map, *curr_move):
                        
                        #if there's only one move and that too has been covered by pichu
                        #it means pichu can't take this path and it needs to go back to previous node which has different unvisited move
                        if len(moves(house_map, *curr_move))==1:
                                if move in visited:
                                        #remove the wrong direction
                                        dir.pop()

                        #if the possible move is our goal state, pichu has reached safely!
                        if house_map[move[0]][move[1]]=="@":
                                #check the final direction and append it to dir
                                dir=direction(dir,(move[0],move[1]),curr_move)
                                #Convert list items of direction to a string
                                dir=''.join(dir)
                                return (len(dir), dir)  # return the shortest path and direction

                        #if move is not goal, and is not visited, explore the possible moves from this         
                        elif move not in visited :

                                #calculate the distance from goal_loc
                                h=manhattan(move,goal_loc)

                                #toal cost
                                cost= (g+1)+(h)
                                
                                #Add the move with it's cost to fringe
                                fringe.append((move,cost))

                #Sort the node in such way that top item has minimum cost
                fringe=sorted(fringe, key=lambda t: t[1],reverse=True)

                #Now current move becomes previous move
                prev_move=curr_move
        
        #if no more node to traverse, means there's no path. return -1 
        return (-1,"") 
        
# Main Function
if __name__ == "__main__":
     
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])
            
        