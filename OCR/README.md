

-------------------------------------------
### Problem - 1 (Part-of-Speech Tagging):
-------------------------------------------

**Problem Description** <br>
We are given a sentence as an input and we need to tag every word of that sentence as a part of speech like noun, verb, adjective, etc. We have to implement 3 types of models for solving the same. They are as follows:
1. Simplified Model
2. HMM using Viterbi Algorithm 
3. Complicated MCMC Model using Gibbs Sampling <br>

We also have to print the percentage of number of words labelled correct and number of sentences labelled correct by all the three models.

**Our Solution** <br>
We have implemented all the models and their explanation are as follows:

**Simplified Model** <br>
In this model we perform the following steps: <br>
1. We first take the sentence as the input
2. We loop through the sentence getting each word separately
3. We then loop through each of the 12 tags and calculate the emission pobability of the word given the tag and multiply that value with the initial probability of the tag and store it in a list
4. Then we take the maximum value of all these values to determine which tag we should assign for that particular word
5. Then we return the tag as the solution <br>

For this model we got the following results: <br>
a. 92.52% - accuracy for number of words that are tagged correctly <br>
b. 40.60% - accuracy for number of sentences that are tagged correctly

**HMM using Viterbi Algorithm** <br>
In this model we made use of three probabilities: <br>
1. Initial probability - we check the probability of the tags(parts of speech) occurring at the start of each sentence  
2. Emission probability - the probability of getting a word associated with a part of speech
3. Transition probability - the probability that a particular word associated with one part of speech is followed by a certain part of speech <br>
We then made use of these probabilities to tag each word of the sentence. <br>

For this model we got the following results: <br>
a. 93.47% - accuracy for number of words that are tagged correctly <br>
b. 46.30% - accuracy for number of sentences that are tagged correctly

**Complicated MCMC Model using Gibbs Sampling** <br>
In this model we perform the following steps: <br>
For this part the training model incorporates a more complex Bayes net, with each part of speech based on two parts of speech 
which were present before the word in consideration.<br>
Thus transition probabilities from the third word in a sentence to two earlier sections of speech are examined in this technique.<br>
Initially, we give a set of tags to each word from hmm prediction, and then we take each word and assign all 12 parts of speech to it. For each word, we compute the posterior probabilty with this formula - P(S_{i}|S-S_{i},W) = (P(S_{1})P(W_{1}|S_{1})P(S_{2}|S_{1})P(S_{3}|S_{1},S_{2})….P(S_{n}|S_{n-1},S_{n-2})<br>
 
After calculating the posterior we try and reoraganize the elements with the following formula:<br>
P(S_{1}){P(S_{2}|S_{1})P(S_{3}|S_{2})…P(S_{n}|S_{n-1})}{P(S_{3}|S_{1},S_{2})….P(S_{n}|S_{n-1},S_{n-2})}{P(W_{1}|S_{1})…P(W_{n}|S_{n})}<br>
a tag is then assigned at random to the reorganized element/word from randonly picked normalised proababilties,<br>
We then fix the the selected parts of speech to the word and utilize this changed value in further calculations<br>
We repeat this process for all of the words once and a sample will be generated. This simulation takes place over a 100 times.<br>
After a few initial iterations (50-in our case), the tag that appears the most consistently for a word is assigned as the final tag/part of speech from the remaining samples.<br>
 

For this model we got the following results: <br>
a. 93.56% - accuracy for number of words that are tagged correctly <br>
b. 46.35% - accuracy for number of sentences that are tagged correctly

-------------------------------------------
### Problem - 2 (Reading Text):
-------------------------------------------

**Problem Description** <br>
The problem here is to extract text from a noisy scanned image of a document. All the texts have the same fixed-width font. Each letter is made up of 16 * 25 pixels. An assumption for the document is that it contains 26 upper case letters, 26 lower case letters, 0-9 numbers, spaces and 7 punctuation symbols((),.-!?'"). We have to implement 2 types of models for solving the same. They are as follows:
1. Simplified Model
2. HMM using Viterbi Algorithm <br>

As a result we print the sentences formed by both of the models.

**Our Solution** <br>
We have implemented both the models and their explanation are as follows:

**Simplified Model** <br>
In this model we perform the following steps: <br>
1. We take the train set of character's and the test image set of character's in the form of space's and star's
2. We then compare every character in test character's with every train character respectively and get the count of how many star's coincide for both
3. We make a probability out of that by taking star's matching count divided by count of star's in train and count of star's in test (we added 1 to numerator and denominator to avoid math division error)
4. We then appended all these values for each of the test character to a dictionary
5. From the dictionary we check each test character and find the max of the probability in that test character's set of values this would be the character that best coincides with the test character
6. We take the character from above and append it to the final sentence and return it as the result for this model

**HMM using Viterbi Algorithm** <br>
1. Fill the probability of getting each character at 0th index using the formula: PROB[CHAR]= INITIAL probability[CHAR]+LOG(EMISSION_PROB[CHAR])*FACTOR
2. If the image is noisy or if its character's are faded, we multiply the emission factor by 40, to make it dominant 
3. Next we find out the maximum probability from the previous index using the lookup table and find the next corresponding maximum probabilty for each letter
4. Update the lookup table with the sum of transition and emission probabilities and the previos character will get updated to previous character plus the character with the maximum probability
5. Backtrack to fetch the optimum sentence

**Challenges Faced** <br>
For each and every sentence the noise level in images were different and some image were light and some distorted, so finding a common scalar factor for emission probability proved to be very difficult. This is the reason why some of the characters are not predicted correctly.
