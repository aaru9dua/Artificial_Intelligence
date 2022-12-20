###################################
# CS B551 Fall 2022, Assignment #3
#
# Your names and user ids:
# Aarushi Dua - aarudua
# Kalyani Malokar - kmalokar
# Sai Teja Burla - saburla
#
# (Based on skeleton code by D. Crandall)


import random
import math
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.


class Solver:


    def __init__(self):

        self.tags=['det','noun','adj','verb','adp','.','adv','conj','prt','pron','num','x']
        self.TotalTag=0

        self.PosCount={}
        self.tag_prob={}

        self.words=[]
        self.initial_prob={}
        self.unique_words=[]

        self.word_observation={}
        self.emission_prob={}

        self.tag_transition={}
        self.tag_transition_prob={}
        
        self.tag_2_transition={}
        self.tag_2_transition_prob={}


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!


    def posterior(self, model, sentence, label):

        # If condition to check which algorithm is given as an input
        # And calculate the posterior probability based on this input
        if model == "Simple":

            # Variable to calculate and store posterior probability 
            # We initialise it with 1 as we perform multiplication through out
            posterior_probability = 1

            # For loop that iterates through each of the categories and elements in the train file (this could be words or punctuations)
            for i in range(len(label)):

                # Variable to store the category and the word at the ith index
                word_tags = label[i]
                word_from_lines = sentence[i]

                # If condition to check if the word from above is in the emission probability
                # If yes then we check the probability of the category assigned to it 
                # Else if the probability of the category given the word is 0 then we take the probability as 0.00001
                if word_from_lines in self.emission_prob and self.emission_prob[word_from_lines][word_tags] != 0:
                    posterior_probability = posterior_probability * self.emission_prob[word_from_lines][word_tags] * self.tag_prob[word_tags]

                else:
                    posterior_probability = posterior_probability * 0.00001  * self.tag_prob[word_tags]
            
            # If the poseterior probability is 0 then we assign it to 0.00001
            if posterior_probability == 0:
                posterior_probability = 0.00001

            # Finally we return the log of the calculated posterior probability
            return math.log10(posterior_probability)

        elif model == "HMM":

            posterior_probability = 1

            for i in range(len(label)):

                word_tags = label[i]
                word_from_lines = sentence[i]

                if word_from_lines in self.emission_prob and self.emission_prob[word_from_lines][word_tags] != 0:
                    posterior_probability = posterior_probability * self.emission_prob[word_from_lines][word_tags]

                else:
                    posterior_probability = posterior_probability * 0.00001
            
            # We multiply the probability of category i to the posterior probability calculated so far
            posterior_probability = posterior_probability * self.tag_prob[label[0]]

            # For loop to multiply transition probabilities
            for i in range(1, len(label)):

                if self.tag_transition_prob[label[i-1]][label[i]] != 0:
                    posterior_probability = posterior_probability * self.tag_transition_prob[label[i-1]][label[i]]

                else:
                    posterior_probability = posterior_probability * 0.00001
            
            if posterior_probability == 0:
                posterior_probability = 0.00001

            return math.log10(posterior_probability)

        elif model == "Complex":

            posterior_probability_c = self.random_probabilty(sentence, label)

            return posterior_probability_c
        
        # If the algorithm is not recognised we simply print the following message
        else:

            print("Unknown Algorithm!!!")


    # Function for training the model
    def train(self, data):

        for words, tags in data:

            # To count the number of tags in training sentences 
            self.TotalTag+=len(tags)

            for i in range(len(words)):

                if tags[i] not in self.PosCount:
                    self.PosCount[tags[i]]=1

                else:
                    self.PosCount[tags[i]]+=1

                self.words.append(words[i])

        self.unique_words=list(set(self.words))

        # Calculating initial probability for s1, s2, sN
        for tag, count in self.PosCount.items():

            self.initial_prob[tag]= count/self.TotalTag

        # Calculating emission count for the observed words from a particular tag
        for words, tags in data:

            for i in range(len(words)):
                
                if words[i] not in self.word_observation:

                    self.word_observation[words[i]]={}
                    self.word_observation[words[i]][tags[i]]=1

                elif words[i] in self.word_observation:

                    if tags[i] not in self.word_observation[words[i]]:
                        self.word_observation[words[i]][tags[i]]=1

                    else:
                        self.word_observation[words[i]][tags[i]]+=1

        # Emission Probability
        for word, tag_count in self.word_observation.items():

            for tag in self.tags:

                if word not in self.emission_prob:
                    self.emission_prob[word]={}

                if tag in self.word_observation[word]:
                    self.emission_prob[word][tag]= self.word_observation[word][tag]/self.PosCount[tag]

                else:
                    self.emission_prob[word][tag]=0.00001

        # To calculate tag's transition count    
        for words, tags in data:

            for i in range(1,len(words)):
                
                    if tags[i] not in self.tag_transition:

                        self.tag_transition[tags[i]]={}
                        self.tag_transition[tags[i]][tags[i-1]]=1

                    elif tags[i] in self.tag_transition:
                   
                        if tags[i - 1] in self.tag_transition[tags[i]]:
                                self.tag_transition[tags[i]][tags[i - 1]] += 1

                        else:
                                self.tag_transition[tags[i]][tags[i - 1]] = 1
                                
                    if i>1:
                        
                        if tags[i] in self.tag_2_transition:

                            if tags[i - 1] in self.tag_2_transition[tags[i]]:

                                if tags[i - 2] in self.tag_2_transition[tags[i]][tags[i - 1]]:
                                    self.tag_2_transition[tags[i]][tags[i - 1]][tags[i - 2]] += 1

                                else:
                                    self.tag_2_transition[tags[i]][tags[i - 1]][tags[i - 2]] = 1

                            else:

                                self.tag_2_transition[tags[i]][tags[i - 1]] = {}
                                self.tag_2_transition[tags[i]][tags[i - 1]][tags[i - 2]] = 1

                        else:

                            self.tag_2_transition[tags[i]] = {}
                            self.tag_2_transition[tags[i]][tags[i - 1]] = {}
                            self.tag_2_transition[tags[i]][tags[i - 1]][tags[i - 2]] = 1
                        
        # Calculate transition probability for HMM
        for curr_tag,prev_tag in self.tag_transition.items():

            for tag in self.tags:

                if curr_tag not in self.tag_transition_prob:
                    self.tag_transition_prob[curr_tag]={}

                if tag in prev_tag:
                    self.tag_transition_prob[curr_tag][tag]= prev_tag[tag]/self.PosCount[tag]

                else:
                    self.tag_transition_prob[curr_tag][tag]=0.00001
         
        # Calculate transition probability for MCMC
        for curr_tag,prev_tag in self.tag_2_transition.items():

            if curr_tag not in self.tag_2_transition_prob:
                    self.tag_2_transition_prob[curr_tag]={}

            for prev_tag in self.tags:

                if prev_tag in self.tag_2_transition[curr_tag]:

                    if prev_tag not in self.tag_2_transition_prob[curr_tag]:
                         self.tag_2_transition_prob[curr_tag][prev_tag]={}

                    for prev_tag2 in self.tags:

                        if prev_tag2 in self.tag_2_transition[curr_tag][prev_tag]:
                            self.tag_2_transition_prob[curr_tag][prev_tag][prev_tag2]=self.tag_2_transition[curr_tag][prev_tag][prev_tag2]/self.tag_transition[prev_tag][prev_tag2]

                        else:
                            self.tag_2_transition_prob[curr_tag][prev_tag][prev_tag2]=0.00001

                else:
            
                    if prev_tag not in self.tag_2_transition_prob[curr_tag]:
                         self.tag_2_transition_prob[curr_tag][prev_tag]={}

                    for prev_tag2 in self.tags:
                        self.tag_2_transition_prob[curr_tag][prev_tag][prev_tag2]=0.00001
        
        for pos in self.PosCount.keys():
            self.tag_prob[pos] = self.PosCount[pos]/ self.TotalTag


    def simplified(self, sentence):

            #si = arg maxsi(P(Si = si|W)).
            predict_tag=[]
           
            for word in sentence:

                total_prob=[]

                for tag in self.tags:

                    if word in self.emission_prob:
                        prob_tag_w=self.emission_prob[word][tag]

                    else:
                        prob_tag_w=0.00001
                        
                    total_prob.append((self.initial_prob[tag]*prob_tag_w,tag))

                max_prob=max(total_prob)
                predict_tag.append(max_prob[1])
                
            return predict_tag

    
    # Referenced from - https://medium.com/@phylypo/nlp-text-segmentation-using-hidden-markov-model-f238743d87eb
    #Reference from - https://www.youtube.com/watch?v=IqXdjdOgXPM
    #The above mentioned resoureces helped us understand the workflow of Viterbi  
    def hmm_viterbi(self, sentence):
     
        V_table= [{}]

        # To get the probability of current state and store the previous visited state
        for tag in self.tags:

            if sentence[0] in self.emission_prob:
                V_table[0][tag] = {"p": self.initial_prob[tag] * self.emission_prob[sentence[0]][tag], "prev": None}

            else:
                V_table[0][tag] = {"p": self.initial_prob[tag] * 0.00001, "prev": None}
            
        for obs in range(1, len(sentence)):

            V_table.append({})

            for tag in self.tags:

              max_tr_prob = V_table[obs - 1][self.tags[0]]["p"] * self.tag_transition_prob[tag][self.tags[0]]
              prev_st_selected = self.tags[0]
                
              # To find the max probability from the previous states
              for prev_st in self.tags[1:]:

                  tr_prob = V_table[obs - 1][prev_st]["p"] * self.tag_transition_prob[tag][prev_st]

                  if tr_prob > max_tr_prob:

                      max_tr_prob = tr_prob
                      prev_st_selected = prev_st

              if sentence[obs] in self.emission_prob:
                  max_prob = max_tr_prob * self.emission_prob[sentence[obs]][tag]

              else:
                  max_prob = max_tr_prob *0.00001

              V_table[obs][tag] = {"p": max_prob, "prev": prev_st_selected}
            
        sequence = []
        max_prob = 0
        bestState = None

        for st, prob in V_table[-1].items():

          if prob["p"] > max_prob:

                max_prob = prob["p"]
                bestState = st

        sequence.append(bestState)
        prev_state = bestState

        # Here you'll have a loop that backtracks to find the most likely state sequence
        for t in range(len(V_table) - 2, -1, -1):

            sequence.insert(0, V_table[t + 1][prev_state]["prev"])
            prev_state = V_table[t + 1][prev_state]["prev"]

        return sequence
    
    #to calculate the probabilty for complex model
    def random_probabilty(self,sentence, predicted_pos):

            # Variable to store the length of the input sentence
            s_len = len(sentence)

            # Variable to store and initialising probability to 0
            probable = 0

            # For loop that runs for the length of the sentence
            for i in range(s_len):


                words = sentence[i]
                position = predicted_pos[i]

                # If the given particular word is not in emission_prob then we assign x to a very small number
                if words not in self.emission_prob:
                    x = 0.00001

                # Else we assign x to the emission_prob value for a word in a particular position
                else:
                    x = self.emission_prob[words][position]

                # Adding the x value to the probability
                probable = probable + math.log(x)

                # To calculate Transition probability for S(n)
                if i == 0:
                    probable = probable + math.log(self.tag_prob[position])

                # To calculate Transition probability for S(n-1)
                elif i == 1:

                    pos_1 = predicted_pos[i - 1]
                    probable = probable + math.log(self.tag_transition_prob[position][pos_1])

                # To calculate Transition probability for S(n-2)
                else:

                    pos_1 = predicted_pos[i - 1]
                    pos_2 = predicted_pos[i - 2]
                    probable = probable + math.log(self.tag_2_transition_prob[position][pos_1][pos_2])

            # Returning the probability    
            return probable
    
    # Referenced from - http://www2.stat.duke.edu/~rcs46/modern_bayes17/lecturesModernBayes17/lecture-7/07-gibbs.pdf
    def complex_mcmc(self,sentence):
        
        predicted_pos = self.hmm_viterbi(sentence)

        init_pred = predicted_pos

        sample_mcmc = []

        # Function to use gibbs sampling on the sentence
        def gibbs(sentence, init_pred):
            
            #DIFFERENT SAMPLE POSITION OF TAGS
            sample_position = list(init_pred)

            s_len = len(sentence)
            
            #RANDOMLY ASSIGN A TAG TO A WORD
            for i in range(s_len):

                position, position_probability = [], []

                for curr_pos in self.tags:

                    position.append(curr_pos)

                    sample_position[i] = curr_pos
                    #GET THE PROBABILTY FOR CURRENT SENTENCE BY ASSIGNING TAG TO ith words and s_len-ith words will get predited tag from hmm
                    current_position_probability= self.random_probabilty(sentence, sample_position)
                    
                    #store the exponential probabilty
                    position_probability.append(math.exp(current_position_probability))
                #sum up the probabilities 
                gibbs_sum = sum(position_probability)
                
                #if gibs_sum is zero, assgin the starting position only
                if gibbs_sum == 0:
                    sample_position[i] = position[0]

                else:
                    #store the probabilty by normalizing all of them with gibbs_sum
                    temp_prob = [x / gibbs_sum for x in position_probability]
                    #and then randomly choose the tag from given normalized probabilty
                    sample_position[i] = np.random.choice(position, p=temp_prob)

            return sample_position
        
        # LET'S RESAMPLE ASSIGNING OF RANDOM TAGS TO THE WORDS, 100 TIMES AND SEE WHERE IT'S CONVERGING QUICKLY
        for j in range(0, 100):
            #pass the sentence with initial predicted prob from hmm
            sample_predicted = gibbs(sentence, init_pred)
            #After 50 iterations, the predicted pos were coming pretty quickly.
            if j > 50:
                sample_mcmc.append(sample_predicted)
           
        #ZIP ALL THE PREDICTED TAGS AFTER 50 ITERATIONS FOR EACH WORD
        columns = list(zip(*sample_mcmc))
        
        #LOOP THROUGH EACH WORD AND GET MAX OF A PREDICTED TAG
        predicted_pos = [max(set(k), key=k.count) for k in columns]

        # Returning the predicted solutions
        return predicted_pos
        
    
    def solve(self, model, sentence):
            if model == "Simple":
                return self.simplified(sentence)
            elif model == "HMM":
                return self.hmm_viterbi(sentence)
            elif model == "Complex":
                return self.complex_mcmc(sentence)
            else:
                print("Unknown algo!")
