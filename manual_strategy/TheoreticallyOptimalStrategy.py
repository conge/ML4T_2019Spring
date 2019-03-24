import pandas as pd
import datetime as dt
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from util import get_data
from marketsimcode import compute_portvals, get_portfolio_stats
import indicators


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
        trades.iloc[0] = position[0]
        trades.iloc[-1] = 0
        trades.columns = 'Trades'


        # buy and sell happens when the difference change direction
        df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Trades'])

        return df_trades


def plot_optimal_strategy():

    tos = TheoreticallyOptimalStrategy()

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades = tos.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    df_orders = df_trades.copy()

    df_orders = df_orders.loc[(df_orders.Trades != 0)]

    #df_orders = df_trades[['Trades']][df_trades['Trades'] != 0]

    df_orders['Symbol'] = symbol
    df_orders['Order'] = np.where(df_orders['Trades']>0, 'BUY', 'SELL')
    df_orders['Shares'] = np.abs(df_orders['Trades'])

    port_vals = compute_portvals(df_orders, start_val=100000, commission=0.0, impact=0.0)

    benchmark_orders = pd.DataFrame(data={'Symbol': ["JPM","JPM"], 'Order': ["BUY","BUY"],'Shares': [1000,0]},index={df_trades.index.min(),df_trades.index.max()})

    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = compute_portvals(benchmark_orders, start_val=100000, commission=0.0, impact=0.0)

    normed_port = port_vals / port_vals.ix[0]
    normed_bench = benchmark_vals / benchmark_vals.ix[0]


    """fig = plt.figure(figsize=(12,6.5))
    ax1 = fig.add_subplot(111)
    normed_port.plot(ax=ax1, color='red', lw=2)
    normed_bench.plot(ax=ax1, color='green', lw=1.2)
    ax1.set_ylabel('Normalized Portfolio Value')
    ax1.set_xlabel('Date')
    plt.grid(True)

    plt.legend()
    plt.title('Theoretically Optimal Strategy (%s)' % symbol)
    #plt.show()
    plt.savefig('04_TOS.png')
    """

    plt.figure(figsize=(12,6.5))
    plt.plot(normed_port, label="Portfolio", color='red', lw=2)
    plt.plot(normed_bench, label="Benchmark",color='green', lw=1.2)

    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.grid(True)
    plt.title('Theoretically Optimal Strategy (%s)' % symbol)
    plt.savefig('04_TOS.png')
    plt.close()

    port_cr, port_adr, port_stddr, port_sr = get_portfolio_stats(port_vals)
    bench_cr, bench_adr, bench_stddr, bench_sr = get_portfolio_stats(benchmark_vals)

    # Compare portfolio against benchmark
    print "=== Theoretically Optimal Strategy (TOS) ==="
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of TOS: {}".format(port_sr)
    print "Sharpe Ratio of BenchMark : {}".format(bench_sr)
    print
    print "Cumulative Return of TOS: {}".format(port_cr)
    print "Cumulative Return of Benchmark : {}".format(bench_cr)
    print
    print "Standard Deviation of TOS: {}".format(port_stddr)
    print "Standard Deviation of Benchmark : {}".format(bench_stddr)
    print
    print "Average Daily Return of TOS: {}".format(port_adr)
    print "Average Daily Return of BenchMark : {}".format(bench_adr)
    print
    print "Final TOS Portfolio Value: {}".format(port_vals[-1])
    print "Final Benchmark Portfolio Value: {}".format(benchmark_vals[-1])
    print




if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    plot_optimal_strategy()
