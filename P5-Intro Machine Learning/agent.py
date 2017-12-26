import sys
import pickle
sys.path.append("../tools/")
from sklearn import *
from time import time
import numpy as np
from copy import deepcopy
from pprint import pprint

from feature_format import featureFormat, targetFeatureSplit

class LearnAgent():

	def __init__(self, X, y, grid_params, classifier='ensemble.RandomForestClassifier', f_selector=None, scaler=None, cross_validator='StratifiedShuffleSplit', scoring_function='f1', filter_outliers=False):
		
		self.classifier = eval(classifier)()
		self.scaler = getattr(preprocessing, scaler)() if scaler else scaler
		self.f_selector = eval(f_selector)() if f_selector else f_selector
		self.cross_validator = getattr(cross_validation, cross_validator)
		self.scoring_function = scoring_function
		self.grid_params = grid_params
		self.filter_outliers = filter_outliers
		self.X = X
		self.y = y

	def gen_cross_validator(self):
		try:
			self.cross_validator = self.cross_validator(self.y, n_iter=100, random_state = 42)
		except: pass

	def gen_pipeline(self):
		pipe = [('classifier', self.classifier)]
		if self.f_selector: pipe.insert(0, ('f_selector', self.f_selector))
		if self.scaler: pipe.insert(0, ('scaler', self.scaler))
		self.pipeline = pipeline.Pipeline(pipe)

	def export(self):
		return self.pipeline.set_params(**self.grid.best_params_)

	def gen_grid(self):
		self.grid = grid_search.GridSearchCV(self.pipeline, self.grid_params, n_jobs=-1, scoring=self.scoring_function, cv=self.cross_validator)

	def print_best_result(self):
		print "Estimator: {}".format(self.grid.best_estimator_)
		print "Best params are {}".format(self.grid.best_params_)
		print "{} score is {}".format(self.scoring_function, self.grid.best_score_)

	def print_metrics(self):
		X_train, X_test,  y_train, y_test = cross_validation.train_test_split(self.X, self.y, test_size=.3)
		print metrics.classification_report(y_test, self.grid.predict(X_test))
		print metrics.confusion_matrix(y_test, self.grid.predict(X_test))

	def fit(self):
		t0 = time()
		self.grid.fit(self.X, self.y)

	def learn(self):
		self.gen_cross_validator()
		self.gen_pipeline()
		self.gen_grid()
		self.fit()
		return self.grid.best_score_

class LearnCoach:

	def __init__(self, X, y):
		self.selectors = {}
		self.classifiers = {}
		self.scalers={}
		self.validators={}
		self.agents = {}
		self.scores = {}
		self.run_time = {}
		self.X = np.array(X) if type(X) == list else X
		self.y = np.array(y) if type(y) == list else y

	def recruit_agent(self, classifier, selector=None, scaler=None, name=None):
		agent_name = ''
		agent_params = {}
		grid_params = {}
		if scaler:
			agent_name += (scaler[0] + '-')
			agent_params['scaler'] = scaler[1][0]
			for k,v in scaler[1][1].items():
				grid_params['scaler__' + k] = v
		if selector:
			agent_name += (selector[0] + '-')
			agent_params['f_selector'] = selector[1][0]
			for k,v in selector[1][1].items():
				grid_params['f_selector__' + k] = v
		if classifier:
			agent_name += classifier[0]
			agent_params['classifier'] = classifier[1][0]
			for k,v in classifier[1][1].items():
				grid_params['classifier__' + k] = v
		agent_params['grid_params'] = grid_params
		agent_params['X'] = self.X
		agent_params['y'] = self.y
		if name: agent_name=name
		self.agents[agent_name] = LearnAgent(**agent_params)

	def compose_strategies(self):
		for classifier in self.classifiers.items():
			self.recruit_agent(classifier)
			for selector in self.selectors.items():
				self.recruit_agent(classifier, selector=selector)
				for scaler in self.scalers.items():
					self.recruit_agent(classifier, selector=selector, scaler=scaler)
			for scaler in self.scalers.items():
				self.recruit_agent(classifier, scaler=scaler)
		return self.agents

	def clear_strategies(self):
		self.agents = {}

	def add_strategy(self, classifier, scaler=None, selector=None, name=None):
		if (selector and scaler):
			self.recruit_agent((classifier, self.classifiers[classifier]), selector=(selector, self.selectors[selector]), scaler=(scaler, self.scalers[scaler]), name=name)
		elif selector:
			self.recruit_agent((classifier, self.classifiers[classifier]), selector=(selector, self.selectors[selector]), name=name)
		elif scaler:
			self.recruit_agent((classifier, self.classifiers[classifier]), scaler=(scaler, self.scalers[scaler]), name=name)
		else:
			self.recruit_agent((classifier, self.classifiers[classifier]), name=name)

	def train(self):
		for name, agent in self.agents.items():
			t0 = time()
			self.scores[name] = agent.learn()
			self.run_time[name] = time() - t0
			print '{}: {:.2f} f1-score, {:.2f} scs'.format(name, self.scores[name], self.run_time[name])
		self.scores = sorted(self.scores.items(), key=lambda x:-x[1])
		print(self.scores)

	def select_best_agent(self):
		self.train()
		return self.agents[self.scores[0][0]]






