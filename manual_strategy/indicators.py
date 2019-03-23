import pandas as pd
import datetime as dt
import numpy as np
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from util import get_data


def get_price(symbols, dates):
    # get prices of stocks indicated by the symbols, NOTE: get the adjusted closing price.

    # always get the price data with SPY to make sure there is no missing dates
    prices_all = get_data(symbols, dates, addSPY=True, colname='Adj Close')

    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # dealing with missing values in the data file.
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)

    return prices, prices_SPY


def get_SMA(prices, lookback):
    # calculate simple moving average from prices
    SMA = pd.rolling_mean(prices, window=lookback)

    return SMA


def get_BB(prices, lookback):
    # calculate Bollinger Bands from price

    SMA, _ = get_SMA(prices, lookback)
    rolling_std = pd.rolling_std(prices, window=lookback)
    upper_bb = SMA + (2 * rolling_std)
    lower_bb = SMA - (2 * rolling_std)
    bb_indicator = (prices - SMA) / (2 * rolling_std)
    return upper_bb, lower_bb, bb_indicator, SMA


def get_volatility(prices):
    daily_returns = (prices / prices.shift(1)) - 1
    daily_returns = daily_returns[1:]

    VOL = daily_returns.std()

    return VOL


def get_momentum(prices, lookback):

    momentum = prices / prices.shift(lookback) - 1
    return momentum

def plot_indicators():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code
    #
    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    dates = pd.date_range(start_date, end_date)
    symbols = ['JPM']

    # Assess the portfolio
    prices, prices_SPY = get_price(symbols, dates)

    normed_prices = prices / prices.iloc[0,:]
    normed_prices_SPY = prices_SPY / prices_SPY.iloc[0]

    upper_bb, lower_bb, bb_indicator, SMA = get_BB(prices, 14) # 14 day

    # calculate the price to SMA ratio (PSR)
    PSR = prices / SMA - 1

    fig = plt.figure(figsize=(12,6.5))
    top = plt.subplot2grid((5,1), (0,0), rowspan=4, colspan=1)
    bottom = plt.subplot2grid((5,1), (4,0), rowspan=1, colspan=1, sharex=top)

    top.plot(pd.concat([prices, SMA,upper_bb, lower_bb],axis=1))
    bottom.plot(bb_indicator, color='crimson')

    filename = '02_bb_indicator.pgn'

    plt.savefig(filename)







if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    plot_indicators()
