Problem Description
We are given a sentence as an input and we need to tag every word of that sentence as a part of speech like noun, verb, adjective, etc. We have to implement 3 types of models for solving the same. They are as follows:

Simplified Model
HMM using Viterbi Algorithm
Complicated MCMC Model using Gibbs Sampling
We also have to print the percentage of number of words labelled correct and number of sentences labelled correct by all the three models.

Our Solution
We have implemented all the models and their explanation are as follows:

Simplified Model
In this model we perform the following steps:

We first take the sentence as the input
We loop through the sentence getting each word separately
We then loop through each of the 12 tags and calculate the emission pobability of the word given the tag and multiply that value with the initial probability of the tag and store it in a list
Then we take the maximum value of all these values to determine which tag we should assign for that particular word
Then we return the tag as the solution
For this model we got the following results:
a. 92.52% - accuracy for number of words that are tagged correctly
b. 40.60% - accuracy for number of sentences that are tagged correctly

HMM using Viterbi Algorithm
In this model we made use of three probabilities:

Initial probability - we check the probability of the tags(parts of speech) occurring at the start of each sentence
Emission probability - the probability of getting a word associated with a part of speech
Transition probability - the probability that a particular word associated with one part of speech is followed by a certain part of speech
We then made use of these probabilities to tag each word of the sentence.
For this model we got the following results:
a. 93.47% - accuracy for number of words that are tagged correctly
b. 46.30% - accuracy for number of sentences that are tagged correctly

Complicated MCMC Model using Gibbs Sampling
In this model we perform the following steps:
For this part the training model incorporates a more complex Bayes net, with each part of speech based on two parts of speech which were present before the word in consideration.
Thus transition probabilities from the third word in a sentence to two earlier sections of speech are examined in this technique.
Initially, we give a set of tags to each word from hmm prediction, and then we take each word and assign all 12 parts of speech to it. For each word, we compute the posterior probabilty with this formula - P(S_{i}|S-S_{i},W) = (P(S_{1})P(W_{1}|S_{1})P(S_{2}|S_{1})P(S_{3}|S_{1},S_{2})….P(S_{n}|S_{n-1},S_{n-2})

After calculating the posterior we try and reoraganize the elements with the following formula:
P(S_{1}){P(S_{2}|S_{1})P(S_{3}|S_{2})…P(S_{n}|S_{n-1})}{P(S_{3}|S_{1},S_{2})….P(S_{n}|S_{n-1},S_{n-2})}{P(W_{1}|S_{1})…P(W_{n}|S_{n})}
a tag is then assigned at random to the reorganized element/word from randonly picked normalised proababilties,
We then fix the the selected parts of speech to the word and utilize this changed value in further calculations
We repeat this process for all of the words once and a sample will be generated. This simulation takes place over a 100 times.
After a few initial iterations (50-in our case), the tag that appears the most consistently for a word is assigned as the final tag/part of speech from the remaining samples.

For this model we got the following results:
a. 93.56% - accuracy for number of words that are tagged correctly
b. 46.35% - accuracy for number of sentences that are tagged correctly
