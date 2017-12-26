#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""
    
import sys
import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#########################################################
### your code goes here ###
from sklearn.naive_bayes import GaussianNB
import numpy

classifier = GaussianNB() #gaussian naive bayes classifier

def classify():
	classifier.fit(features_train, labels_train) #X and y

def predict():
	predictions = classifier.predict(features_test)
	return predictions

def evaluate(predictions):
	accuracy = sum(predictions == labels_test) / float(len(predictions))
	print "Accuracy is {}".format(accuracy)

#########################################################

t0 = time.time()
classify()
t1 = time.time()
print "Classify - Time elapsed: {} secs".format(t1-t0)

t0 = time.time()
predictions = predict()
t1 = time.time()
print "Predict - Time elapsed: {} secs".format(t1-t0)

t0 = time.time()
evaluate(predictions)
t1 = time.time()
print "Evaluate - Time elapsed: {} secs".format(t1-t0)

#########################################################

#will the methods have acess to the variables, even though they were defined outside of the scope and not defined as globals?
#yes, they do. how? not sure
#there is some abstraction and black-boxing going on in this code. makes it simpler to switch algorithms, if required
#which is what we are going to do at the next stage, that is, trying support vector machines
#how is this useful? or state of the art?
#not just running the algorithms is the thing
#the actual thing is selecting the data, wrangling the data, making the necessary modifications to it
#that comes first. second is selecting the best parameters for the model, to avoid overfit or underfit
#third is knowing how to run it in distributed systems, and leverage all the memory and computational power you have access to
#actually what comes between 1st and 2nd is selecting the right algorithm




