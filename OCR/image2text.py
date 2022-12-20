#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# Aarushi Dua - aarudua
# Kalyani Malokar - kmalokar
# Sai Teja Burla - saburla
#
# (based on skeleton code by D. Crandall, Oct 2020)
#



from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }



#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]

train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


with open(train_txt_fname) as f:
    train_data = [line.rstrip('\n') for line in f]
#TRANSITION PROBABILTIES->

TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

trans_count={}
trans_prob={}

for line in train_data:
    for word_pos in range(len(line)):
       
        #FIND THE INITIAL COUNT AND PROBABILITY OF EACH CHARACTER IN THE SENTENCES
        #IF INDEX IS 0, MEANS BEFORE THAT CHARACTER THEIR WILL BE SPACE, 
        #SO INITIAL_COUNT[LINE[0]]== TRANS_COUNT[[LINE[0]]][' ']

        if word_pos==0 and line[0] not in trans_count:
            
            trans_count[line[0]]={}
            trans_count[line[0]][" "]=1
            
            trans_prob[line[0]]={}
            trans_prob[line[0]][" "]=1

        elif word_pos==0 and line[0] in trans_count:
            trans_count[line[0]][" "]+=1
            trans_prob[line[0]][" "]=1

        #NOW TRAVERSE THROUGH ALL THE NEXT CHARACTER AND FIND THE TRANSITION COUNT
        if word_pos>0:

            if line[word_pos] in trans_count:
                if line[word_pos-1] not in trans_count[line[word_pos]]:
                    trans_count[line[word_pos]][line[word_pos-1]]=1
                else:
                    trans_count[line[word_pos]][line[word_pos-1]]+=1
                    trans_prob[line[word_pos]][line[word_pos-1]]=1
            else:
                trans_count[line[word_pos]]={}
                trans_count[line[word_pos]][line[word_pos-1]]=1
                
                trans_prob[line[word_pos]]={}
                trans_prob[line[word_pos]][line[word_pos-1]]=1

#GET THE FINAL TRANSITION PROBABILTY
for word in trans_count:
    
    word_count = sum(trans_count[word].values())

    for prev_word in trans_count[word]:

         trans_prob[word][prev_word] = math.log(float(trans_count[word][prev_word])/ float(word_count))

#IS PREVIOUS STATE IS EMPTY, PROBABILTY OF HAVING NEXT EMPTY IS REALLY LESS
trans_prob[" "][" "] = -1000000

#EMISSION PROBABILITY->
test_letters = load_letters(test_img_fname)
emission_prob={}
for l_idx in range(len(test_letters)):
    score={}
    for letter,pattern in train_letters.items():
        star_count = 0
        train_star = 0
        test_star = 0
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if pattern[i][j] == '*':
                    train_star +=1 
                if test_letters[l_idx][i][j] == '*':
                    test_star +=1 
                if test_letters[l_idx][i][j] == pattern[i][j] == '*':
                    star_count += 1
        star_prob = (star_count + 1) / (train_star + test_star + 1)
        score[letter]=star_prob
    emission_prob[l_idx]=score

#SIMPLE PROBABILTY-

def simple_predict(test_letters):
    word_pred = []
    for i in range(len(test_letters)):  
        PROBS= list(emission_prob[i].values())
        chars= list(emission_prob[i].keys())
        if max(PROBS)==-float('inf') :
            word_pred.append(" ")
        else:
            max_Probability=PROBS.index(max(PROBS))
            word_pred.append(chars[max_Probability])
      
    
    return ''.join(word_pred)

#VERTERBI ALGORITHM ---
#REFERENCE- https://www.youtube.com/watch?v=IqXdjdOgXPM
#ABOVE VIDEO HELPED US TO UNDERSTAND THE WORKFLOW OF THE VITERBI 
#IN THIS APPROACH, WE find an optimal set of hidden states that maximizes the likelihood of observing the provided set of observations.
def hmm_viterbi(test_letters):

    #INITIALY STORE, PROBABILTY AS 0 AND PREVISOUS LETTER AS A in LOOK UP TABLE
    V_table = [[(0, TRAIN_LETTERS[0]) for i in range(len(TRAIN_LETTERS))] for j in range(len(test_letters))]

    x = 0
    #FILL THE PROBABILTY FOR THE FIRST PATTERN, PROB[CHAR]= INITIAL probability[CHAR]+LOG(EMISSION_PROB[CHAR])*FACTOR
    #if the image is noisy or if its charatcers are light, multiply emission factor by 40, to make it dominant 
    for char_ele in TRAIN_LETTERS:
        if char_ele in trans_prob and " " in trans_prob[char_ele]:
            V_table[0][x] = (trans_prob[char_ele][" "] + math.log(emission_prob[0][char_ele])*40,char_ele)
        else:
            V_table[0][x] = (-1000000, char_ele)
        x+=1
    #NOW FIND OUT THE MAX_PROBABILITY FROM PREVIOUS INDEX FROM v_table and find the next corresponding maximum probabilty for each letter
    for p in range(1, len(test_letters)):

        for q in range(len(TRAIN_LETTERS)):

            max_Probability = -1000000
            previous_ele = TRAIN_LETTERS[0]

            for r in range(len(TRAIN_LETTERS)):
                if TRAIN_LETTERS[q] in trans_prob and TRAIN_LETTERS[r] in trans_prob[TRAIN_LETTERS[q]]:
                    curr_trans_prob = trans_prob[TRAIN_LETTERS[q]][TRAIN_LETTERS[r]]

                else:
                    curr_trans_prob = -1000000

                if V_table[p-1][r][0] + curr_trans_prob > max_Probability:
                    max_Probability = V_table[p-1][r][0] + curr_trans_prob
                    previous_ele = V_table[p-1][r][1]

            V_table[p][q] = (max_Probability + math.log(emission_prob[p][TRAIN_LETTERS[q]])*40, previous_ele + TRAIN_LETTERS[q])
    
    ## backward to fetch optimal sequence
    max_Probability = -float('inf')   

    index_ele = 0
    for j in range(len(TRAIN_LETTERS)):
        if V_table[len(test_letters) - 1][j][0] > max_Probability:
            max_Probability = V_table[len(test_letters) - 1][j][0]   
            index_ele = j

    return V_table[len(test_letters) - 1][index_ele][1]

#CALL BOTH THE ALGORITHM TO PREDICT THE TEXT      
print("Simple: " + simple_predict(test_letters) )
print("   HMM: " + hmm_viterbi(test_letters))
