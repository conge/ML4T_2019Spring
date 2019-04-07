""" 			  		 			     			  	   		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Tucker Balch (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: qli7 (replace with your User ID)
GT ID: 902265013 (replace with your GT ID)
"""

import numpy as np
import random as rand


class QLearner(object):

    def __init__(self, \
                 num_states=100, \
                 num_actions=4, \
                 alpha=0.2, \
                 gamma=0.9, \
                 rar=0.5, \
                 radr=0.99, \
                 dyna=0, \
                 verbose=False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_states = num_states
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        # initialize Q table with random nubers
        self.Q = np.random.uniform(low=-1, high=1, size=(num_states,num_actions))

        # Parameters for Dyna_Q
        self.T_c = np.random.random(size=(num_states, num_actions, num_states))
        self.T_c.fill(0.00001)  # small value is to prevent divide by zero errors
        self.T = self.T_c/np.sum(self.T_c, axis=2, keepdims=True)  #initialize the T matrix

        self.R = self.Q.copy()
        self.R.fill(-1.0) # piazza solution, not sure why this work


    def author(self):
        return 'qli7' # replace tb34 with your Georgia Tech username.

    def querysetstate(self, s):
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			     			  	   		   	  			  	
        @param s: The new state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """
        self.s = s
        action = rand.randint(0, self.num_actions - 1)

        chance = rand.randint(1, 100) / 100.0  # a random number between 0 and 1

        if chance >= self.rar:  # This is to control when the action should be randomly selected or select the one with largest Q value
            action = np.argmax(self.Q[self.s])

        if self.verbose: print "s =", s, ", a =", action

        return action

    def query(self, s_prime, r):
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the Q table and return an action 			  		 			     			  	   		   	  			  	
        @param s_prime: The new state 			  		 			     			  	   		   	  			  	
        @param r: The ne state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """
        a = self.a
        s = self.s

        # Updates the Q Table
        action = np.argmax(self.Q[s])

        self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + \
                       self.alpha * (r + self.gamma * np.max(self.Q[s_prime, action]))

        # DYNA code
        if self.dyna != 0:
            # update T_c and T. (T_c is the count of T[s, a, s'] After real live Q upstate, but before Dyna loop
            self.T_c[s, a, s_prime] += 1

            # update T
            self.T = self.T_c/np.sum(self.T_c, axis=2, keepdims=True)

            # update R[s,a]
            self.R[s, a] = (1 - self.alpha) * self.R[s, a] + (self.alpha * r)

            for _ in range(self.dyna):
                dyna_s = rand.randint(0, self.num_states - 1)
                dyna_a = rand.randint(0, self.num_actions - 1)
                dyna_r = self.R[dyna_s, dyna_a]
                dyna_s_prime = self.T[dyna_s, dyna_a].argmax()
                dyna_a_prime = np.argmax(self.Q[dyna_s_prime])
                # update Q
                self.Q[dyna_s,dyna_a] = (1 - self.alpha) * self.Q[dyna_s,dyna_a] + \
                                        self.alpha * (dyna_r + self.gamma * self.Q[dyna_s_prime,dyna_a_prime])

        # update parameters -------
        # Select Action
        action = rand.randint(0, self.num_actions - 1)
        chance = rand.randint(1, 100) / 100.0  # a random number between 0 and 1

        if chance >= self.rar:  # This is to control when the action should be randomly selected or select the one with largest Q value
            action = np.argmax(self.Q[s_prime])

        self.a = action
        self.s = s_prime
        self.rar = self.radr * self.rar

        if self.verbose: print "s =", s, ", a = ", action, ", s' = ", s_prime,", r = ", r
        return action


if __name__ == "__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
