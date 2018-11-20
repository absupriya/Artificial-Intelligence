#!/usr/bin/env python2
# geolocate.py : Tweets classification
# Supriya Ayalur Balasubramanian, 26-Oct-2018
# A classic application of Bayes Law is in document classification. Let's examine one particular classification problem: 
# Estimating where a Twitter "tweet" was sent, based only on the content of the tweet itself. We'll use a bag-of-words model, 
# which means that we'll represent a tweet in terms of just an unordered bag of words instead of modeling anything about its grammatical structure.
# ***********************************************************************************************
# Run commands: 
# ./geolocate.py training-file testing-file output-file
# ./geolocate.py tweets.train.clean.txt tweets.test1.clean.txt Output.txt

'''
******************************Comments**************************************
Following design decisions was tried upon before finalizing the code:
1. Ignore words that do not appear more than a handful of times. When I implemented in the code, I was getting low accuracy. 
   I ignored those words having count less than 20,15,10,5,3,2. None of them was giving more accuracy than 68.2%.
2. Filtering words with numbers, alphanumeric characters too didn't give me good accuracy.
3. I tried ignoring words of length more than 4 (for stopwords) but then we will loose out on the city shortnames like MA, CA, TX etc.
4. I used an array of stopwords (reference from "http://xpo6.com/list-of-english-stop-words/") and filtered them to create a bag of words model.
5. I am substituing the special characters with '' and then stripping them out from the tweets.
6. Punctuations are removed. The tweet message is converted to lower case for easy modelling and probability calcuations
7. My preproceesing function will retain all words irrespective of its length, alphanumerics and numbers expect for the stopwords from the array defined.
8. Bag of words model is created on the above cleansed tweet which is defined as a dictionary of dictionary.
9. If a word from the testing file is unavailable in the bagofwords, then a very small probability is assigned to that word. 
   After multiple trial and errors, I found that 1/1000000 is giving me good accuracy.
10. For the training and testing datasets given to us, my program gives an accuracy of 68.2% in about 35-40 seconds. 
   The time taken is dependent on the machine configuration and server load on silo.
******************************Comments**************************************
'''

import sys
import re
import operator

# Cleaning the data, create a bag of words model and tweets count for each city
def preprocess_trainfile(trainfile):
    with open(trainfile,'r') as ipfile:
        file=ipfile.readlines()
        for line in file:
            city=line.split()[0]
            message=filter(str.strip,(re.sub(r"(\&amp)|[\W_']+",'',w.lower()) for w in line.split()[1:])) # Replacing the symbols using regex commands
            message=filter(lambda twt:twt not in stopwords, message) # Filtering stopwords
            tweetscountsincity[city]=(1 if city not in tweetscountsincity.keys() else tweetscountsincity[city]+1) #Count of tweets for each city
            bagofword(city,message) # Creates the bag of words for each line

# Counting the number of words that appear for the same city and storing it in a dictionary 'bagofwords'
def bagofword(city,msg):
    if city in bagofwords.keys():
        for wrd in msg:
            bagofwords[city][wrd]=(bagofwords[city][wrd]+1 if wrd in bagofwords[city].keys() else 1)
    else:
        bagofwords[city]={}
        for wrd in msg:
            bagofwords[city][wrd]=(bagofwords[city][wrd]+1 if wrd in bagofwords[city].keys() else 1)

# Calculate the probability of location given words, i.e, P(L/w1,w2,w3...)
def probabilityofcitygivenword(gcity,gmsg):
    for gcity in tweetscountsincity.keys():
        probofcity=float(tweetscountsincity[gcity])/sum(tweetscountsincity.values()) #Calculate the probability of the city,i.e P(L)
        probwordgcity=1
        for gword in gmsg:
            if gword in bagofwords[gcity].keys():
                probwordgcity=probwordgcity*(float(bagofwords[gcity][gword])/sum(bagofwords[gcity].values())) #Calculate P(w1/l)*P(w2/L)*P(w3/L)...
            else:
                probwordgcity=probwordgcity*(float(1)/(1000000))
        posteriorprob=probwordgcity*probofcity  #Calculate the posterior probability P(l/w)=P(w/L)*P(L)
        probcitygivenword[gcity]=posteriorprob
    return max(probcitygivenword.items(),key=operator.itemgetter(1))[0]  #Pick the city that has the max probability for the tweet

# Predict for the testing file
def predict(testfile):
    for line in testfile:
        city=line.split()[0]
        origtweet=line.split()[1:]
        message=filter(str.strip,(re.sub(r"(\&amp)|[\W_']+",'',w.lower()) for w in origtweet)) # Replacing the symbols using regex commands
        message=filter(lambda twt:twt not in stopwords, message) # Filtering stopwords
        predictedcity.append(probabilityofcitygivenword(city,message))

# Write the predicted city to an output file
def output(predcity,testfile,outfile):
    with open(outfile,"w") as f:
        for i in range(len(testfile)):
            f.write(predcity[i]+' '+testfile[i])

# Calculate the accuracy of the predicted cities in testing file
def accuracy():
    match=0
    notmatch=0
    for i in range(len(predictedcity)):
        if predictedcity[i]==testfile[i].split()[0]: 
            match+=1
        else:
            notmatch+=1
        accuracypercent=(float(match)/(match+notmatch))*100
    return accuracypercent

# Print the top 5 words for each city
def topwords():
    print 'Top 5 words for each city are:'
    for city in tweetscountsincity.keys():
        top5words=sorted(bagofwords[city].items(),key=operator.itemgetter(1),reverse=True)[:5]
        top5words=[i[0] for i in top5words]
        print city+': ['+', '.join(top5words)+']'

# Input parameters
trainingfile=sys.argv[1] #'tweets.train.clean.txt'
testingfile=sys.argv[2] #'tweets.test1.clean.txt'
outputfile=sys.argv[3] #'Output.txt'

# Initialize global list and dictionaries
bagofwords={}
tweetscountsincity={}
probcitygivenword={}
predictedcity=[]

# List of stopwords. Reference: http://xpo6.com/list-of-english-stop-words/. Added few words that I found from the tweets that can be ignored.
stopwords=["","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",\
           "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", \
           "amount", "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", \
           "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", \
           "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", \
           "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", \
           "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", \
           "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", \
           "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", \
           "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", \
           "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", \
           "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", \
           "hundred", "i","ie", "if", "im","in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", \
           "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", \
           "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must",\
           "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", \
           "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", \
           "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", \
           "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", \
           "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", \
           "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", \
           "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", \
           "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", \
           "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", \
           "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", \
           "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", \
           "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", \
           "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole",\
           "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", \
           "yourself", "yourselves", "am", "pm", "th", "st", "rd", "nd"]

# Clean the training file
preprocess_trainfile(trainingfile)

# Predict testing file and store the data in an dataframe
testfile=open(testingfile,'r').readlines()
predict(testfile)

# Output the predicted values to an output file
output(predictedcity,testfile,outputfile)

# Calculating accuracy
percent=accuracy()
print 'Accuracy achieved is',round(percent,2),'%\n'

# Print top 5 words to the console
topwords()

