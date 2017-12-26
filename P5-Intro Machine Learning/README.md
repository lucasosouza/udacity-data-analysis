### Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?  [relevant rubric items: “data exploration”, “outlier investigation”]

The goal of this project is to identify persons of interest of the Enron fraud scheme. To accomplish this goal, data was collected regarding financial data and emails exchanged for every Enron employee. Based on the available dataset, we will use a supervised learning classifier to evaluate patterns that can predict whether an employee is a person of interest or not.

To take a first look at the data, I did some exploratory data analysis (available at *eda-commented.html*). The dataset is small, with only 146 observations and 22 variables. Out of these observations, 18 are classified as Persons of Interest and 128 not. Lots of features have missing values, some as high as 95% with missing values, which as seen below, makes them unusable for the classifier.

> Percentage of missing values per feature, ordered descending
[('loan_advances', 0.95945945945945943),
 ('director_fees', 0.8716216216216216),
 ('restricted_stock_deferred', 0.86486486486486491),
 ('deferral_payments', 0.72297297297297303),
 ('deferred_income', 0.65540540540540537),
 ('long_term_incentive', 0.54054054054054057),
 ('bonus', 0.43243243243243246),
 ('to_messages', 0.40540540540540543),
 ('shared_receipt_with_poi', 0.40540540540540543),
 ('from_messages', 0.40540540540540543),
 ('from_poi_to_this_person', 0.40540540540540543),
 ('from_this_person_to_poi', 0.40540540540540543),
 ('other', 0.35810810810810811),
 ('expenses', 0.34459459459459457),
 ('salary', 0.34459459459459457),
 ('exercised_stock_options', 0.29729729729729731),
 ('restricted_stock', 0.24324324324324326),
 ('total_payments', 0.14189189189189189),
 ('total_stock_value', 0.13513513513513514),
 ('poi', 0.0),
 ('email_address', 0.0),
 ('person', 0.0)]

The significant outlier identified was a line named TOTAL, which was removed from the dataset. The outlier could be easily identified by plotting the histogram of some of the variables which had a maximum value much higher than the upper boundary of the interquartile range.

As for the features, I have found 3 groups of features by verifying the correlation between them.The 1st group contains mostly financial information, and are highly correlated between them(0.95 to 0.99), These variables are: u'bonus', u'deferral_payments', u'deferred_income', u'exercised_stock_options', u'expenses', u'long_term_incentive', u'other', u'restricted_stock', u'salary', u'total_payments', u'total_stock_value'

The 2nd group is related to messages exchanged with persons of interest. The variables in this group are also correlated with each other, but with lower scores ( between 0.2 and 0.7): u'shared_receipt_with_poi', u'from_messages', u'from_poi_to_this_person', u'from_this_person_to_poi',  u'to_messages'.

The 3rd group are variables with a high number of NAs, hence we do not have enough data to evaluate, and have weird correlation scores with other variables and POI: u'loan_advances' (142 NAs) ,  u'director_fees'(131 NAs), u'restricted_stock_deferred'(130 NAs).

### What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.  [relevant rubric items: “create new features”, “properly scale features”, “intelligently select feature”]

I have ended up using all the features from the groups 1 and 2, stated above. Apart from that, I have also created 3 new features, based on the realationship of the existing features. 

The first new feature is an attempt to check percentage of stock options the employee exercised (exercised_stock_option / total_stocks). Exercising a stock option is something an employee would do if he thought the price of the stock is getting lower in the near future.

The other 2 features are related to how much of the messages an employee sent are to the person of interest (from_this_person_to_poi/from_messages), as well as how much of the received messages are from persons of interest (from_poi_to_this_person/to_messages).

Using Kbest through grid search, I have found that the optimal number of features to feed the classifier are 16.The scores given by K-best are shown below in descending order:

