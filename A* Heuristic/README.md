# a0-release
<h1>Part 1: Navigation </h1>


<h2> OVERVIEW </h2>

Given a house consists of a grid of N × M cells where we need to find the shortest path that Michu will take to reach the goal where goal is indicated by “@“.
I used A * algorithm and mainly the search function needs to be updated  in order to find the optimal solution. I’ll discuss the approach in later section.

<h2> Problem with Given Code </h2>

The  code is taking one argument that is file name in which the house grid is given.
It is parsing the house map in a matrix form and passing that matrix in a search function.
Then, we need to know where pichu is, so pichu_loc contains that information. Add pacha’s location to fringe along with the cost and each step cost us 1 unit. Then code will loop till there’s no possible path to go.  POP the top node and store the current_move and distance. Now check what will the next step, pichu can only move in ‘.’ Space. Then if the next move contains the goal state, it’s returning a dummy answering, otherwise just append the move with it’s cost. That’s where the code lack some information. 

Pichu get stuck in an infinite loop because it’s just moving back and forth because it doesn’t have information regarding the visited nodes and how close it is to the goal state. So there are basically 3 things which I felt should be there: a) Information of the visited states. B) How close is pichu’s location to the goal ( which will be calculated using heurisitic function) C) Track of direction in which pichu is moving.

<h2> Abstraction </h2>

<li><b> Valid States </b ></li>
Consider the house has a grid for our search space. The possible states are where pichu can move on this grid of N*M But pichu can’t take states which contain wall in them which are denoted by “X” in the grid.

<li><b> Initial State </b></li>
The start position of pichu is the initial state and it is represented with coordinates (x,y).

<li><b> Goal State</b></li>
The goal state in this problem is where pichu wants to reach that is where “@“ coordinate is present in the grid.

<li><b> Cost Function</b></li>

The cost of moving for pichu to one state to another is 1 Because it can only take one step.

<li><b>Successor Function </b></li>
Moving pichu to the next possible available space can be achieved by 4 actions only UP, DOWN, RIGHT AND LEFT.


<h2>Approach</h2>
I have took Manhattan distance for finding the distance from pacha’s current location and goal location because there are only 4 moves possible.
So total cost in fringe will be
Cost =g(x)+h(x)
g(x)- cost of moving pichu to x position where each step cost us 1 unit.
And we will take that path which have least cost and try to explore their successive nodes first.  If possible move is our goal, then return the directions which this code is tracking and with the shortest distance. If no more node to traverse means there’s no path and then return -1.
I have explained the whole procedure with the below ppt.
https://docs.google.com/presentation/d/1y5rK4al6NQOjg4hZNlSq5nn0lo169xT4CGPWf_cYfMo/edit?usp=sharing




<h1>Part 2: Hide n seek</h1>


<h2> OVERVIEW </h2>
We want to place pichus on the house such that they can’t see each other and two agents(pichus) can see each other if they are on either the same row, column, or diagonal of the map, and there are no walls between them. 

I change the solve function by adding some rules.
Start with initial grid given, and add that to fringe. IF NUMBER OF AGENTS IS MORE THAN THE AVAILABLE SPACE than it’s not possible to find solution, so return NONE. Otherwise, find all the successor grid by placing pichu in the initial grid which satisfy 3 rules which are row safety , column safety and diagonal safety. Append the grid which pass the rule condition and if any grid is the goal state means number of agents has been achieved, Return that grid. Next take any grid out the fringe and start placing a pichu in available spaces. Loop through all possible grid till goal state is achieved or there’s no grid available in the fringe.






<h2> Abstraction </h2>

<li><b> Valid States </b ></li>
Consider the house has a grid for our search space. The possible states are where pichu can be placed on this grid of N*M But pichu can’t take states which contain wall in them which are denoted by “X” in the grid.

<li><b> Initial State </b></li>
There should be one pichu placed on the grid as the initial state and it is represented with coordinates (x,y).

<li><b> Goal State</b></li>
The goal state in this problem is all the required pichus are placed on the grid such that no two agents attack each other.

<li><b> Cost Function</b></li>

The cost of placing pichu is 0 .

<li><b>Successor Function </b></li>
Placing pichu to the available space which can be achieved by looking for ‘.’ On the grid.








