import pandas as pd
import datetime as dt
import numpy as np
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from util import get_data, plot_data


def get_price(symbols, dates):
    # get prices of stocks indicated by the symbols, NOTE: get the adjusted closing price.

    # always get the price data with SPY to make sure there is no missing dates
    prices = get_data(symbols, dates, addSPY=True, colname='Adj Close')

    # but ned to drop SPY before returning the data.
    prices = prices.drop(columns=['SPY'])

    # dealing with NA values, forward fill then back fill
    prices = prices.fillna(method='ffill').fillna(method='bfill')

    return prices


def get_SMA(prices, lookback):
    # calculate simple moving average from prices
    SMA = pd.rolling_mean(prices, window=lookback)

    # calculate the price to SMA ratio (PSR)
    PSR = prices / SMA

    return SMA, PSR

def get_BB(prices, lookback):
    # calculate Bollinger Bands from price

    SMA, _ = get_SMA(prices, lookback)
    rolling_std = pd.rolling_std(prices, window=lookback)
    upper_bb = SMA + (2 * rolling_std)
    lower_bb = SMA - (2 * rolling_std)
    bb_value = (prices - SMA) / (2 * rolling_std)
    return upper_bb, lower_bb, bb_value, SMA
