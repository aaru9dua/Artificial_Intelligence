# Elements of AI

## Assignment 2

-----------------
### TEAM MEMBERS:
-----------------

**Aarushi Dua - aarudua** <br>
**Kalyani Malokar - kmalokar** <br>
**Sai Teja Burla - saburla** <br>

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

-------------------------------------------
### Problem - 2 (Truth be Told):
-------------------------------------------

**Problem Description** <br>
We are given a user generated reviews dataset in which we have two types of reviews:
1. Deceptive - These reviews are basically fake reviews which could be a tactic by the hotel to improve their customer contact
2. Truthful - These reviews are real reviews given by actual people who stayed in a particular hotel which gives other people a good intuition about the hotel
<br> The problem statement here is to use a Bayesian Classifier to evaluate a specific review and classify it as Deceptive or Truthful.

**Pre-Processing of the Data** <br>
Two types of pre-processing was done on the given data:
1. Remove Punctuations from the Reviews
2. Remove Stop Words from the Reviews

**Our Solution** <br>
The following steps were done to get our solution:
1. We first get the count of all the words in deceptive and truthful reviews and store these values in a dictionary
2. Next we calculate frequencies of each of the words in deceptive and truthful reviews and store the same
3. Then we use the Bayesian Classifier Formula to get the probability of how much a word could be linked to deceptive or truthful review
4. Then we get the deceptive and truthful score for each review
5. Finally we compute the odds ratio by dividing the deceptive score by truthful score and comparing it with a threshold value which in this case is 1
6. If the divided value is greater than 1 then the review is classified as deceptive else it is classified as truthful
7. We store the classified values in a list and return it to compare with the test dataset which inturn would give us the accuracy of our model

**Results** <br>
The accuracy of our model is 82.75%

**Challenges Faced** <br>
When we were working on the code we realised that removing only a certain set of stop words can affect the overall accuracy of the code so we made a personalised list of stop words to get the accuracy we have with our current model.
