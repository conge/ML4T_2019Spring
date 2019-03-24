"""MC2-P1: Market simulator.

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

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():

    return 'qli7' # replace tb34 with your Georgia Tech username.


def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # orders = pd.read_csv(orders_file,index_col='Date',parse_dates=True,na_values=['nan'])

    start_date = orders.index.min()
    end_date = orders.index.max()

    # Not reading in 'SPY'
    if orders.__len__() == 1:
        symbols = [orders['Symbol']]
    else:
        symbols = orders['Symbol'].unique().tolist()

    df_prices = get_data(symbols, pd.date_range(start_date, end_date), addSPY=True)
    df_prices.index.name = 'Date'
    df_prices['CASH'] = 1.0
    df_prices = df_prices.drop(labels='SPY', axis=1) # read SPY in to ensure we get every trading day in the prices dataFrame

    # start a trade dataFrame based on the prices and the orders dataFrame
    df_trades = df_prices.copy(deep=True)
    df_trades[:] = 0 # initialize the df to be all zeros.

    for i in range(orders.shape[0]):
        index =  orders.index[i]
        symbol = orders.iloc[i]['Symbol']
        order =  orders.iloc[i]['Order']
        shares =  orders.iloc[i]['Shares']

        price = df_prices.get_value(index, symbol)
        if order == 'SELL':
            shares = shares * -1
            price = (1 - impact) * price
        else:
            price = (1 + impact) * price

        cash = price * shares * -1 - commission

        # update the values in the df_trade
        trade_cash = cash + df_trades.get_value(index, 'CASH')
        trade_shares = shares + df_trades.get_value(index, symbol)

        df_trades.set_value(index, symbol, trade_shares)
        df_trades.set_value(index, 'CASH', trade_cash)


    # start a holdings dataFrame based on the prices and the orders dataFrame
    # the holdings is simply the cumulative sum of the trades. need to notice
    # the start value will affect the first Cash row.
    df_holdings = df_trades.copy(deep=True)

    #df_holdings[:] = 0 # initialize the df to be all zeros.

    # the first value of the Cash column should be the Start value + the cost of the buying the stocks.
    df_holdings.loc[df_holdings.index[0],'CASH'] += start_val

    df_holdings = df_holdings.cumsum()

    # things become easier from here
    df_values = df_prices * df_holdings
    portvals = df_values.sum(axis=1)

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    ## start_date = dt.datetime(2008,1,1)
    ## end_date = dt.datetime(2008,6,1)
    ## portvals = get_data(['IBM'], pd.date_range(start_date, end_date))
    ## portvals = portvals[['IBM']]  # remove SPY
    ## rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())

    ## return rv
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-03.csv"
    sv = 1000000

    # Process orders
    orders = pd.read_csv(of, index_col='Date', parse_dates=True, na_values=['nan']);

    portvals = compute_portvals(orders, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