> Scores from KBest, ordered descending:
Selected
[('exercised_stock_options', 24.815079733218194),
 ('total_stock_value', 24.182898678566879),
 ('bonus', 20.792252047181535),
 ('salary', 18.289684043404513),
 ('percentage_messages_to_poi', 16.409712548035792),
 ('deferred_income', 11.458476579280369),
 ('long_term_incentive', 9.9221860131898225),
 ('restricted_stock', 9.2128106219771002),
 ('total_payments', 8.7727777300916756),
 ('shared_receipt_with_poi', 8.589420731682381),
 ('expenses', 6.0941733106389453),
 ('from_poi_to_this_person', 5.2434497133749582),
 ('other', 4.1874775069953749),
 ('percentage_messages_from_poi', 3.1280917481567192),
 ('from_this_person_to_poi', 2.3826121082276739),
 ('to_messages', 1.6463411294420076)
Not selected
 ('deferral_payments', 0.22461127473600989),
 ('from_messages', 0.16970094762175533),
 ('exercised_stocks_percentage', 0.04211676849806735)]

Not all the features, though, were relevant in the decision tree analysis (see *tree.pdf*), and the feature importance given by the decision tree differ significantly from the features scores given by k-best. The features evaluated by the decision tree are given below: 

> Features importance from decision tree, ordered descending:
[('expenses', 0.35143111634978136),
 ('other', 0.20199092286204867),
 ('shared_receipt_with_poi', 0.12740670766674253),
 ('from_poi_to_this_person', 0.074731079542461901),
 ('total_payments', 0.020507436869729046)] 

### What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  [relevant rubric item: “pick an algorithm”]

I've tried many approaches. I've opted to try a combination of different preprocessing techniques (such as standardization and scaling to normalize features, and principal component analysis and feature selection to reduce the number of features) with different classifiers. I'm aware that for some classifiers, such as decision trees, normalizing features are not needed. Nevertheless, being a small dataset, my approach was to try all combinations and verify which brought the best result. 

This was done in an object oriented approach to facilitate code reusability. In the conceived model, there are learning agents, that can learn given a dataset, specific techniques (preprocessing steps and classifier) and a grid of parameters to search for each technique. Above that there is a learning coach, which plans several strategies and recruits a learning agent to implement each of these strategies. The coach chooses the best agent by evaluating their score function. The model is available at *agent.py*. (std stans for standard scaler, as opposed to minmaxscaler)

> F1-score and running times
std-naive_bayes: 0.24 f1-score, 0.25 scs
std-kbest-decision_tree: 0.37 f1-score, 33.59 scs
std-decision_tree: 0.36 f1-score, 4.15 scs
kbest-adaboost: 0.30 f1-score, 71.45 scs
std-kbest-naive_bayes: 0.35 f1-score, 0.96 scs
decision_tree: 0.36 f1-score, 3.61 scs
std-kbest-adaboost: 0.29 f1-score, 71.96 scs
naive_bayes: 0.24 f1-score, 0.14 scs
kbest-decision_tree: 0.37 f1-score, 29.01 scs
kbest-naive_bayes: 0.35 f1-score, 0.87 scs
std-adaboost: 0.29 f1-score, 10.36 scs
adaboost: 0.29 f1-score, 12.63 scs

The best results were achieved selecting 16 most important features, using SelectKBest, and a decision tree with fine-tuned parameters found through grid search.

>  Selected Algorithm
Pipeline(steps=[('f_selector', SelectKBest(k=16, score_func=<function f_classif at 0x104de3de8>)), ('classifier', DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
            max_features=None, max_leaf_nodes=None, min_samples_leaf=2,
            min_samples_split=6, min_weight_fraction_leaf=0.0,
            random_state=None, splitter='best'))])


### What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).  [relevant rubric item: “tune the algorithm”]

Tuning the parameters means choosing the best set of parameters for the classification algorithm (or a preprocessing step). The parameters of each classifier will vary. For example, for decision trees you can set the minimum number of leaf nodes or the maximum depth of the tree, amongst others, while on ensemble methods such as adaboost and random forest you can choose the number of classifiers and the learning rate applied. 

