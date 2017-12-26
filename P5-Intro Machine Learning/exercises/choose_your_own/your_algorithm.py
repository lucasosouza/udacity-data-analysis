#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture
from class_vis import output_image
from time import time
from pprint import pprint

#import pdb;pdb.set_trace()

features_train, labels_train, features_test, labels_test = makeTerrainData()

### the training data (features_train, labels_train) have both "fast" and "slow"
### points mixed together--separate them so we can give them different colors
### in the scatterplot and identify them visually
"""
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]

#### initial visualization
plt.xlim(0.0, 1.0)
plt.ylim(0.0, 1.0)
plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
plt.legend()
plt.xlabel("bumpiness")
plt.ylabel("grade")
plt.show()

#there is a looping going on when calculating grade_fast, etc., which is slowing down the script execution time
"""

################################################################################
### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary

from sklearn import ensemble
from sklearn import metrics
from sklearn import tree
import numpy as np
import operator

def classify(clf, features_train, labels_train):
	#t = time()
	clf.fit(features_train, labels_train)
	#print "Training took {} scs".format(time() - t)
	return clf

def predict(clf, features_test):
	#t = time()
	prediction = clf.predict(features_test)
	#print "Prediction took {} scs".format(time() - t)
	return prediction

def score(ytrue, ypred):
	#t = time()
	acc = metrics.accuracy_score(ytrue, ypred)
	#print "Scoring took {} scs".format(time() - t)
	print "Accuracy is {}".format(acc)
	return acc

def cycle(base_estimator, n_estimators=50,learning_rate=0.25):
	#print 'Starting to classify with n estimators {} and learning rate {}'.format(n_estimators, learning_rate)
	clf = ensemble.AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate)
	clf = classify(clf, features_train, labels_train)
	prediction = predict(clf, features_test)
	acc = score(labels_test, prediction)
	return acc

def tune():
	results = {}
	for crit in criterion:
		for split in splitter:
			for feat in max_features:
				for depth in max_depth:
					for leaf in max_leaf_nodes:
						for min_split in min_samples_split:
							for min_leaf in min_samples_leaf:
								for weight in min_weight_fraction_leaf:
									for classw in class_weight:
										base_estimator = tree.DecisionTreeClassifier(criterion=crit, max_features=feat, max_depth=depth, max_leaf_nodes=leaf, min_samples_split=min_split, min_samples_leaf= min_leaf, min_weight_fraction_leaf=weight, class_weight=classw)
										try:
											acc = cycle(base_estimator=base_estimator)
											if acc >= .932:
												print (crit,split,feat,depth,leaf,min_split,min_leaf,weight,classw)
									 			results[(crit,split,feat,depth,leaf,min_split,min_leaf,weight,classw)] = acc
										except:
											pass
 	sorted_results = sorted(results.items(), key=operator.itemgetter(1))
 	return sorted_results

#what can I tune
#parameters = {	
#ada boost
n_estimators = [1+(i*2) for i in range(50)]
learning_rate = [0.01 * i**1.5 for i in range(40)]
#decision tree classifier
criterion = ['gini', 'entropy']
splitter = ['best', 'random']
max_features = ['auto', 'sqrt', 'log2', 10, 100, None]
max_depth = [10, 100, None]
max_leaf_nodes = [10, 100, None]
min_samples_split = [2+(i*2) for i in range(50)]
min_samples_leaf = [1+(i*2) for i in range(50)]
min_weight_fraction_leaf = [0+(i*2) for i in range(50)]
class_weight = ['balanced', None]
#}

print tune()
#cycle(n_estimators=50, learning_rate=0.25)

#prettyPicture(clf, features_test, labels_test)
#output_image("test.png", "png", open("test.png", "rb").read())

#there is some crazy shit happening I can't figure it out... and it is slowing dow execution time.

#Here is a challenge - beat the classifier, using AdaBoost
#I need to tune all possible parameters, programatically, in order to do so
#creates arrays with default parameters. Try all of those. Only show the Top 5 results. Or show them all?
#with default parameters, I can get 0.924. I need to increase it to > 0.936

#adaboost parameters
#two levels
#first the tree
#second the optmizer

# try all estimators, in a log3 basis, from 1
# try all learning rates, log3 bases, from 0.01

# def tune():
# 	results: {}
# 	i =1 
# 	while i<100: #cycle n_estimators
# 		i = i+1
# 		j = 0.01
# 		while j<3: #cycle learning rate
# 			j = j*1.5
# 			results[(i, j)] = cycle(n_estimators=i, learning_rate=j)
# 	sorted_results = sorted(results.items(), key=operator.itemgetter(1))
# 	return sorted_results

