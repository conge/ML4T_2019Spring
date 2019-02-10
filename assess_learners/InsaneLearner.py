import BagLearner as bl
import LinRegLearner as lrl

"""
import InsaneLearner as it
learner = it.InsaneLearner(verbose = False) # constructor
learner.addEvidence(Xtrain, Ytrain) # training step
Y = learner.query(Xtest) # query
"""
class InsaneLearner(object):

    def __init__(self, verbose = False):
        self.verbose = verbose
        # initialize the learner to be a bag learner with 20 LinRegLearners.
        self.learners = []
        for i in range(20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=self.verbose))

    def author(self):
        return 'qli7' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Sample data the data with replacement, train the learner and get a model. repeat this 'bags' times to get models
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # train all the learners

        for learner in self.learners:

            # train the learners with different data
            learner.addEvidence(dataX, dataY)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """

        predY = []
        for learner in self.learners:
            predY.append(learner.query(points))

        return np.mean(predY, axis=0)  # average of the predicted value by all models is the result of the bagLearner
