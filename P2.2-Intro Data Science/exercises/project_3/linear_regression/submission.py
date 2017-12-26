import numpy as np
import pandas
import statsmodels.api as sm

def linear_regression(features, values):    
    m,n = features.shape #as mxn matrix in linear algebra
    X=np.concatenate((np.ones((m,1)),features),axis=1) #need to include 1s here
    y=values
    theta = np.zeros(n+1) #np.random.random
    alpha = 0.03 #tested:2e-5
    num_iters = 2000
    theta, costs = gradient_descent(theta, X, y, alpha, num_iters)
    return theta[0], theta[1:]

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

    return theta, costs

def predictions(dataframe):
    variables = ['minpressurei','meanwindspdi','mintempi','Hour', 'fog']
    features = dataframe[variables]
    values = dataframe['ENTRIESn_hourly']

    features = add_polynomials(features, ['Hour'], 30)
    features = normalize(features)

    intercept, params = linear_regression(features, values)
    predictions = intercept + np.dot(features, params)

    return predictions

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