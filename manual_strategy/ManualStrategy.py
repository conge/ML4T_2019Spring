import pandas as pd
import datetime as dt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from util import get_data
from marketsimcode import compute_portvals, get_portfolio_stats
import indicators as id


class ManualStrategy(object):
    def __init__(self):
        pass


    def testPolicy(self, symbol, sd, ed, sv=100000):
        # this policy is like this: buy when the price will go up the next day, sell when the price will do down the next day
        # get price data
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
        prices = prices_all[symbol]  # only portfolio symbols

        # get indicators
        lookback = 14

        _, PSR = id.get_SMA(prices, lookback)
        _, _, bb_indicator = id.get_BB(prices, lookback)
        momentum = id.get_momentum(prices, lookback)

        holdings = pd.DataFrame(np.nan, index=prices.index, columns=['Holdings'])

        # make sure when PSR (= price / SMA -1) >0.05 and bb_indicator > 1 and momentum > 0.05 SELL or hold -1000
        # when PSR (= price / SMA -1) < -0.05 and bb_indicator < -1 and momentum < -0.05 Buy or hold -1000

        print("PSR: ", PSR)
        print("momentum: ", momentum)
        print("bb_indicator: ", bb_indicator)

        for t in range(prices.shape[0]):
            if PSR.iloc[t]< -0.02 and bb_indicator.iloc[t] < -0.8 and momentum.iloc[t] < -0.03:
                holdings.iloc[t] = 1000
            elif PSR.iloc[t] > 0.02 and bb_indicator.iloc[t] > 0.8 and momentum.iloc[t] > 0.03:
                holdings.iloc[t] = -1000

        # fill the NAN data
        holdings.ffill(inplace=True)
        holdings.fillna(0, inplace=True)
        trades = holdings.diff()
        trades.iloc[0] = 0
        #trades.iloc[-1] = 0
        #trades.columns = 'Trades'

        # buy and sell happens when the difference change direction
        df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Trades'])

        return df_trades


def generate_orders(df_trades,symbol):
    df_orders = df_trades.copy()
    df_orders[-1] = 1

    df_orders = df_orders.loc[(df_orders.Trades != 0)]

    #df_orders = df_trades[['Trades']][df_trades['Trades'] != 0]

    df_orders['Symbol'] = symbol
    df_orders['Order'] = np.where(df_orders['Trades']>0, 'BUY', 'SELL')
    df_orders['Shares'] = np.abs(df_orders['Trades'])
    df_orders.loc[df_orders.index[-1],'Shares'] = 0

    benchmark_orders = pd.DataFrame(data={'Symbol': [symbol,symbol], 'Order': ["BUY","BUY"],'Shares': [1000,0]},
                                    index={df_trades.index.min(), df_trades.index.max()})

    return df_orders, benchmark_orders


