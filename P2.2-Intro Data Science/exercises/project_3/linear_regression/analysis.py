    #initialize a random theta. vector, with n rows, 1 colum
    # forget random initialization, only for neural network theta = np.random.rand(m+1)
 #learning rate issue was due to lack of normalization

    #test
    # var_groups = combinations(variables)
    # combs = {}
    # for group in var_groups:
    #     if group: combs[group] = linear_regression(dataframe[list(group)], values)
    #return combs
    

        #variables = ['maxdewpti','maxpressurei','mindewpti','minpressurei','meandewpti','meanpressurei','meanwindspdi','mintempi','meantempi','maxtempi','precipi','thunder','fog','rain','Hour']

        #all variables reduced prediction cost of random from 3,321,525 to 2,832,550. 
    #a very small reduction

    #well... I will just test all freaking possible combinations, that is what a computer is for. and then see which is the best.

    #how many are there?
    #I can turn on or off each variable. is binary. since I have 15, my possible combinations are 2 to the 15, or 32,678. if each ones takes on average 5 seconds, I need 45 hours to test them all. 
    #that seems a lot. don't have 45 hours. alternatives?
    #I can calc the correlation of each variable (r2 score), and see which ones mean something and which ones doesn't mean anything at all
    #then, based on this, I will just take the variable that means something
    #if I cut down to 8 variables, then I can run it in 20 minutes
    #which starts being acceptable

    """
    these are the variables selected, according to:
    correlation to one another: more than 80% of correlation, just one variable it was chosen
    correlation with y: bigger than 0.01
    {'Hour': 0.17543044683295933,
     'fog': 0.011367527824781185,
     'mintempi': -0.029034361121668181, 
     'minpressurei': -0.020517187364530745,
     'meanwindspdi': 0.026626586761216906,    
    """

    #I'm down to 5 variables
    #that's 32 combinations
    #now I'm gonna run all of them 
    #since hour has a lot of correlation, and it certainly is not linear, I wanna try polinomials. maybe to the third
    #I need a new method not to mess this one even further


    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.40 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~10%) of the data contained in 
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with 
    this exercise on your own computer, locally. If you do, you may want to complete Exercise
    8 using gradient descent, or limit your number of features to 10 or so, since ordinary
    least squares can be very slow for a large number of features.
    
    If you receive a "server has encountered an error" message, that means you are 
    hitting the 30-second limit that's placed on running your program. Try using a
    smaller number of features.
    '''

    ################################ MODIFY THIS SECTION #####################################
    # Select features. You should modify this section to try different features!             #
    # We've selected rain, precipi, Hour, meantempi, and UNIT (as a dummy) to start you off. #
    # See this page for more info about dummy variables:                                     #
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html          #
    ##########################################################################################

# I will need to implement gradient descent as well, that is clear now
# why is it taking so long? where is it breaking
# oh shit - I got 131951 results - that is going to take forever
# what the hell...
# that is probably why there are optmized libraries to do it
# don't just implement the algorithm yourself, smarthead

#this is just ridiculously long.... it just increases
#i gotta fix the hell out of this
# before moving any further
# I gotta think this through and attack the logic - write it in paper
# what could possibly be wrong?
    """
    Perform linear regression given a data set with an arbitrary number of features.
    
    This can be the same code as in the lesson #3 exercise.
    
    """
    #I need gradient descent here, or some method of optimization, in order to implement linear
    #otherwise, how am I to arrive at the optimal theta?
    #let's make a try

    #how do I calc correlation??
    #it has something to do with standard deviation
    
    """
    values = dataframe['ENTRIESn_hourly']

    #let's try pearsonr
    #calc the correlation for each variable

    correlations = {}
    for variable in variables:
        correlations[variable] = pearsonr(dataframe[variable],values)[0]

    #threshold = 0.01
    #correlations = {k:v for k,v in correlations.items() if abs(v)>threshold}
    pprint(correlations)

    {'Hour': 0.17543044683295933,
     'fog': 0.011367527824781185,
     'mintempi': -0.029034361121668181, 
     'minpressurei': -0.020517187364530745,
     'meanwindspdi': 0.026626586761216906,

     'precipi': 0.009664885753838939,
         'rain': 0.0030615870211442632,
     'thunder': nan}

    #I'm removing the ones not related to value... but what about the ones related to one another? I'm gonna run the test for all. If anyone is more than 80% correlated with another, I will have to pick just one of them for the final test
    #let's first find the pairs

    sameness = 0.8
    pairs = set([])
    for var1 in variables:
        for var2 in variables:
            if abs(pearsonr(dataframe[var1], dataframe[var2])[0])>sameness and var1 != var2:
                pairs.add((var1,var2))

    pprint(pairs)

    set([('maxdewpti', 'meandewpti'),
         ('maxdewpti', 'mindewpti'),
         ('maxdewpti', 'mintempi'),
         ('meandewpti', 'maxdewpti'),
         ('meandewpti', 'mindewpti'),
         ('meandewpti', 'mintempi'),
         ('mindewpti', 'maxdewpti'),
         ('mindewpti', 'meandewpti'),
         ('mindewpti', 'mintempi'),
         ('mintempi', 'maxdewpti'),
         ('mintempi', 'meandewpti'),
         ('mintempi', 'mindewpti')])    
         'maxdewpti': -0.0098932776645542439,
         'meandewpti': -0.016197867524249145,
         'mindewpti': -0.020135113918292417,

         ('maxpressurei', 'meanpressurei'),
         ('maxpressurei', 'minpressurei'),
         ('meanpressurei', 'maxpressurei'),
         ('meanpressurei', 'minpressurei'),
         ('minpressurei', 'maxpressurei'),
         ('minpressurei', 'meanpressurei'),
         'maxpressurei': -0.017084364969893875,
         'meanpressurei': -0.016128237261487318,

         ('maxtempi', 'meantempi'),
         ('meantempi', 'maxtempi'),
         ('meantempi', 'mintempi'),
         ('mintempi', 'meantempi'),
        'maxtempi': -0.014303225741266233,
        'meantempi': -0.022796041448386175,


    """

    #I suddenly get the need for iptyhon - the need to keep state, and don't need to recalculate every time you change one line

    #I don't know what the dummy is for... so better not to use it, for now
    #dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #features = features.join(dummy_units)

        """
    #let's try my own optimization algorith
    for i in range(num_iters):
        errors = np.dot(X, theta) - y
        #calculate the cost, to monitor progression
        costs.append(int(np.sum(errors**2)/(2*m)))
        for var in range(n):
            #divide errors by the variable
            residual = errors / X[:,var]
            #them sum it up, divide by n and by m
            weighted = np.sum(residual)/(n*m)
            #apply it to theta
            theta[var] = theta[var] - alpha * weighted


    for i in range(num_iters):
        errors = np.dot(X, theta) - y
        #save the cost further checking
        cost = np.sum(errors**2)/(2*m)
        costs.append(cost)
        #calculate theta adjustment for each variable individually
        for var in range(n):
            Xvar = X[:,var]
            sumError = np.dot(errors.transpose(),Xvar) / m
            theta[var] = theta[var] - sumError*alpha
    return theta, costs

    #my vector implementation was right... but it is still not converging
    #why???
    #write it in paper

    adjustment = np.dot(X.transpose(), errors)/m 
    theta = theta - adjustment * alpha

    for v = 1:qtdVars #for all the variables     
        xV = X(:,v); #get all the values in X for one column
        errorsAdj = errors.transpose() * xV; 
        #multiply errors transpose 1x10 per all values X 10x1
        #that will give a one value
        sumError = (1/m) * sum(errorsAdj);
        errorLearned = alpha*sumError;
        theta(v) = theta(v) - alpha*sumError;
    end
    do it step-wise then check 
"""   

    """
    features is a matrix
    n rows, where each row is an observation
    m columns, where each column is a feature
    
    values is a vector
    n rows, where each row is an observation
    1 column, with the expected results
    
    procedure:
    am I going to assign a random number to each theta
    then multiply it by the features
    compare with the results
    get this difference, and apply it to the value of theta, considering the learning rate
    iterate till global optimum is found
    global optimum is found when the next iteration is equal or greater than the previous
    if the learning rate is too high, it may fail to converge
    """