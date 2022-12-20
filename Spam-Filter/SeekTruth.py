# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
# Aarushi Dua - aarudua
# Kalyani Malokar - kmalokar
# Sai Teja Burla - saburla
#
# Based on skeleton code by D. Crandall, October 2021

import sys

def load_file(filename):
    
    objects=[]
    labels=[]
    
    with open(filename, "r") as f:
        
        for line in f:
            
            parsed = line.strip().split(' ',1)
            
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

def get_message(data):
    
    # To divide and store all the messages in two lists: deceptive and truthful
    deceptive_messages = []
    truthful_messages = []
    
    # To remove punctuations and stop words from the messages we wrote the following code
    punctuation_set = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    stop_words_set = "a also am an and are at be been but by can cant could for from get give goes had happen has how i if ill im in is isnt it its ive just keep let like make many may me no not now of only or our say see some take tell than that the their them then they this to try up us use used uses very want was way we what when where which who why will with wont you your youre"
    
    stop_words_list = stop_words_set.split(' ')
    
    for i in range(len(data['objects'])):
        # Converting the entire message into lower
        data['objects'][i] = data['objects'][i].lower()
        
        # Code to remove punctuations in the message
        for element in data['objects'][i]:
            if element in punctuation_set:
                data['objects'][i] = data['objects'][i].replace(element, "")
                
        message = data['objects'][i]
        message = message.split(' ')
        
        # Code to remove stopwords in the message
        for word in message:
            if word in stop_words_list:
                message.remove(word)
                
        message_string = ""
        for word in message:
            message_string = message_string + word + ' '
            
        data['objects'][i] = message_string
        
        # Segregating the messages into deceptive and truthful
        if data['labels'][i] == "deceptive":
            deceptive_messages.append(data['objects'][i])
        else:
            truthful_messages.append(data['objects'][i])
    
    # Returning lists of deceptive and truthful messages
    return deceptive_messages, truthful_messages

def get_words_count(data):
    
    # To store the count of each word in all the messages 
    words_count = {}
    
    # Loop to check through each message and each word in that message
    for message in data:
        
        words = message.split()
        
        for word in words:
            
            # If the word is already in the dictionary we just increment count by 1
            if word in words_count:
                words_count[word] = words_count[word] + 1
                
            # Else we initialise the word with count 1
            else:
                words_count[word] = 1
    
    # Return the dictionary with the counts of all words
    return words_count

def get_words_frequency(words_count):
    
    # To store the frequency of each word in all the messages
    words_frequency = {}
    
    for words, occurences in words_count.items():
        words_frequency[words] = (occurences / sum(words_count.values()), occurences)
    
    # Return the dictionary with the frequencies of all words
    return words_frequency

def get_words_deceptive_message(deceptive_words_frequency, truthful_words_frequency, initial_probability_deceptive, occurence_threshold):
    
    # To store the probability of each word belonging to a deceptive message
    deceptives = {}
    
    # Storing all words from both deceptive and truthful messages with frequencies
    words = set(list(deceptive_words_frequency) + list(truthful_words_frequency))
    
    for word in words:
        deceptive_words_occurences = deceptive_words_frequency[word][1] if word in deceptive_words_frequency else 0
        truthful_words_occurences = truthful_words_frequency[word][1] if word in truthful_words_frequency else 0
        
        # Condition to not include words if their frequency is below a certain threshold
        if deceptive_words_occurences + truthful_words_occurences >= occurence_threshold:
            
            # Condition to check if the words is in both deceptive and truthful messages
            if word in deceptive_words_frequency and word in truthful_words_frequency:
                
                # Calculating probability that a message containing a given word is deceptive
                # Formula for this is as follows:
                #                                    P(Word|Deceptive) * P(Deceptive)
                # P(Deceptive|Word) = -----------------------------------------------------------------
                #                     P(Word|Deceptive) * P(Deceptive) + P(Word|Truthful) * P(Truthful)
                
                deceptive_words_probability = deceptive_words_frequency[word][0] * initial_probability_deceptive
                truthful_words_probability = truthful_words_frequency[word][0] * (1 - initial_probability_deceptive)
                deceptives[word] = deceptive_words_probability / (deceptive_words_probability + truthful_words_probability)
            
            # Condition where the word is not present in deceptive messages
            elif deceptive_words_occurences == 0:
                deceptives[word] = 0.01
                
            # Condition where the word is not present in truthful messages
            elif truthful_words_occurences == 0:
                deceptives[word] = 0.99
    
    return deceptives

