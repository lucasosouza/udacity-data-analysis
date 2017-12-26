#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
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
from sklearn import svm
from time import time
from sklearn import metrics

#reduce training set
# reduced = len(features_train)/100
# features_train = features_train[:reduced]
# labels_train = labels_train[:reduced]

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

def cycle(C):
	clf = svm.SVC(kernel='rbf', C=C)
	clf = classify(clf, features_train, labels_train)
	prediction = predict(clf, features_test)
	score(labels_test, prediction)
	return prediction	

def tuneC():
	C = 0.01
	for i in range(10):
		print "C is {}".format(C)
		cycle(C)
		C = C*10

pred = cycle(10000)
print "Chris emails: {}".format(len(pred[pred==1]))
print "Sara emails: {}".format(len(pred[pred==0]))

#chris is 1, sara is 0

#GridCV - tune the parametes

#reduced training set to test for different parameters and optmize
#but is there a rule of thumb to determine the best parameter?
#or should we always test it for each dataset?
#what is the logic, the rationality, the mathematics behind it?
#do we not know, or do we simply abstract out of it to make it simpler?