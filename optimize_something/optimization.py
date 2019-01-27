"""MC1-P2: Optimize a portfolio.

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
GT User ID: tb34 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 900897987 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data

from scipy import optimize as spo


def compute_daily_returns(df):
    """Compute and return daily returns"""
    daily_returns = (df / df.shift(1)) - 1
    daily_returns = daily_returns[1:]
    return daily_returns


def compute_cumulative_returens(df):
    """Compute and return cumulative returns"""
    cumulative_returns = (df / df[0]) - 1
    return cumulative_returns


def sharpe(daily_returns, rfr=0, samplingRate=252):
    """Compute Sharpe ration for a portfolio
    Input:
       allocs: allocation of a portfolio, note: allocs.sum() should be one and allocs in [0,1]
       prices: prices of all stocks in a portfolio
       rf: risk-free return
       K: K_daily = sqrt(252); K_annually = sqrt(1); K_monthly = sqrt(12)
    return:
      Sharpe_ratio
    """

    sharpe_ratio = np.sqrt(samplingRate) * (daily_returns - rfr).mean() / daily_returns.std()
    return sharpe_ratio


# this is the function that the minimizer will work on.
def neg_sharpe(allocs, prices, rfr=0, samplingRate=252):
    normed = prices / prices.iloc[0,:]
    alloced = normed * allocs
    port_val = alloced.sum(axis=1)
    daily_returns = compute_daily_returns(port_val)
    neg_sharpe_ratio = -1 * sharpe(daily_returns, rfr, samplingRate)
    return neg_sharpe_ratio


def fit_allocs(prices, sharpe_func):
    """Find the best allocation for a portfolio
    based-on the historical prices of the stocks in it.

    :param prices: prices of the portfolio
    :param sharpe_func: the function to minimize
    :return: allocs: allocation of the stocks in a portfolio

    """
    # guess value for minimizer: even distribution
    size = len(prices.columns)
    allocs_guess = np.ones(size)/size

    # Setting boundary to be [0, 1];
    # constraints to be sum(allocs) == 1
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = ((0, 1),) * size # duplicate tuple size times in a tuple

    allocs = spo.minimize(sharpe_func, allocs_guess, args=(prices,), method='SLSQP', bounds=bnds, constraints=cons)

    return allocs.x

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    """

    Return:
        allocs: A 1-d Numpy ndarray of allocations to the stocks. All the allocations must be between 0.0 and 1.0 and they must sum to 1.0.
        cr: Cumulative return
        adr: Average daily return
        ddr: Standard deviation of daily return
        sr: Sharpe ratio
    """
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed) 			  		 			     			  	   		   	  			  	
    prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			     			  	   		   	  			  	
    prices = prices_all[syms]  # only portfolio symbols 			  		 			     			  	   		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later


    # dealing with missing values in the data file.
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)

    #  find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case

    # build the function to minimize, in this case that function should be the negative Sharpe Ratio.

    # testing code
    #size = len(prices.columns)
    #allocs_guess = np.ones(size)/size
    #allocs = allocs_guess

    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations
    # cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    allocs = fit_allocs(prices, neg_sharpe)

    normed = prices / prices.iloc[0,:]
    alloced = normed * allocs
    port_val = alloced.sum(axis=1) # portfolio
    daily_returns = compute_daily_returns(port_val)

    cr = (port_val[-1] - port_val[0]) / port_val[0]
    adr = daily_returns.mean() # average daily returns
    sddr = daily_returns.std()

    sr = sharpe(daily_returns)

    #  Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    #  Compare daily portfolio value with SPY using a normalized plot
    if gen_plot: 			  		 			     			  	   		   	  			  	
        # add code to plot here 			  		 			     			  	   		   	  			  	
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)

        df_temp = df_temp / df_temp.iloc[0, :] # normoalize the data
        plot_data(df_temp, title="Performance Comparison: Portfolio V.S. SPY", ylabel="Normalized price")

    return allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			     			  	   		   	  			  	
    # It is only here to help you set up and test your code
    #
    # Define input parameters
    # Note that ALL of these values will be set to different values by 			  		 			     			  	   		   	  			  	
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date 			  		 			     			  	   		   	  			  	
    print "End Date:", end_date 			  		 			     			  	   		   	  			  	
    print "Symbols:", symbols 			  		 			     			  	   		   	  			  	
    print "Allocations:", allocations 			  		 			     			  	   		   	  			  	
    print "Sharpe Ratio:", sr 			  		 			     			  	   		   	  			  	
    print "Volatility (stdev of daily returns):", sddr 			  		 			     			  	   		   	  			  	
    print "Average Daily Return:", adr 			  		 			     			  	   		   	  			  	
    print "Cumulative Return:", cr


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader 			  		 			     			  	   		   	  			  	
    # Do not assume that it will be called 			  		 			     			  	   		   	  			  	
    test_code()

