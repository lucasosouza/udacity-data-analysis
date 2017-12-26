#!/usr/bin/python
import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from tester import test_classifier
from agent import *

import pandas as pd
import numpy
import warnings
from pprint import pprint

with open("final_project_dataset.pkl", "r") as data_file:
  data_dict = pickle.load(data_file)

### Task 1: Select what features you'll use.
features = ['bonus', 'deferral_payments', 'deferred_income','exercised_stock_options', 
            'expenses', 'long_term_incentive', 'other', 'restricted_stock', 'salary', 
            'total_payments', 'total_stock_value', 'shared_receipt_with_poi', 'from_messages', 
            'from_poi_to_this_person', 'from_this_person_to_poi',  'to_messages']

### Task 2: Remove outliers
#complete analysis at eda-commented
del data_dict['TOTAL']  
del data_dict['THE TRAVEL AGENCY IN THE PARK']

### Task 3: Create new feature(s)

#convert to panda and force numeric
df = pd.DataFrame(data_dict.values())
df = df.convert_objects(convert_numeric=True)

#add new features
features.extend(['exercised_stocks_percentage', 'percentage_messages_from_poi', 'percentage_messages_to_poi'])
df['exercised_stocks_percentage'] = df.exercised_stock_options / df.total_stock_value
df['percentage_messages_from_poi'] = df.from_poi_to_this_person / df.to_messages
df['percentage_messages_to_poi'] = df.from_this_person_to_poi / df.from_messages 

#remove Nan-values
for feature in features:
	df.loc[df[feature].isnull(), feature] = 0

#convert back to dict
transformed_features = df.to_dict('index')
new_data_dict = dict(zip(data_dict.keys(), transformed_features.values())) 
   
#proceed with defaulted data wrangling
data = featureFormat(new_data_dict, ['poi'] + features, sort_keys = True)
y, X = targetFeatureSplit(data)

### Task 4: Try a variety of classifiers

coach = LearnCoach(X,y)
coach.selectors['kbest'] = ('feature_selection.SelectKBest', {'k': [1,2,4,8,12,16,'all']})
coach.classifiers['naive_bayes'] = ('naive_bayes.GaussianNB', {})
coach.classifiers['decision_tree'] = ('tree.DecisionTreeClassifier', {
 		'criterion': ['gini', 'entropy'],
 		'min_samples_split': [2,3,4,6,8],
 		'min_samples_leaf': [1,2,4]
 	})
coach.classifiers['adaboost'] = ('ensemble.AdaBoostClassifier', {
 		'n_estimators': [150],
 		'learning_rate': [0.01, 0.1, 0.3, 1]
 	})
coach.scalers['std'] = ('StandardScaler', {})
coach.compose_strategies()

with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	agent = coach.select_best_agent()

agent.print_best_result()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
# parameters already tuned through grid search
# will replicate the results without pipeline in order to get scores from selectKBest and features importance from the decision tree, as well as the tree graph

# feature selection
from sklearn.feature_selection import SelectKBest
fsel = SelectKBest(k=16)
X_new = fsel.fit_transform(X, y)
print("Scores from KBest, ordered descending:")
pprint(sorted(zip(features,fsel.scores_), key=lambda x:-x[1]))

## classifier
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(min_samples_leaf=2, min_samples_split=6, criterion='entropy')
clf.fit(X,y)
print("Features importance from decision tree, ordered descending:")
pprint(sorted(zip(features[:16],clf.feature_importances_), key=lambda x:-x[1]))

#export tree
from sklearn.externals.six import StringIO  
import pydot 
dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data, feature_names=features) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("tree.pdf") 

### Task 6: Dump your classifier, dataset, and features_list so anyone can check your results. 
dump_classifier_and_data(agent.export(), new_data_dict, ['poi'] + features)
test_classifier(agent.export(), new_data_dict, ['poi'] + features)

