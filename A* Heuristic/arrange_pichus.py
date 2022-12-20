#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Aarushi Dua AND aarudua]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    #check the count of agents and if that's statisfy the rules
    return count_pichus(house_map) == k and rule(house_map)

#Define the row condition, that no pichu's should be placed in same row with no walls in between.
def row_safety(grid,r,c):

    #LOOP THROUGH ROW
    for x in range(r):
        
        #Initiate count of pichu's in that row
        Pcount=0
        #move to next column
        for y in range(c):

            #if we found p here, increament the count
            if 'p' in grid[x][y]:
                Pcount+=1

            #if while traversing, wall ('X') came, reduce the count of p. because we can place p after this wall
            elif 'X' in grid[x][y]:
                #don't do anything if P hasn't come in the row
                if Pcount==0:
                    pass
                else:
                    Pcount-=1
            #if the Pcount reaches 2 after another P encounter,means no wall came in between to reduce the count.
            if Pcount ==2 :
                #Hence 'row clash' happens, discard the grid
                return False

    #otherwise grid is row safely
    return True


#Define the column condition, that no pichu's should be placed in same column with no walls in between.
def col_safety(grid,r,c):

    #LOOP THROUGH COLUMNS
    for y in range(c):

        #Initiate count of pichu's in that COLUMN
        Pcount=0

        #move to next ROW
        for x in range(r):
            
            #if we found p here, increament the count
            if 'p' in grid[x][y]:
                Pcount+=1

            #if while traversing, wall ('X') came, reduce the count of p. because we can place p after this wall

            elif 'X' in grid[x][y]:
                #don't do anything if P hasn't come in the column
                if Pcount==0:
                    pass
                else:
                    Pcount-=1
            #Same as row saftey logic
            if Pcount ==2 :
                #Hence 'column clash' happen, discard the grid
                return False
    #otherwise, grid is column safely
    return True


#Define the diagonal condition, that no pichu's should be placed in same diagonals
#PROBLEM FACED: I found a bit difficult to keep track of forawrd elements and backward elements in a diagonal
#So i did some research, I found a peice of code which helps me in building this function
#https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
#here I put the reference from where i  took first 7 lines of code for this function.
def diag_safety(grid,r,c):
    
    #All the forward and backward elements  in a diagonal, has r+c-1 elements 
    fdiag = [[] for _ in range(r + c - 1)]
    bdiag = [[] for _ in range(r+c-1)]
    min_bdiag = -r + 1

    #loop through the grid
    for x in range(c):
        for y in range(r):
            #Notice, forward diagnol elements have their x+y coordinates same
            fdiag[x+y].append(grid[y][x])
            #backward diagnl elements have their x-y same , but in order to store elements in list, a element has been added to store it into positive index
            bdiag[x-y-min_bdiag].append(grid[y][x])

    #Again loop through both forward and backward diagonal list and keep track of count of P as described in row and col safety
    for i in fdiag:
        count=0
        for j in i:
            if j=='p':
                count+=1

            elif j=='X':
                if count==0:
                    pass
                else:
                    count-=1


            if count ==2 :
                #print('diag clash')
                return False

    for i in bdiag:
        count=0
        for j in i:
            if j=='p':
                count+=1

            elif j=='X':
                if count==0:
                    pass
                else:
                    count-=1

            if count ==2 :
                #print('diag clash')
                return False
    #Grid is diagonal safely
    return True

#Define all the row, column and diagonal conditions in a rule, pass a grid
def rule(grid):
    #store row and column
    r=len(grid)
    c=len(grid[0])
    #if all the three functions return TRUE that means grid is perfect.
    return row_safety(grid,r,c) and col_safety(grid,r,c) and diag_safety(grid,r,c)
     
    

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    #Add initial house grid to fringe
    fringe = [initial_house_map]
    

    #IF NUMBER OF AGENTS IS MORE THAN THE AVAILABLE SPACE.
    #COUNT DOT FOR AVAILABLE SPACE IN THE GRID
    dotCount=0
    for r in range(len(initial_house_map)):
        for c in range(len(initial_house_map[0])):
            #IF DOT FOUND, INCREASE COUNT BY 1
            if initial_house_map[r][c]=='.':
                dotCount+=1
    #if agents are more than space, return none
    if k>dotCount:
        return None

    #LOOP THROUGH ALL POSSIBLE GRIDS, till there's no possible grid in fringe
    while len(fringe) > 0:

        #Find the successor of a grid, by placing p into the new grid
        for new_house_map in successors( fringe.pop() ):
            
            #check if new house grid satisfy rules that we define
            if rule(new_house_map):

                #append the grid into fringe
                fringe.append(new_house_map)
            
            #if this grid our goal state
            if is_goal(new_house_map,k):
                
                #return the grid 
                return(new_house_map,True)
  


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)


    

    print ("Here's what we found:")
    #pass false if solution is None
    if solution == None:
        print('False')
    else:
        #print the grid is there's a solution
        print (printable_house_map(solution[0]))

