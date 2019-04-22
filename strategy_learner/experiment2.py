import pandas as pd
import datetime as dt
import StrategyLearner, ManualStrategy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def author():

        return 'qli7'

def get_port_val_sl(impact,symbol, start_date,end_date, sv,commission = 9.95):
    sl = StrategyLearner.StrategyLearner(impact=impact,commission=commission)
    sl.addEvidence(symbol=symbol, sd=start_date, ed=end_date, sv = 100000, n_bins=5)

    df_trades_sl = sl.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)
    df_orders_sl, _ = ManualStrategy.generate_orders(df_trades_sl,symbol)
    port_vals_sl = ManualStrategy.compute_portvals(df_orders_sl, start_val=100000,
                                                   sd =start_date, ed=end_date,
                                                   commission=commission, impact=impact)
    normed_port_sl = port_vals_sl / port_vals_sl.ix[0]

    return normed_port_sl


def experiment2():

    symbol = "JPM"
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009,12, 31)
    sv = 100000
    port_val_dict = []


    plt.figure(0)
    for i in range(5):
        impact = 0.0025 * i
        port_val = get_port_val_sl(impact,symbol, start_date,end_date, sv)
        plt.plot(port_val,label='Impact is %s' % impact)

        port_val_dict.append(port_val)

    #plt.xlim((0, 300))
    #plt.ylim((-256, 100))
    #plt.xlabel('Number of Spins')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.title("Experment 2: impact on Q-learning Strategy")
    plt.savefig('03_MLS_impact_Exp2.png')


if __name__ == '__main__':
    experiment2()
