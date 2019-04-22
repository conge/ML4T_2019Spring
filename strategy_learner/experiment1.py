import pandas as pd
import ManualStrategy
import StrategyLearner
import datetime as dt
from util import get_data
import indicators as id
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def author():

        return 'qli7'

def experiment1():

    ms = ManualStrategy.ManualStrategy()
    sl = StrategyLearner.StrategyLearner()
    sl.addEvidence()

    commission = 9.95
    impact = 0.005

    # in sample
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    sl.addEvidence(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    df_trades_ms = ms.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)
    df_trades_sl = sl.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    # generate orders based on trades
    df_orders_ms, benchmark_orders= ManualStrategy.generate_orders(df_trades_ms,symbol)
    df_orders_sl, _ = ManualStrategy.generate_orders(df_trades_sl,symbol)

    port_vals_ms = ManualStrategy.compute_portvals(df_orders_ms, start_val=100000, sd =start_date, ed=end_date, commission=commission, impact=impact)
    port_vals_sl = ManualStrategy.compute_portvals(df_orders_sl, start_val=100000, sd =start_date, ed=end_date, commission=commission, impact=impact)
    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = ManualStrategy.compute_portvals(benchmark_orders, sd =start_date, ed=end_date,start_val=100000, commission=commission, impact=impact)

    normed_port_ms = port_vals_ms / port_vals_ms.ix[0]
    normed_port_sl = port_vals_sl / port_vals_sl.ix[0]
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
    for index, marks in df_trades_sl.iterrows():
        if marks['Trades'] > 0:
            plt.axvline(x=index, color='blue',linestyle='dashed', alpha = .9)
        elif marks['Trades'] < 0:
            plt.axvline(x=index, color='black',linestyle='dashed', alpha = .9)
        else:
            pass

    top.xaxis_date()
    top.grid(True)
    top.plot(normed_port_sl, lw=2, color='red', label='Q-Learning Strategy')
    top.plot(normed_port_ms, lw=1.5, color='black', label='Manual Strategy')
    top.plot(normed_bench, lw=1.2, color='green', label='Benchmark')

    top.set_title('Portfolio V.S Benchmark - In Sample Analysis')
    top.set_ylabel('Normalized Value')
    for index, marks in df_trades_sl.iterrows():
        if marks['Trades'] > 0:
            top.axvline(x=index, color='blue',linestyle='dashed', alpha=.9)
        elif marks['Trades'] < 0:
            top.axvline(x=index, color='black',linestyle='dashed', alpha=.9)
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

    filename = '05_MLS_insample.png'

    plt.savefig(filename)

    plt.close()

    port_cr_sl, port_adr_sl, port_stddr_sl, port_sr_sl = ManualStrategy.get_portfolio_stats(port_vals_ms)
    port_cr_ms, port_adr_ms, port_stddr_ms, port_sr_ms = ManualStrategy.get_portfolio_stats(port_vals_ms)
    bench_cr, bench_adr, bench_stddr, bench_sr = ManualStrategy.get_portfolio_stats(benchmark_vals)

    # Compare portfolio against benchmark
    print "=== Machine Learning Strategy (MLS) V.S. Manual Strategy (MS) In Sample ==="
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of MLS: {}".format(port_sr_sl)
    print "Sharpe Ratio of MS: {}".format(port_sr_ms)
    print "Sharpe Ratio of BenchMark : {}".format(bench_sr)
    print
    print "Cumulative Return of MLS: {}".format(port_cr_sl)
    print "Cumulative Return of MS: {}".format(port_cr_ms)
    print "Cumulative Return of Benchmark : {}".format(bench_cr)
    print
    print "Standard Deviation of MLS: {}".format(port_stddr_sl)
    print "Standard Deviation of MS: {}".format(port_stddr_ms)
    print "Standard Deviation of Benchmark : {}".format(bench_stddr)
    print
    print "Average Daily Return of MLS: {}".format(port_adr_sl)
    print "Average Daily Return of MS: {}".format(port_adr_ms)
    print "Average Daily Return of BenchMark : {}".format(bench_adr)
    print
    print "Final MLS Portfolio Value: {}".format(port_vals_sl[-1])
    print "Final MS Portfolio Value: {}".format(port_vals_ms[-1])
    print "Final Benchmark Portfolio Value: {}".format(benchmark_vals[-1])
    print

    # ========================
    # OUT OF SAMPLE Analysis
    # ========================
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades_ms = ms.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)
    df_trades_sl = sl.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    # generate orders based on trades
    df_orders_ms, benchmark_orders= ManualStrategy.generate_orders(df_trades_ms,symbol)
    df_orders_sl, _ = ManualStrategy.generate_orders(df_trades_sl,symbol)

    port_vals_ms = ManualStrategy.compute_portvals(df_orders_ms, start_val=100000, sd =start_date, ed=end_date, commission=commission, impact=impact)
    port_vals_sl = ManualStrategy.compute_portvals(df_orders_sl, start_val=100000, sd =start_date, ed=end_date, commission=commission, impact=impact)
    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = ManualStrategy.compute_portvals(benchmark_orders, sd =start_date, ed=end_date,start_val=100000, commission=commission, impact=impact)

    normed_port_ms = port_vals_ms / port_vals_ms.ix[0]
    normed_port_sl = port_vals_sl / port_vals_sl.ix[0]
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
    for index, marks in df_trades_sl.iterrows():
        if marks['Trades'] > 0:
            plt.axvline(x=index, color='blue',linestyle='dashed', alpha = .9)
        elif marks['Trades'] < 0:
            plt.axvline(x=index, color='black',linestyle='dashed', alpha = .9)
        else:
            pass

    top.xaxis_date()
    top.grid(True)
    top.plot(normed_port_sl, lw=2, color='red', label='Q-Learning Strategy')
    top.plot(normed_port_ms, lw=1.5, color='black', label='Manual Strategy')
    top.plot(normed_bench, lw=1.2, color='green', label='Benchmark')

    top.set_title('Portfolio V.S Benchmark - Out Sample Analysis')
    top.set_ylabel('Normalized Value')
    for index, marks in df_trades_sl.iterrows():
        if marks['Trades'] > 0:
            top.axvline(x=index, color='blue',linestyle='dashed', alpha=.9)
        elif marks['Trades'] < 0:
            top.axvline(x=index, color='black',linestyle='dashed', alpha=.9)
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

    filename = '06_MLS_outsample.png'

    plt.savefig(filename)

    plt.close()

    port_cr_sl, port_adr_sl, port_stddr_sl, port_sr_sl = ManualStrategy.get_portfolio_stats(port_vals_ms)
    port_cr_ms, port_adr_ms, port_stddr_ms, port_sr_ms = ManualStrategy.get_portfolio_stats(port_vals_ms)
    bench_cr, bench_adr, bench_stddr, bench_sr = ManualStrategy.get_portfolio_stats(benchmark_vals)

    # Compare portfolio against benchmark
    print "=== Machine Learning Strategy (MLS) V.S. Manual Strategy (MS) OUT Sample ==="
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of MLS: {}".format(port_sr_sl)
    print "Sharpe Ratio of MS: {}".format(port_sr_ms)
    print "Sharpe Ratio of BenchMark : {}".format(bench_sr)
    print
    print "Cumulative Return of MLS: {}".format(port_cr_sl)
    print "Cumulative Return of MS: {}".format(port_cr_ms)
    print "Cumulative Return of Benchmark : {}".format(bench_cr)
    print
    print "Standard Deviation of MLS: {}".format(port_stddr_sl)
    print "Standard Deviation of MS: {}".format(port_stddr_ms)
    print "Standard Deviation of Benchmark : {}".format(bench_stddr)
    print
    print "Average Daily Return of MLS: {}".format(port_adr_sl)
    print "Average Daily Return of MS: {}".format(port_adr_ms)
    print "Average Daily Return of BenchMark : {}".format(bench_adr)
    print
    print "Final MLS Portfolio Value: {}".format(port_vals_sl[-1])
    print "Final MS Portfolio Value: {}".format(port_vals_ms[-1])
    print "Final Benchmark Portfolio Value: {}".format(benchmark_vals[-1])
    print

if __name__ == '__main__':
    experiment1()
