# aarudua-hipath-sajairam-a1

<h1>Part 1: Birds, heuristics, and A* </h1>

<h2> OVERVIEW </h2>

The problem starts with 5 birds sitting on power line, we need to arrange them in ascending order as each birds are given a  number from 1 to 5 and we can move a bird with its adjacent bird. 


<h2> Abstraction </h2>

<li><b> Valid States </b ></li>
Move the birds with their adjacent neighbor bird one by one.

<li><b> Initial State </b></li>
The initial position of birds on the power line.For example in one of the case : 1 3 4 2 5

<li><b> Goal State</b></li>
The goal state in this problem is the - 1 2 3 4 5 (all the birds in sorted order)

<li><b> Cost Function</b></li>

The cost of moving a pair of bird should be 1. (taking pair wise step cost)

<li><b>Successor Function </b></li>
Moving a bird to the neighboring bird possible which can be achieved by RIGHT AND LEFT (except the birds on the edges. They can take only 1 action)


<h2>Approach</h2>
1.Initialize the priority queue to add states based on the cost

2.Need to keep track of visited nodes.

3.Put the cost(0), state(initial_state), and posssible path([]) in the fringe.

3, Find the next possible state from  current state, so we are taking pair of each of the bird in their current order.
4. We need to find cost function.

Total cost will be g_cost( how far the bird arrangments has reached from starting)+h_cost(how far the arrangments need to go)

<b>Heurisitic Function</b>
Need to check how many adjacent pair are not in ascending order.
 example- 13254- (1,3),(3,2),(2,5),(5,4)- here 2 pairs are not in correct position so , h = 2

<b>G_cost</b>
Increase g_Cost by 1 because moving a pair we considering it as a 1 step thing.

5. Pop the cost, current state and moves taken,(Now the state with least cost will be popped)
6. repeat the process till we reach the goal  1 2 3 4 5

<h1>Part 2: The 2022 Puzzle </h1>

<h2> OVERVIEW </h2>

Given a 5*5 board with 25 tiles and no empty space. We need solve the puzzle by performing Row, Column, Inner ring and Outer ring.


<h2> Abstraction </h2>

<li><b> Initial State </b></li>
The initial state is a 5*5 board with 25 tiles randomly arranged.

<li><b> Goal State</b></li>
The goal state in this problem is to arrange the tiles in the ascending order as:</br>
1  2  3  4  5</br>
6  7  8  9  10</br>
11 12 13 14 15</br>
16 17 18 19 20</br>
21 22 23 24 25</br>

<li><b> Cost Function</b></li>
The cost for moving per tile on the board is 1

<li><b>Successor Function </b></li>
Obtain possible boards by sliding the rows, columns, Inner ring and Outer ring elements by one position and wrapping around.



<h2>Approach</h2>
- Initialize a priority queue that has the states, moves made and the cost of each state as a fringe</br>
- Keep track the visited states to avoid re-considering them</br>
- Generate the successor states by performing these operations:</br>
    Operations:</br>
    Ri - Slide the ith Row of the board to right</br>
    Li - Slide the ith Row of the board to left</br>
    Ui - Slide the ith column of the board to up</br>
    Di - Slide the ith column of the board to </br>
    Oc - Slide the Outer ring elements clockwise</br>
    Occ - Slide the Outer ring elements counter-clockwise</br>
    Ic - Slide the Inner ring elements clockwise</br>
    Icc - Slide the Inner ring elements counter-clockwise</br>
- Find the tuned manhattan cost of each tile and calculate the weighted average</br>
- The board with the min cost will be considered as the next successor state. </br>
- Return the moves made and the #moves to reach the goal state if the goal state is obtained </br></br>


<b>Heurisitic Function</b>

We have calculated: </br>
- h(s) as the weighted average of tuned manhatten distance of each misplaced tile to its goal position</br>
- g(s) as the averahe path each tile travelled till the current state</br>
Total heuristic function is computed as f(s)= h(s) + g(s)</br></br>

<b>Question - 1</b>

In this problem, what is the branching factor of the search tree?</br>
- Each state has 24 successor states that are generated using Ri(5 states), Li(5 states), Ui(5 states), Di(5 states), Oc(1 state), Occ(1 state), Ic(1 state), Icc(1 state) => 5+5+5+5+1+1+1+1 = 24. </br>
- Hence, the branching factor the search tree is 24</br></br>

<b>Question - 2</b></br>

If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? </br>
- Given, solution can be reached in 7 moves</br>
- If Breadth First search is used, we should be exploring about 24^7 states before the goal is obtained</br>


<h1>Part 3</h1>

<h2> OVERVIEW </h2>

In this problem, we are trying to find the optimal path between two cities/ highway intersection based on different cost functions:
[“segments”,”distance”,”time”,”delivery”]. The road segments dataset has data regarding the connecting road such as distance, speed and highway name between the two cities/ highway intersection. The city gps dataset has data on latitude and longitude coordinates of the city.  

The city-gps dataset has no coordinate information for highways present.

<b>Handling missing coordinates in case of Highways:</b>

When we take a highway intersection to travel between two cities we see that the highway for obvious reasons does not have a latitude and longitude coordinates. The way we fix this is by taking the average of the neighboring cities' latitude and longitude coordinates. This is known as Triangulation. 

<h2>Abstraction</h2>
<li> Set of states S: The set of cities or highway intersections that can be visited on the map.</li>
<li> Successor function: Returns the city or intersection that is neighboring to the current junction/city on our route.</li>
<li> Initial State: Start city or highway intersection where we begin the trip</li>
<li> End State: Destination city or highway intersection where we end the trip</li><br/>
<br/>
<b> Cost: </b> 
<li>a. <b> Segments:</b> cost gets added by 1 </li>
<li>b. <b> Distance:</b> Adds the distance we have traveled to reach that point. </li>
<li>c. <b> Time:</b> Adds the time required to reach the point </li>
<li>d. <b> Delivery:</b> Time required by driver from previous point (depends on the cost of fallen package)</li>


 <h2>Search Algorithm:</h2>
The search begins with the start city/ highway. A priority queue is used to explore all possible routes/ states with the optimal cost function value (i.e. minimum value). We pick the best state in the priority queue(i.e. topmost value) and fetch its neighboring cities based on the costs given by the heuristic value and the actual cost( no of segments/ distance/ time/ delivery time between two points). We use the Haversine distance between two points as the heuristic. 



 <h2>Cost Functions we used: </h2> 

<li><b> Segments:</b> cost = segments + (havershine_distance/avg_segment_distance)</li>
<li><b> Distance:</b> cost = curr_distance + havershine_distance</li>
<li><b> Time:</b> cost = time + (havershine_distance/max_speed)</li>
<li><b> Delivery:</b> cost = delivery_time + (havershine_distance/max_speed)</li>
<br/>

The code returns the best path between the starting and ending point for a given cost function once it reaches the destination. 

References Used:<br/>
https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
