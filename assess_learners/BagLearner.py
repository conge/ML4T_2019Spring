import numpy as np


class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.models = []

    def author(self):
        return 'qli7' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Sample data the data with replacement, train the learner and get a model. repeat this 'bags' times to get models
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # build learners with the kwargs.
        for i in range(0, self.bags):
            # start a learner
            learner = self.learner(**self.kwargs)

            # create a bag of data by sampling dataX and dataY
            choice = np.random.choice(a=dataX.shape[0], size=len(dataY),replace=True)
            bag_dataX = dataX[choice]
            bag_dataY = dataY[choice]

            # train the learners with different data
            learner.addEvidence(bag_dataX, bag_dataY)

            # save the learnt model for later use
            self.models.append(learner)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        if not self.models:
            print "Please train the bag learner before querying it: learner.addEvidence(Xtrain, Ytrain)"
            return np.nan

        predY = []
        for learner in self.models:
            predY.append(learner.query(points))

        print "line 54: predY "
        print predY

        return np.mean(predY, axis=0)


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
