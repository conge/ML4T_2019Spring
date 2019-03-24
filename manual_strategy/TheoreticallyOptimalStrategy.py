import pandas as pd
import datetime as dt
import numpy as np
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from util import get_data
from marketsimcode import compute_portvals


class TheoreticallyOptimalStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol, sd, ed, sv=100000):
        ## this policy is like this: buy when the price will go up the next day, sell when the price will do down the next day
        # get price data
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
        prices = prices_all[symbol]  # only portfolio symbols
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later

        # detect price changes
        prices_diff = prices.diff()
        # if the next price change from increase to drop, today sell and short. get a -1000 position
        # if next day price change from droping to increasing, buy and long: get a 1000 position.
        # when the trend does not change, do nothing, no trading.

        position = np.sign(prices_diff.shift(-1)) * 1000
        trades = position.diff()
        trades.ix[0] = position[0]

        # buy and sell happens when the difference change direction
        df_trades = pd.DataFrame(data=trades, index = prices.index, columns = ['Trades'])

        return df_trades


def plot_optimal_strategy():

    tos = TheoreticallyOptimalStrategy()

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades = tos.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    df_orders = df_trades[['Trades']][df_trades['Trades'] != 0]

    df_orders['Symbol'] = symbol
    df_orders['Order'] = np.where(df_orders['Trades']>0, 'BUY', 'SELL')
    df_orders['Shares'] = np.abs(df_orders['Trades'])

    port_vals = compute_portvals(df_orders, start_val=100000, commission=0.0, impact=0.0)

    benchmark_orders = pd.DataFrame(data={"Symbol":[symbol], "Order":["BUY"], "Shares": [1000]}, index=[start_date])

    benchmark_vals = compute_portvals(benchmark_orders, start_val=100000, commission=0.0, impact=0.0)

    normed_port = port_vals / port_vals.ix[0]
    normed_bench = benchmark_vals / benchmark_vals.ix[0]



    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    normed_port.plot(ax=ax1, color='black', lw=1.2)
    normed_bench.plot(ax=ax1, color='blue', lw=1.2)
    ax1.set_ylabel('Normalized Portfolio Value')
    ax1.set_xlabel('Date')
    plt.grid(True)
    red_patch = mpatches.Patch(color='black', label='Best Strategy')
    blue_patch = mpatches.Patch(color='blue', label='Benchmark')
    plt.legend(handles=[red_patch,blue_patch], loc='upper left')
    plt.title('%s Best Possible Strategy' % symbol)
    #plt.show()
    plt.savefig('04_TOS.png')





if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    plot_optimal_strategy()
