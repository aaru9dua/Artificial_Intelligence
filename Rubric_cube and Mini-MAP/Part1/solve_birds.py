#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
from queue import PriorityQueue
N=5

#####
# THE ABSTRACTION:

# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state

def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
def h(state):
    #Approach: Need to check how many adjacent pair are not in ascending order,
    # example- 13254- (1,3),(3,2),(2,5),(5,4)- here 2 pairs are not in correct position so , h = 2
    h_gap=0
    for t1, t2 in zip(state,state[1:]):
        #if next element is greater, increase the cost
        if t1>t2:
            h_gap+=1
    return h_gap

#########
#
# THE ALGORITHM:
#
# This is a generic solver using BFS. 
#
def solve(initial_state):

    #initialize the priority queue to add states based on the cost
    fringe = PriorityQueue()
    visited = [] # List to keep track of visited nodes.
    #
   #goal= [1,2,3,4,5]
   #initial cost is 0
    cost=0
    #put the cost, state, and posssible path
    fringe.put((cost,initial_state, []))
    #g_cost is how much step will it take to move to next path, we are moving birds one by one, so cost should increment by 1 
    g_cost=1
    #loop till fringe is empty
    while not fringe.empty():
        #pop the cost, current state and moves taken
        (cost,state, path) = fringe.get()

        #append the current state in visited
        visited.append(state)

        #if the birds are in the correct options, return the path 
        if is_goal(state):
            return path+[state,]

        
        #Number of moves possible
        for s in successors(state):
            
            if s not in visited:

                #find the heurisitic cost
                h_cost=h(s)

                #Total cost will be g_cost( how far the bird arrangments has reached from starting)+h_cost(how far the arrangments need to go)
                total_cost=h_cost+g_cost
                #put them in priority queue
                fringe.put((total_cost,s, path+[state,])) 
        
        #increase the g_cost
        g_cost+=1
        

    return []
  

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

    