def plot_manual_strategy():

    ms = ManualStrategy()

    commission = 9.95
    impact = 0.005

    # in sample
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades = ms.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    # generate orders based on trades
    df_orders, benchmark_orders= generate_orders(df_trades,symbol)

    port_vals = compute_portvals(df_orders, start_val=100000, commission=commission, impact=impact)
    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = compute_portvals(benchmark_orders, start_val=100000, commission=commission, impact=impact)

    normed_port = port_vals / port_vals.ix[0]
    normed_bench = benchmark_vals / benchmark_vals.ix[0]

    dates = pd.date_range(start_date, end_date)
    prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
    prices = prices_all[symbol]  # only portfolio symbols

    # get indicators
    lookback = 14

    _, PSR = id.get_SMA(prices, lookback)
    _, _, bb_indicator = id.get_BB(prices, lookback)
    momentum = id.get_momentum(prices, lookback)

    # figure 5.
    plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=3, colspan=1)
    bottom = plt.subplot2grid((5,1), (3,0), rowspan=2, colspan=1, sharex=top)

    # plot the Long or short action
    for index, marks in df_trades.iterrows():
        if marks['Trades'] > 0:
            plt.axvline(x=index, color='blue',linestyle='dashed', alpha = .5)
        elif marks['Trades'] < 0:
            plt.axvline(x=index, color='black',linestyle='dashed', alpha = .5)
        else:
            pass

    top.xaxis_date()
    top.grid(True)
    top.plot(normed_port, lw=2, color='red', label='Manual Strategy')
    top.plot(normed_bench, lw=1.2, color='green', label='Benchmark')

    top.set_title('Portfolio V.S Benchmark - In Sample Analysis')
    top.set_ylabel('Normalized Value')
    for index, marks in df_trades.iterrows():
        if marks['Trades'] > 0:
            top.axvline(x=index, color='green',linestyle='dashed', alpha = .5)
        elif marks['Trades'] < 0:
            top.axvline(x=index, color='red',linestyle='dashed', alpha = .5)
        else:
            pass

    bottom.plot(momentum, color='olive', lw=1, label="momentum")
    bottom.plot(PSR, color='purple', lw=1, label="PSR")
    #bottom.plot(bb_indicator, color='blue', lw=1, label="Bollinger")
    bottom.set_title('Indicators')

    bottom.axhline(y = -0.2,  color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0.2,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.legend()

    top.legend()
    top.axes.get_xaxis().set_visible(False)
    plt.xlim(start_date,end_date)

    filename = '05_MS_insample.png'

    plt.savefig(filename)

    plt.close()

    port_cr, port_adr, port_stddr, port_sr = get_portfolio_stats(port_vals)
    bench_cr, bench_adr, bench_stddr, bench_sr = get_portfolio_stats(benchmark_vals)

    # Compare portfolio against benchmark
    print "=== Manual Strategy (MS) In Sample ==="
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of MS: {}".format(port_sr)
    print "Sharpe Ratio of BenchMark : {}".format(bench_sr)
    print
    print "Cumulative Return of MS: {}".format(port_cr)
    print "Cumulative Return of Benchmark : {}".format(bench_cr)
    print
    print "Standard Deviation of MS: {}".format(port_stddr)
    print "Standard Deviation of Benchmark : {}".format(bench_stddr)
    print
    print "Average Daily Return of MS: {}".format(port_adr)
    print "Average Daily Return of BenchMark : {}".format(bench_adr)
    print
    print "Final MS Portfolio Value: {}".format(port_vals[-1])
    print "Final Benchmark Portfolio Value: {}".format(benchmark_vals[-1])
    print

    # ========================
    # OUT OF SAMPLE Analysis
    # ========================
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades = ms.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    # generate orders based on trades
    df_orders, benchmark_orders= generate_orders(df_trades,symbol)

    port_vals = compute_portvals(df_orders, start_val=100000, commission=commission, impact=impact)
    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = compute_portvals(benchmark_orders, start_val=100000, commission=commission, impact=impact)

    normed_port = port_vals / port_vals.ix[0]
    normed_bench = benchmark_vals / benchmark_vals.ix[0]

    dates = pd.date_range(start_date, end_date)
    prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
    prices = prices_all[symbol]  # only portfolio symbols

    # get indicators
    lookback = 14

    _, PSR = id.get_SMA(prices, lookback)
    _, _, bb_indicator = id.get_BB(prices, lookback)
    momentum = id.get_momentum(prices, lookback)

    # figure 6.
    plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=3, colspan=1)
    bottom = plt.subplot2grid((5,1), (3,0), rowspan=2, colspan=1, sharex=top)

    # plot the
    for index, marks in df_trades.iterrows():
        if marks['Trades'] > 0:
            plt.axvline(x=index, color='blue',linestyle='dashed')
        elif marks['Trades'] < 0:
            plt.axvline(x=index, color='blak',linestyle='dashed')
        else:
            pass

    top.xaxis_date()
    top.grid(True)
    top.plot(normed_port, lw=2, color='red', label='Manual Strategy')
    top.plot(normed_bench, lw=1.2, color='green', label='Benchmark')

    # plot the Long or short action
    for index, marks in df_trades.iterrows():
        if marks['Trades'] > 0:
            top.axvline(x=index, color='blue', linestyle='dashed', alpha = .5)
        elif marks['Trades'] < 0:
            top.axvline(x=index, color='black', linestyle='dashed', alpha = .5)
        else:
            pass

    top.set_title('Portfolio V.S Benchmark - Out Sample Analysis')
    top.set_ylabel('Normalized Value')
    bottom.plot(momentum, color='olive', lw=1, label="momentum")
    bottom.plot(PSR, color='purple', lw=1, label="PSR")
    #bottom.plot(bb_indicator, color='blue', lw=1, label="Bollinger")
    bottom.set_title('Indicators')

    bottom.axhline(y = -0.2,  color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.axhline(y = 0.2,   color = 'grey', linestyle='--', alpha = 0.5)
    bottom.legend()

    top.legend()
    top.axes.get_xaxis().set_visible(False)
    plt.xlim(start_date,end_date)

    filename = '06_MS_OutSample.png'

    plt.savefig(filename)

    plt.close()

    port_cr, port_adr, port_stddr, port_sr = get_portfolio_stats(port_vals)
    bench_cr, bench_adr, bench_stddr, bench_sr = get_portfolio_stats(benchmark_vals)

    # Compare portfolio against benchmark
    print "=== Manual Strategy (MS) Out Sample ==="
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of MS: {}".format(port_sr)
    print "Sharpe Ratio of BenchMark : {}".format(bench_sr)
    print
    print "Cumulative Return of MS: {}".format(port_cr)
    print "Cumulative Return of Benchmark : {}".format(bench_cr)
    print
    print "Standard Deviation of MS: {}".format(port_stddr)
    print "Standard Deviation of Benchmark : {}".format(bench_stddr)
    print
    print "Average Daily Return of MS: {}".format(port_adr)
    print "Average Daily Return of BenchMark : {}".format(bench_adr)
    print
    print "Final MS Portfolio Value: {}".format(port_vals[-1])
    print "Final Benchmark Portfolio Value: {}".format(benchmark_vals[-1])
    print



if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    #plot_optimal_strategy()
    plot_manual_strategy()
