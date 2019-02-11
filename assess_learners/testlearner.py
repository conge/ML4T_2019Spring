""" 			  		 			     			  	   		   	  			  	
Test a learner.  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import math 			  		 			     			  	   		   	  			  	
import LinRegLearner as lrl
import DTLearner as DT
import RTLearner as RT
import BagLearner as bl
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    #if len(sys.argv) != 2:
    #    print "Usage: python testlearner.py <filename>"
    #    sys.exit(1)

    # =========== EXPERiMENT 1 ===================
    """
    Train DTLearners with varied leaf_size and calculate RMSE and Correlation to measure accuracy of the models
    for each leaf_size, repeat 15 iterations and get the mean value of the metrics. For each iteration, randomly select
    data as Training and testing set. 
    """

    # Get data from Istanbul.csv
    f = 'Data/Istanbul.csv'
    data = np.genfromtxt(f,delimiter=',')

    data = data[1:, 1:] # remove the header row and the time column
    #data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
 			  		 			     			  	   		   	  			  	
    # compute how much of the data is training and testing 			  		 			     			  	   		   	  			  	
    train_rows = int(0.6* data.shape[0]) 			  		 			     			  	   		   	  			  	
    test_rows = data.shape[0] - train_rows

    max_leaf_size = 80
    repeat_times = 15

 			  		 			     			  	   		   	  			  	
    #print testX.shape
    #print testY.shape

 	# experiment 1: Run DT with different leaf_size and calculate RMSE
    rmse_in_sample = np.zeros((repeat_times, max_leaf_size))
    corr_in_sample = []
    rmse_out_sample = []
    corr_out_sample = []
    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    for j in range(max_leaf_size):
        leaf_size = j + 1
        learner = DT.DTLearner(leaf_size, verbose = False) # create a dt learner
        learner.addEvidence(trainX, trainY) # train it
        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse_in_sample.append(math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]))
        c = np.corrcoef(predY, y=trainY)
        corr_in_sample.append(c[0,1])

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse_out_sample.append(math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]))
        c = np.corrcoef(predY, y=testY)
        corr_out_sample.append(c[0,1])

    # plot the data

    x = range(1, max_leaf_size + 1)
    plt.figure(1)
    plt.plot(x, rmse_in_sample, label="in-sample", linewidth=2.0)
    plt.plot(x, rmse_out_sample, label="out-of-sample", linewidth=2.0)
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.title("RMSE of Decision Tree Learner with different leaf size")
    plt.savefig('Exp1_fig1.png')
    plt.close()





    """# create a learner and train it 			  		 			     			  	   		   	  			  	
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner 			  		 			     			  	   		   	  			  	
    learner.addEvidence(trainX, trainY) # train it 			  		 			     			  	   		   	  			  	
    print learner.author()
    

    learner = RT.RTLearner(10, verbose = True) # create a dt learner
    learner.addEvidence(trainX, trainY) # train it
    print learner.author()
    


    learner = bl.BagLearner(learner = RT.RTLearner, kwargs = {"leaf_size":10}, bags = 10, boost = False, verbose = False)
    learner.addEvidence(trainX, trainY) # train it
    print learner.author()
 			  		 			     			  	   		   	  			  	
    # evaluate in sample 			  		 			     			  	   		   	  			  	
    predY = learner.query(trainX) # get the predictions 			  		 			     			  	   		   	  			  	
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "In sample results" 			  		 			     			  	   		   	  			  	
    print "RMSE: ", rmse 			  		 			     			  	   		   	  			  	
    c = np.corrcoef(predY, y=trainY) 			  		 			     			  	   		   	  			  	
    print "corr: ", c[0,1] 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # evaluate out of sample 			  		 			     			  	   		   	  			  	
    predY = learner.query(testX) # get the predictions 			  		 			     			  	   		   	  			  	
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]) 			  		 			     			  	   		   	  			  	
    print 			  		 			     			  	   		   	  			  	
    print "Out of sample results" 			  		 			     			  	   		   	  			  	
    print "RMSE: ", rmse 			  		 			     			  	   		   	  			  	
    c = np.corrcoef(predY, y=testY) 			  		 			     			  	   		   	  			  	
    print "corr: ", c[0,1] 	
    """
