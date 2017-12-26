#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#########################################################
### your code goes here ###
from sklearn import tree
from sklearn import metrics
import numpy as np
#########################################################

print np.shape(features_train)

def classify(clf, features_train, labels_train):
	t = time()
	clf.fit(features_train, labels_train)
	print "Training took {} scs".format(time() - t)
	return clf

def predict(clf, features_test):
	t = time()
	prediction = clf.predict(features_test)
	print "Prediction took {} scs".format(time() - t)
	return prediction

def score(ytrue, ypred):
	t = time()
	acc = metrics.accuracy_score(ytrue, ypred)
	print "Scoring took {} scs".format(time() - t)
	print "Accuracy is {}".format(acc)
	return acc

def cycle(min_samples_split):
	clf = tree.DecisionTreeClassifier(min_samples_split=min_samples_split)
	clf = classify(clf, features_train, labels_train)
	prediction = predict(clf, features_test)
	score(labels_test, prediction)
	return clf, prediction	

def tune(parameters):
	for pmt in parameters:
		print "Parameter is {}".format(pmt)
		cycle(pmt)


tune([40])
#clf, prediction = cycle()
#prettyPicture(clf, features_test, labels_test)
#output_image("test.png", "png", open("test.png", "rb").read())

