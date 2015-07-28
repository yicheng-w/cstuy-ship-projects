#!/usr/bin/python

from sklearn import svm
from sklearn.externals import joblib
import os
from sys import argv

try:
    movieReviewer = joblib.load("./SVM/movieReviewer%s.svm" % argv[1])
except:
    print "Please train with SVMTrain.py first!"

wordList = []

def asciify(text):
    return "".join([i for i in list(text) if isAlphanumeric(i)])

def isAlphanumeric(char):
    order = ord(char)
    return (order >= 48 and order <= 57) or (order >= 65 and order <= 90) or (order >= 97 and order <= 122) or order == 9 or order == 32


os.system("echo -n 'loading keywords...\t\t'")
# argv = command line arguments, argv[1] = type of training to be done
# Possible arguments: -POS: part of speech, -U: unigrams, -A: adjectives
if argv[1] == '-POS':
    POSList = open('PosKeywords.txt', 'r').read().split("\n")
    for i in POSList:
        wordList.append("".join(i.split()[:-1]))

elif argv[1] == '-U':
    wordList = open("SVM/PosKeywords.txt", 'r').read().split()
    wordList += open("SVM/NegKeywords.txt", 'r').read().split()

elif argv[1] == 'A':
    AdjList = open('Adjectives.txt', 'r').read().split("\n")
    for i in AdjList:
        wordList.append("".join(i.split()[:-1]))
# this is so that it only takes in 1000 keywords.

os.system("echo -n '[done]\n'")

def intersection(keywords, text):
    resultVec = []
    textSet = set(text)
    for i in keywords:
        if i in textSet:
            resultVec.append(1)
        else:
            resultVec.append(0)
    return resultVec

if __name__ == '__main__':
    review = asciify(open(raw_input("Please enter the review location: "), 'r').read()).split()
    X = intersection(wordList, review)
    result = movieReviewer.predict(X)[0]

    if (result > 0):
        print "Good movie!"
        #print result
    else:
        print "BAD movie!"
        #print result
