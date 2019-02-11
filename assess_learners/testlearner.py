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
import time
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
    for each leaf_size. 
    """

    # Get data from Istanbul.csv
    f = 'Data/Istanbul.csv'
    data = np.genfromtxt(f,delimiter=',')

    data = data[1:, 1:] # remove the header row and the time column
    #data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
 	"""		  		 			     			  	   		   	  			  	
    # compute how much of the data is training and testing 			  		 			     			  	   		   	  			  	
    train_rows = int(0.6* data.shape[0]) 			  		 			     			  	   		   	  			  	
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    max_leaf_size = 80
    #repeat_times = 15

 			  		 			     			  	   		   	  			  	
    #print testX.shape
    #print testY.shape

 	# experiment 1: Run DT with different leaf_size and calculate RMSE
    rmse_in_sample = []
    corr_in_sample = []
    rmse_out_sample = []
    corr_out_sample = []


    for i in range(max_leaf_size):
        leaf_size = i + 1
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
    plt.ylabel("Root Mean Squared Errors")
    plt.legend(loc="lower right")
    plt.title("RMSE of Decision Tree Learner with different leaf size")
    plt.savefig('Exp1_fig1.png')
    plt.close()

    # Overfitting happens when in sample error is smaller than the out of sample error
    # when in-sample error is higher than out-of-sample error, it is not overfitting.
    # in figure 1, smaller leaf sizes are more likely to overfit
    # Find and print the index of the first leaf_size that does not overfit
    print "Experiment 1: DT stopped overfit when leaf size is larger than ", np.argmin(rmse_out_sample ) + 1


    # =========== EXPERiMENT 2 ===================
    """
    Using BagLearner with DTLearners with varied leaf_size and calculate RMSE and Correlation to measure accuracy of the models
    for each leaf_size. 
    """
    gtid = 902265013
    np.random.seed(gtid)

    bags = 20
    rmse_in_sample = []
    corr_in_sample = []
    rmse_out_sample = []
    corr_out_sample = []


    for i in range(max_leaf_size):
        leaf_size = i + 1
        # learner = DT.DTLearner(leaf_size, verbose = False) # create a dt learner
        learner = bl.BagLearner(learner = DT.DTLearner, kwargs = {"leaf_size":leaf_size}, bags = bags, boost = False, verbose = False)
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

    #x = range(1, max_leaf_size + 1)
    plt.figure(2)
    plt.plot(x, rmse_in_sample, label="in-sample", linewidth=2.0)
    plt.plot(x, rmse_out_sample, label="out-of-sample", linewidth=2.0)
    plt.xlabel("Leaf Size")
    plt.ylabel("Root Mean Squared Errors")
    plt.legend(loc="lower right")
    plt.title("RMSE of Bagging with Decision Tree Learner with different leaf size\n(20 bags)")
    plt.savefig('Exp2_fig2.png')
    plt.close()

    # Overfitting happens when in sample error is smaller than the out of sample error
    # when in-sample error is higher than out-of-sample error, it is not overfitting.
    # in figure 1, smaller leaf sizes are more likely to overfit
    # Find and print the index of the first leaf_size that does not overfit
    print "EXP2: DT with bagging stopped overfit when leaf size is larger than ", np.argmin(rmse_out_sample ) + 1


    bags = 10
    rmse_in_sample = []
    corr_in_sample = []
    rmse_out_sample = []
    corr_out_sample = []


    for i in range(max_leaf_size):
        leaf_size = i + 1
        # learner = DT.DTLearner(leaf_size, verbose = False) # create a dt learner
        learner = bl.BagLearner(learner = DT.DTLearner, kwargs = {"leaf_size":leaf_size}, bags = bags, boost = False, verbose = False)
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

    #x = range(1, max_leaf_size + 1)
    plt.figure(3)
    plt.plot(x, rmse_in_sample, label="in-sample", linewidth=2.0)
    plt.plot(x, rmse_out_sample, label="out-of-sample", linewidth=2.0)
    plt.xlabel("Leaf Size")
    plt.ylabel("Root Mean Squared Errors")
    plt.legend(loc="lower right")
    plt.title("RMSE of Bagging with Decision Tree Learner with different leaf size\n(10 bags)")
    plt.savefig('Exp2_fig3a.png')
    plt.close()

    # Overfitting happens when in sample error is smaller than the out of sample error
    # when in-sample error is higher than out-of-sample error, it is not overfitting.
    # in figure 1, smaller leaf sizes are more likely to overfit
    # Find and print the index of the first leaf_size that does not overfit
    print "EXP2-3a: DT with bagging stopped overfit when leaf size is larger than ", np.argmin(rmse_out_sample ) + 1

    bags = 100
    rmse_in_sample = []
    corr_in_sample = []
    rmse_out_sample = []
    corr_out_sample = []


    for i in range(max_leaf_size):
        leaf_size = i + 1
        # learner = DT.DTLearner(leaf_size, verbose = False) # create a dt learner
        learner = bl.BagLearner(learner = DT.DTLearner, kwargs = {"leaf_size":leaf_size}, bags = bags, boost = False, verbose = False)
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

    #x = range(1, max_leaf_size + 1)
    plt.figure(4)
    plt.plot(x, rmse_in_sample, label="in-sample", linewidth=2.0)
    plt.plot(x, rmse_out_sample, label="out-of-sample", linewidth=2.0)
    plt.xlabel("Leaf Size")
    plt.ylabel("Root Mean Squared Errors")
    plt.legend(loc="lower right")
    plt.title("RMSE of Bagging with Decision Tree Learner with different leaf size\n(100 bags)")
    plt.savefig('Exp2_fig3b.png')
    plt.close()

    # Overfitting happens when in sample error is smaller than the out of sample error
    # when in-sample error is higher than out-of-sample error, it is not overfitting.
    # in figure 1, smaller leaf sizes are more likely to overfit
    # Find and print the index of the first leaf_size that does not overfit
    print "EXP2-3b: DT with bagging stopped overfit when leaf size is larger than ", np.argmin(rmse_out_sample ) + 1
    """

    # =========== EXPERiMENT 3 ===================

    """ Test training time and querying time of DT and RT learners
    """
    portions = np.array(range(1,10))/10.0
    leaf_size = 6

    train_time_DT = []
    query_time_DT = []
    train_time_RT = []
    query_time_DT = []


    for p in portions:
        # compute how much of the data is training and testing
        train_rows = int(p * data.shape[0])
        test_rows = data.shape[0] - train_rows

        # separate out training and testing data
        trainX = data[:train_rows,0:-1]
        trainY = data[:train_rows,-1]
        testX = data[train_rows:,0:-1]
        testY = data[train_rows:,-1]

        # dt learner
        learner = DT.DTLearner(leaf_size, verbose = False) # create a dt learner

        start = time.time()
        learner.addEvidence(trainX, trainY) # train it
        train_finish = time.time()

        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        query_finish = time.time()

        train_time_DT.append(train_finish - start)
        query_time_DT.append(query_finish - train_finish)

        # Rt learner
        learner = RT.RTLearner(leaf_size, verbose = False) # create a dt learner
        start = time.time()
        learner.addEvidence(trainX, trainY) # train it
        train_finish = time.time()
        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        query_finish = time.time()

        train_time_R.append( train_finish - start)
        query_time_RT.append(query_finish - train_finish)

    query_time_RT = query_time_RT[::-1]
    query_time_DT = query_time_DT[::-1]

    plt.figure(5)
    x = portions
    plt.plot(x, train_time_DT, label="Decision Tree", linewidth=2.0)
    plt.plot(x, train_time_RT, label="Random Tree", linewidth=2.0)
    plt.xlabel("Dataset size (proportion)")
    plt.ylabel("Speed")
    plt.legend(loc="lower right")
    plt.title("Compute time to train")
    plt.savefig('Exp3_fig4a.png')
    plt.close()

    plt.figure(6)
    x = portions
    plt.plot(x, query_time_DT, label="Decision Tree", linewidth=2.0)
    plt.plot(x, query_time_RT, label="Random Tree", linewidth=2.0)
    plt.xlabel("Dataset size (proportion)")
    plt.ylabel("Speed")
    plt.legend(loc="lower right")
    plt.title("Compute time to query")
    plt.savefig('Exp3_fig4b.png')
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
