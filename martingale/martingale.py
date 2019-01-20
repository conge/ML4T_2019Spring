"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


def author():

    return 'qli7' # replace tb34 with your Georgia Tech username.


def gtid():

    return 902265013 # replace with your GT ID number


def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def gamble_simulator_simple(win_prob):
    winnings = np.zeros((1000))
    episode_winnings = 0
    bet_counter = 0

    while episode_winnings < 80:
        bet_amount = 1
        won = False

        while not won:
            won = get_spin_result(win_prob)
            if won:
                episode_winnings = episode_winnings + bet_amount

            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2

            winnings[bet_counter] = episode_winnings
            if bet_counter == 999: # make sure the episode won't run over 1000 times
                return winnings

            bet_counter += 1
    winnings[bet_counter:] = 80

    return winnings


def test_code():
    win_prob = 18/38.0 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once
    print get_spin_result(win_prob) # test the roulette spin
    """
    # add your code here to implement the experiments
    # Exp1_fig1
    plt.figure(0)
    for i in range(10):
        winnings = gamble_simulator_simple(win_prob)
        plt.plot(winnings,label='run %s' % i)

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Number of Spins')
    plt.ylabel('Winnings')
    plt.legend()
    plt.title("Figure 1: Winnings of the strategy\n(simple version)")
    plt.savefig('Exp1_fig1.png')
    plt.close()
    """

    # Exp1_fig2

    all_winnings = np.zeros((1000,1000))
    for i in range(20):

        all_winnings[i,:] = gamble_simulator_simple(win_prob)

    mean_winnings = np.mean(all_winnings, axis=0)
    std_winnings = np.std(all_winnings, axis=0)
    upper_line = mean_winnings + std_winnings
    lower_line = mean_winnings - std_winnings

    plt.figure(1)
    plt.plot(mean, label="Mean")
    plt.plot(upper_line, label="Mean + STD")
    plt.plot(lower_line, label="Mean - STD")

    plt.xlim((0, 300))
    plt.ylim((-256, 100))
    plt.xlabel('Number of Spins')
    plt.ylabel('Winnings')
    plt.legend()
    plt.title("Figure 2: Mean Winnings of 1000 episodes\n(simple version)")
    plt.savefig('Exp1_fig2.png')
    plt.close()



if __name__ == "__main__":
    test_code() 			  		 			     			  	   		   	  			  	
