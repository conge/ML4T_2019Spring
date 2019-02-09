# coding=utf-8
"""
A simple wrapper for decision tree  (c) 2019 Qingyang Li


"""

import numpy as np


class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'qli7' # replace tb34 with your Georgia Tech username

    def find_best_feature(self,dataX,dataY):
        """
        @Summary: find the index of best feature in dataX based on the absolute correlation with dataY
        :param dataX: Training data of Xs
        :param dataY: Training data, Y
        :return: the index of the best feature
        """

        corrs = []
        for i in range(dataX.shape[1]):
            tmp = np.corrcoef(dataX[:, i], dataY) # calculate correlation coeficient
            corr = abs(tmp[0, 1])  # get the absolute value of the correlation coeficient (r)
            corrs.append(corr)

        best_feature_index = np.argmax(corrs)

        return best_feature_index

    def buildTree(self, dataX, dataY):

        # stop conditions

        # condition 1: the tree is not splittable when the size of the data is less or equal to leaf_size
        if dataX.shape[0] <= self.leaf_size:
            leaf = np.array([[-1, np.mean(dataY), -1, -1]])  # leaf node when factor is -1, [factor, value, left, right]
            return leaf

        # condition 2: the tree is not worth splitting when all the value in dataY is the same
        if np.all(dataY == dataY[0]):
            return np.array([[-1, dataY[0], -1, -1]])  # in this case, np.mean(dataY) and dataY[0] are the same
            # return np.array([[-1, np.mean(dataY), -1, -1]])

        # find the "best feature to split on" as the feature (Xi) that has the highest absolute value correlation with Y
        best_feature_index = self.find_best_feature(dataX, dataY)

        feature_to_split = dataX[:, best_feature_index]
        split_value = np.median(feature_to_split)

        # condition 3：when the median of the data is the largest value, there is no way to split it further
        if np.all(feature_to_split <= split_value):
            return np.array([[-1, np.mean(dataY), -1, -1]])

        # split the feature
        split_left = feature_to_split <= split_value  # left tree data index, less than or equal to the split_value
        split_right = ~split_left

        left_dataX = dataX[split_left]
        left_dataY = dataY[split_left]
        right_dataX = dataX[split_right]
        right_dataY = dataY[split_right]

        left_branch = self.buildTree(left_dataX,left_dataY)
        right_branch = self.buildTree(right_dataX,right_dataY)

        root = np.array([[best_feature_index, split_value, 1, left_branch.shape[0] + 1]])

        return np.vstack((root, left_branch, right_branch))

    def addEvidence(self, dataX, dataY):
        """ 			  		 			     			  	   		   	  			  	
        @summary: Add training data to learner, train a model and save it
        @param dataX: X values of data to add 			  		 			     			  	   		   	  			  	
        @param dataY: the Y training values 
        """

        self.tree = self.buildTree(dataX, dataY)

        if self.verbose:
            print ("the author of this code is ",self.author())
            if self.tree is None:
                print ("The tree is empty!")
            else:
                print ("The leaf size is ", self.leaf_size)
                print ("The shape of tree is ", self.tree.shape)
                print ("The tree is：")
                print (self.tree)

    def query(self, points):
        """ 			  		 			     			  	   		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			     			  	   		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			     			  	   		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			     			  	   		   	  			  	
        """

        predY = []
        for point in points:

            keep_searching = True
            node_index = 0 # start searching from the root for each row of input data (points).
            while keep_searching:
                factor = int(self.tree[node_index,0])  # get factor to check

                # check if the node is leaf,
                if factor == -1:  # if yes, then we get the predicted value for point, and we can stop searching.
                    predY = predY.append(self.tree[node_index,1])
                    keep_searching = False

                else:  # if not compare the factor value with the points to determine which node to search
                    split_value = self.tree[node_index,1]
                    if point[factor] <= split_value:
                        node_index = node_index + int(self.tree[node_index, 2])  # goes to the left branch
                    else:
                        node_index = node_index + int(self.tree[node_index, -1])  # goes to the right branch

        return predY


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"

