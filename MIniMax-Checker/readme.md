-------------------------------------------
### Problem - 1 (Raichu):
-------------------------------------------
Raichu was kind of like checkers for us, so we chose the Minimax algorithm with alpha beta pruning to determine our next move since Raichu is a two-person game and we presume that each player plays as optimally as possible.
Prior to writing the function for each piece, we first examined the movements of all the pieces (the Pichus, Pikachus, and Raichus) on the board. We also took into account the valid moves for each piece.

**Problem Description** <br>
We need to play the Game in such a way that our player plays optimal moves and our pieces(Pikachu and Pichu) prioritize becoming Raichu <br>
Initial state : Given an N*N board where (N >= 8) where we initially place all the Pichus and Pikachus <br>
State space : All the boards that we get when we try to move a piece on the board. <br>
Goal State: When there are no pieces remaining for any one of the players. <br>

**Evaluation Function** <br>
We are counting every piece still in play for the black and white side and assigning a weight based on how significant each piece is on the board for our evaluation function based on which the scores for the successor board are calculated, helping the minimax function in deciding the optimal next step.

**Minimax Function with alpha beta pruning** <br>
We initialize the minimum evaluation to negative infinity and the maximum evaluation to positive infinity with a depth of 4 to execute alpha beta pruning. Only the value of alpha will be updated by the Max player. Alpha begins with a value of negative infinity. The Min player will simply update the beta value. Beta is first set to positive infinity. When retracing the tree, node values will be given to upper nodes instead of alpha and beta values. Only the alpha and beta values will be sent to the child nodes. We traverse the successor boards from depth 4 until the depth is 0 or game is over.

**Challenges Faced** <br>
We added another component to our evaluation function which checks the number of pieces left from the opposing teams and gives it the maximum or minimum weight depending on the player after finding out that the evaluation function we wrote, that assigned weight to all the pieces did not produce optimal moves during testing. <br>
One other tricky part of part 1 was making moves for the pieces that became Raichu after reaching the opposite end and figuring out if the evaluation function will perform better if change the weight for Raichu. 
