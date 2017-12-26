import numpy as np
import pandas
import statsmodels.api as sm
import pdb, traceback, sys
from pprint import pprint
import time
from scipy.stats.stats import pearsonr   
import itertools
from sklearn import linear_model

def linear_regression(features, values):    
    m,n = features.shape #as mxn matrix in linear algebra
    #X=np.concatenate((np.ones((m,1)),features),axis=1) #need to include 1s here
    X=features
    y=values
    theta = np.zeros(n+1) #np.random.random
    alpha = 0.1 #tested:2e-5
    num_iters = 50
    #theta, costs = gradient_descent(theta, X, y, alpha, num_iters)
    clf = linear_model.LinearRegression() #much faster than manual, same r2
    clf.fit(X,y)
    # sklearn.linear_model.SGDRegressor(loss='squared_loss', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, n_iter=5, shuffle=True, verbose=0, epsilon=0.1, random_state=None, learning_rate='invscaling', eta0=0.01, power_t=0.25, warm_start=False, average=False)
    import pdb;pdb.set_trace()
    return clf.intercept_, clf.coef_
    #return theta[0], theta[1]
    #I've got a much lower R2 using this SGD regressor 
    #let's try another one

def gradient_descent(theta, X, y, alpha, num_iters=50):
    costs = []
    m,n = X.shape
    for i in range(num_iters):
        errors = np.dot(X, theta) - y
        costs.append(int(np.sum(errors**2)/(2*m)))
        gradient = np.sum(X[:,1:] * errors[:,np.newaxis], axis=0)/m
        gradientZero = np.sum(errors)/m
        theta[1:] = theta[1:] - (alpha * gradient)
        theta[:1] = theta[:1] - (alpha * gradientZero)

    print costs[0]-costs[-1]
    return theta, costs

def predictions(dataframe):
    variables = ['minpressurei','meanwindspdi','mintempi','fog']

    features = dataframe[variables]
    values = dataframe['ENTRIESn_hourly']

    #add dummy_units for UNIT
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)

    #add dummy_units for HOUR
    dummy_units = pandas.get_dummies(dataframe['Hour'], prefix='hour')
    features = features.join(dummy_units)

    features = normalize(features)

    intercept, params = linear_regression(features, values)
    predictions = intercept + np.dot(features, params)

    return predictions

def r2(predictions, values):
    ssres = np.sum((values-predictions)**2)
    sstot = np.sum((values-values.mean())**2)
    return 1- ssres/sstot

def add_polynomials(dataframe, variables, num_pol):
    for variable in variables:
        for i in range(1,num_pol+1):
            dataframe.loc[:,variable + str(i)] = dataframe[variable] ** i
    return dataframe

def normalize(dataframe):
    columns = dataframe.columns.tolist()
    for column in columns:
        mean = dataframe[column].mean()
        std = dataframe[column].std()
        dataframe.loc[:,column] = (dataframe[column] - mean)/std
    return dataframe

if __name__=="__main__":
    try:
        dataframe = pandas.read_csv("turnstile_data_master_with_weather.csv")
        print r2(predictions(dataframe),dataframe['ENTRIESn_hourly'])
        #print "elapsed time: {}".format(time.time()-t0)
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        #print
        pdb.post_mortem(tb)

#r2 - how much of the variance can be explained

# def combinations(x):
#     return [c for i in range(len(x)+1) for c in itertools.combinations(x,i)]

# def predict(dataframe):
#     variables = ['minpressurei','meanwindspdi','mintempi','Hour', 'fog']
#     features = dataframe[variables]
#     values = dataframe['ENTRIESn_hourly']
 
#     dataframe = add_polynomials(features, ['Hour'], 50)
#     dataframe = normalize(features)

#     return linear_regression(dataframe, values)
    

#correlated one variable with anoter
#correlated all of them (pearson correlation with y)
#to figure out the best
#then I added polynomials on the variable that had the highest correlation
#that improved the model a lot
#I've done a lot regarding features selection
#not so much to pick the optimal learning rate, or gradient descent number of iterationts
#I guess gradient descent is easy - just loop until it converges
#learning rate I should at least try a few, once I get the optimal set of variables
#there is also lambda. but I'm not regularizing here
#regularization is what would keep me from overfitting, and probably from diverging
#I skipped that step, what may be the cause for my troubles
#I also had to normalize, since variables had different values
#after normalizing I could use learning rates around 1-10%, without diverging

#finally, I tried Udacity solution to add a dummy unit
#although I don't really know what it means yet
#what I do now is that is taking a lot longer
#but it gets a ridiculous high r2. what the fuck does that mean???

#on gradient descent - should also be aware of local minimuns
#I can run n times, and pick the optimal - that would help ensure it is not going for a local minimum
#but that depends on the initial values
#so I would have to pick them randomly, otherwise there would be no difference



