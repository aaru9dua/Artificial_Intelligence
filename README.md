# Elements of AI

## Assignment 2

-----------------
### TEAM MEMBERS:
-----------------

**Aarushi Dua - aarudua** <br>
**Kalyani Malokar - kmalokar** <br>
**Sai Teja Burla - saburla** <br>


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