def get_words_truthful_message(deceptive_words_frequency, truthful_words_frequency, initial_probability_truthful, occurence_threshold):
    
    # To store the probability of each word belonging to a truthful message
    truthfuls = {}
    
    # Storing all words from both deceptive and truthful messages with frequencies
    words = set(list(deceptive_words_frequency) + list(truthful_words_frequency))
    
    for word in words:
        deceptive_words_occurences = deceptive_words_frequency[word][1] if word in deceptive_words_frequency else 0
        truthful_words_occurences = truthful_words_frequency[word][1] if word in truthful_words_frequency else 0
        
        # Condition to not include words if their frequency is below a certain threshold
        if deceptive_words_occurences + truthful_words_occurences >= occurence_threshold:
            
            # Condition to check if the words is in both deceptive and truthful messages
            if word in deceptive_words_frequency and word in truthful_words_frequency:
                
                # Calculating probability that a message containing a given word is truthful
                # Formula for this is as follows:
                #                                   P(Word|Truthful) * P(Truthful)
                # P(Truthful|Word) = ------------------------------------------------------------------
                #                     P(Word|Truthful) * P(Truthful) + P(Word|Deceptive) * P(Deceptive)
                
                deceptive_words_probability = deceptive_words_frequency[word][0] * (1 - initial_probability_truthful)
                truthful_words_probability = truthful_words_frequency[word][0] * initial_probability_truthful
                truthfuls[word] = truthful_words_probability / (deceptive_words_probability + truthful_words_probability)
            
            # Condition where the word is not present in truthful messages
            elif truthful_words_occurences == 0:
                truthfuls[word] = 0.01
                
            # Condition where the word is not present in deceptive messages
            elif deceptive_words_occurences == 0:
                truthfuls[word] = 0.99
    
    return truthfuls

# Definition to return the deceptive score of the message
def get_deceptive_score(message, words_deceptives):
    
    # We should ignore all the words that have not been encountered before
    main_message = []
    
    words = message.split()
    
    for word in words:
        if word.lower() in words_deceptives.keys():
            main_message.append(word.lower())
    
    # We need to get all the deceptives of the words in the message
    deceptives = [(words, words_deceptives[words]) for words in main_message]
    
    # We should get the top deceptives that are sorted by their distance from the neutral which is 0.5
    top_most_deceptives = sorted(deceptives, key=lambda i: abs(0.5 - i[1]), reverse = True)[:25]
    
    # Calculating probability that a message is deceptive 
    prob_deceptive = 1
    for i in top_most_deceptives:
        prob_deceptive = prob_deceptive * i[1]
        
    return prob_deceptive

# Definition to return the truthful score of the message
def get_truthful_score(message, words_truthfuls):
    
    # We should ignore all the words that have not been encountered before
    main_message = []
    
    words = message.split()
    
    for word in words:
        if word.lower() in words_truthfuls.keys():
            main_message.append(word.lower())
    
    # We need to get all the truthfuls of the words in the message
    truthfuls = [(words, words_truthfuls[words]) for words in main_message]
    
    # We should get the top truthfuls that are sorted by their distance from the neutral which is 0.5
    top_most_truthfuls = sorted(truthfuls, key=lambda i: abs(0.5 - i[1]), reverse=True)[:25]
    
    # Calculating probability that a message is truthful 
    prob_truthful = 1
    for i in top_most_truthfuls:
        prob_truthful = prob_truthful * i[1]
        
    return prob_truthful

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

def classifier(train_data, test_data):
    
    # Get initial probability of deceptive
    initial_probability_deceptive = train_data['labels'].count("deceptive")/len(train_data['labels'])
    #...
    initial_probability_truthful = train_data['labels'].count("truthful")/len(train_data['labels'])
    
    # Set a base threshold
    occurence_threshold = 10
    
    deceptive_train_message, truthful_train_message = get_message(train_data)
    
    # Getting word count of all the words in deceptive and truthful messages
    deceptive_train_words = get_words_count(deceptive_train_message)
    truthful_train_words = get_words_count(truthful_train_message)
    
    # Getting the frequency of all words from the deceptive and truthful messages
    deceptive_words_frequency = get_words_frequency(deceptive_train_words)
    truthful_words_frequency = get_words_frequency(truthful_train_words)
    
    # Getting probability for each word as to how much it can be linked to deceptive or truthful
    words_deceptives = get_words_deceptive_message(deceptive_words_frequency, truthful_words_frequency, initial_probability_deceptive, occurence_threshold)
    words_truthfuls = get_words_truthful_message(deceptive_words_frequency, truthful_words_frequency, initial_probability_truthful, occurence_threshold)
    
    # List to store the classification done by our code on the test data
    result = []
    
    for message in test_data["objects"]:
        
        # To get the probability that a message is deceptive or truthful
        deceptive_message_score = get_deceptive_score(message, words_deceptives)
        truthful_message_score = get_truthful_score(message, words_truthfuls)
        
        # Calculating the odds ratio of the message
        odds_ratio = deceptive_message_score/truthful_message_score
        
        # Classifying a message into deceptive or truthful based on the odds ratio
        if odds_ratio > 1:
              result.append("deceptive")
        else:
              result.append("truthful")
    
    # Returning the list of classifications done by our classifier on the test data
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