The results may vary a lot according to the parameters you selected. Different types of problems will respond better to different sets of parameters. For example, going to deep on a decision tree may overfit an algorithm, specially when you have a low number of observations. Setting a learning rate too low may take a long time to converge to optimal solution, while a learning rate too high may diverge.

I've chosen to use grid search, available in scikit, to tune the parameters.  For each preprocessing step or classifier I've defined, in the strategy, the set of parameters that would be tuned through grid search. In the Decision Tree classifier, I've tuned the parameters of criterion (either uses gini or entropy to evaluate information gain), maximum number of features (applies transformation to features such as sqrt and log2), minimum samples split, minimum samples leaf and maximum leaf nodes.

Below are the results from the selected algorithm, decision tree with selectKbest as the feature selection strategy, and using standard scaler (removes the mean and scales to unit variance) to normalize the parameters. The variables tested are min_samples_leaf, min_samples_split and criterion, from the classifier, and k (as in k parameters) from the feature selector. There are 210 variations, I've filtered only the top 15 to facilitate reading.

[f1_score: 0.48429, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 3, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.47024, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 2, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.46667, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 3, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.45095, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 4, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.44667, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 2, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.43762, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 6, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.43440, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 4, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.42500, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 8, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.42024, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 2, 'f_selector__k': 12, 'classifier__criterion': 'gini'},
 f1_score: 0.41429, params: {'classifier__min_samples_leaf': 1, 'classifier__min_samples_split': 8, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.39429, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 6, 'f_selector__k': 12, 'classifier__criterion': 'gini'},
 f1_score: 0.39357, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 6, 'f_selector__k': 'all', 'classifier__criterion': 'gini'},
 f1_score: 0.39262, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 8, 'f_selector__k': 2, 'classifier__criterion': 'gini'},
 f1_score: 0.38714, params: {'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 2, 'f_selector__k': 12, 'classifier__criterion': 'gini'},
 f1_score: 0.38500, params: {'classifier__min_samples_leaf': 4, 'classifier__min_samples_split': 3, 'f_selector__k': 'all', 'classifier__criterion': 'gini'}]

### What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  [relevant rubric item: “validation strategy”]

Validation is the process of evaluating you algorithm against a test set. Validation is required in order to know the actual performance of the algorithm on a real scenario dataset, as opposed to performance on the training set. 

The classic mistake of not validating your model on a separated dataset, or by using a k-fold cross validation, is to overfit your classifier. If the classifier is overfit for the training data, it will not perform well on other datasets.

There are several strategies to validate your dataset. In the KFold strategy, you divide the dataset into k folds, and use k-1 folds to train your data. A variation from that is the Stratified kFold, in which the dataset is divided into k folds, but assuring that each folds holds the same distribution of classes of the dataset. 

The ShuffleSplit is similar to KFold, with the difference that the dataset is shuffled before the split. The Stratified Shuffle Split is a variation of the above, a randomly split of the dataset into folds that assures all folds have the same distribution of classes as in the complete dataset.

Given the small number of observations and the very skewed distribution, I've chose to use the Stratified Shuffle Split in the GridSearchCV. If I have used a simple KFold, I could have ended up with a test fold with 0 observations of persons of interest that would affect the evaluation of the algorithm. 

### Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]

For scoring I've opted to use the f1 scoring function, which gives equal importance to recall and precision, the two scores I've aimed at maximizing.

> Results from the selected algorithm>
	Accuracy: 0.84447	Precision: 0.40683	Recall: 0.36350	F1: 0.38395	F2: 0.37141
	Total predictions: 15000	True positives:  727	False positives: 1060	False negatives: 1273	True negatives: 11940

A recall of 0.36350 means that the algorithm can predict every 3 or 4 out of 10 persons of interest in a dataset. Recall is a very important metric, also called sensitivity in some fields (such as pharma, in which specificity is also a important metric). A precision of 0.40683 means that 41% of the predicted POIs will actually be a POI.



