""" 			  		 			     			  	   		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Qingyang Li (replace with your name)
GT User ID: qli7 (replace with your User ID)
GT ID: 902265013 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import pandas as pd
import numpy as np
import util as ut 			  		 			     			  	   		   	  			  	
import random
import QLearner as ql
from marketsimcode import compute_portvals, get_portfolio_stats
from util import get_data
import indicators as id
import ManualStrategy as ms


class StrategyLearner(object):

    # constructor
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.impact = impact
        self.num_actions = 3
        self.learner = None
        self.pbins = None
        self.bbins = None
        self.mbins = None

    def author(self):

        return 'qli7' # replace tb34 with your Georgia Tech username.

    def indicators_to_state(self, PSR, bb_indicator, momentum):
        print("SL 57: PSR=",PSR, "BB=",bb_indicator, "mom=",momentum)

        momen_state = np.digitize([momentum],self.mbins,right=True)
        PSR_state = np.digitize([PSR],self.pbins,right=True)
        bbp_state = np.digitize([bb_indicator],self.bbins,right=True)

        #momen_state = pd.cut([momentum], bins=self.mbins, labels=False, include_lowest=True)
        #PSR_state = pd.cut([PSR], bins=self.pbins, labels=False, include_lowest=True)
        #bbp_state = pd.cut([bb_indicator], bins=self.bbins, labels=False, include_lowest=True)

        return momen_state[0] +PSR_state[0]*10 + bbp_state[0] * 100

    def apply_action(self, holdings, action,ret):
        """

        :param holdings: -1000, 0 or 1000
        :param action: 0 = Short, 1 = Do nothing, 2 = buy
        :param ret: return rate of the next day
        :return: updated holdings and reward
        """
        print("77 holdings, action,ret = ",holdings,action,ret)

        rewards = 0.0
        if holdings == -1000: # shorting position
            if action <= 1: # Action = { Do nothing or 0 =Short},
                rewards = -ret # holding don't change, rewards is negative of return
            else:   # actoion is  1 = BUY
                holdings = 1000  # Then holding 1000
                rewards = 2 * ret
        elif holdings == 0:
            if action == 0: # SHORT
                holdings = -1000
                rewards = -ret
            elif action == 2:
                holdings = 1000
                rewards = ret
        else: # when holdings is 1000
            if action == 0: # SHORT
                holdings = -1000
                rewards = -2 * ret
            else:
                rewards = ret

        return holdings, rewards

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # this method should create a QLearner, and train it for trading

        syms=[symbol] 			  		 			     			  	   		   	  			  	
        dates = pd.date_range(sd, ed)
        prices, prices_SPY = id.get_price(syms,dates)

        if self.verbose: print prices

        daily_returns = (prices / prices.shift(1)) - 1
        daily_returns = daily_returns[1:]

        # get indicators and combine them into as a feature data_frame
        lookback = 14

        _, PSR = id.get_SMA(prices, lookback)
        _, _, bb_indicator = id.get_BB(prices, lookback)
        momentum = id.get_momentum(prices, lookback)

        _,self.pbins = pd.qcut(PSR,10,labels=False,retbins=True)
        _,self.bbins = pd.qcut(bb_indicator,10,labels=False,retbins=True)
        _,self.mbins = pd.qcut(momentum,10,labels=False,retbins=True)
        self.pbins = self.pbins[1:-1]
        self.bbins = self.bbins[1:-1]
        self.mbins = self.mbins[1:-1]

        # start training

        converged = False
        df_trades  = None

        count = 0
        old_cum_ret = 0.0

        #print "Total number of states is:", total_states

        # Initialize QLearner,

        self.learner = ql.QLearner(num_states=10**self.num_actions,
                                   num_actions=self.num_actions,
                                   alpha=0.5,
                                   gamma=0.9,
                                   rar=0.0,
                                   radr=0.0,
                                   dyna=0,
                                   verbose=self.verbose)

        while (not converged) and (count<10):
            # Set first state to the first data point (first day)
            indices = prices.index
            holdings = pd.DataFrame(np.nan, index=indices, columns=['Holdings'])
            first_state = self.indicators_to_state(PSR.iloc[0], bb_indicator.iloc[0], momentum.iloc[0])
            action = self.learner.querysetstate(first_state)
            print("SL 152: holdings.iloc[0] = ", holdings.iloc[0], "; daily_rets.iloc[1] = ", daily_rets.iloc[1])
            holdings.iloc[0], _= self.apply_action(0, action, daily_returns.iloc[1][0])
            print("SL 153")

            df_prices = prices.copy()
            df_prices['Cash'] = pd.Series(1.0, index=indices)
            df_trades = df_prices.copy()
            df_trades[:] = 0.0

            old_holdings = 0.0
            reward = 0.0
            print("SL 163")

            # Cycle through dates
            for j in range(1, PSR.shape[0] -1):

                state = self.indicators_to_state(PSR.iloc[j], bb_indicator.iloc[j], momentum.iloc[j])

                # Get action by Query learner with current state and reward to get action
                action = self.learner.query(state, reward)

                # update rewards and holdings with the new action.
                holdings.iloc[j], rewards = self.apply_action(holdings.iloc[j], action, daily_rets.iloc[j+1])

                # Implement action returned by learner and update portfolio
            print("SL 177")
            holdings.ffill(inplace=True)
            holdings.fillna(0, inplace=True)
            trades = holdings.diff()
            trades.iloc[0] = 0
            print("SL 182")
            # buy and sell happens when the difference change direction
            df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Trades'])

            df_orders, _ = ms.generate_orders(df_trades,symbol)
            port_vals = compute_portvals(df_orders, impact=self.impact,start_val=sv)

            cum_ret, _, _, _ = get_portfolio_stats(port_vals)

            count += 1
            print("SL 192")

            # check if converge
            if abs((old_cum_ret - cum_ret)*100.0) < 0.00001:
                converged = True
            else:
                old_cum_ret = cum_ret

        return df_trades

 			  		 			     			  	   		   	  			  	
        # example use with new colname 			  		 			     			  	   		   	  			  	
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        volume = volume_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later 			  		 			     			  	   		   	  			  	
        if self.verbose: print volume 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			     			  	   		   	  			  	
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        syms=[symbol]
 			  		 			     			  	   		   	  			  	
        # here we build a fake set of trades 			  		 			     			  	   		   	  			  	
        # your code should return the same sort of data 			  		 			     			  	   		   	  			  	
        dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
        trades = prices_all[[symbol,]]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			     			  	   		   	  			  	
        trades.values[:,:] = 0 # set them all to nothing 			  		 			     			  	   		   	  			  	
        trades.values[0,:] = 1000 # add a BUY at the start 			  		 			     			  	   		   	  			  	
        trades.values[40,:] = -1000 # add a SELL 			  		 			     			  	   		   	  			  	
        trades.values[41,:] = 1000 # add a BUY 			  		 			     			  	   		   	  			  	
        trades.values[60,:] = -2000 # go short from long 			  		 			     			  	   		   	  			  	
        trades.values[61,:] = 2000 # go long from short 			  		 			     			  	   		   	  			  	
        trades.values[-1,:] = -1000 #exit on the last day
        print("220: ", trades)
        if self.verbose: print type(trades) # it better be a DataFrame! 			  		 			     			  	   		   	  			  	
        if self.verbose: print trades 			  		 			     			  	   		   	  			  	
        if self.verbose: print prices_all

        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices

        daily_rets = (prices / prices.shift(1)) - 1

        # get indicators and combine them into as a feature data_frame
        lookback = 14

        _, PSR = id.get_SMA(prices, lookback)
        _, _, bb_indicator = id.get_BB(prices, lookback)
        momentum = id.get_momentum(prices, lookback)
        indices = prices.index
        holdings = pd.DataFrame(np.nan, index=indices, columns=['Holdings'])
        holdings.iloc[0] = 0


        for i in range(daily_rets.shape[0]):

            state = self.indicators_to_state(PSR.iloc[i], bb_indicator.iloc[i], momentum.iloc[i])

            action = self.learner.querysetstate(state)

            holdings.iloc[i], _ = self.apply_action(holdings.iloc[i], action, daily_rets.iloc[i])

        holdings.ffill(inplace=True)
        holdings.fillna(0, inplace=True)
        trades = holdings.diff()
        trades.iloc[0] = 0

        # buy and sell happens when the difference change direction
        df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Trades'])

        return df_trades
 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "One does not simply think up a strategy" 			  		 			     			  	   		   	  			  	
