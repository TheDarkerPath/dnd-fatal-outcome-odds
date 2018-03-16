#   Author: Geoff Moore
#   Monte Carlo Simulation of fatal outcomes on DnD dice rolls. My current game
#   involves homebrew rules with some fatal or character retiring outcomes
#   for fumbles and crits. This program simulates this scenario and plots the
#   cumulative occurrence of fatal outcomes over time. It also calculates
#   probabilities of fatal outcomes from the generated data which can be used
#   to check the model against actual probabilities. Values for cutoffs for
#   crits and fumbles on the d20 and fatal outcomes on the d100 can be varied.

# Import modules
import random
import os
import sys, signal
import numpy as np
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt

# Code to allow graceful termintation
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

############################################################################################################
# Change values below to play with cutoffs for crits and fumbles on the d20 and fatal outcomes on the d100 #
#                                                                                                          #
############################################################################################################
# define cutoffs for crits and fumbles on the d20
# Cutoff values must be within these ranges:
# 1 < d20_fumble_cutoff < 20
# 1 < d20_crit_cutoff < 20
d20_fumble_cutoff = 1
d20_crit_cutoff = 20

# define cutoffs for fatal or character-retiring outcomes on d100 following crit or fumble on d20
# for the purposes of this simulation, higher values are worse
# A crit or fumble cutoff value can be > 100 which means there are no fatal consequences for that type of roll
d100_fatal_fumble_cutoff = 99
d100_fatal_crit_cutoff = 98

# define number of runs to execute (each run forms a distinct line in the cumulative plot)
number_of_runs = 60

# define number of rounds in each run of the simulation
number_of_rounds = 500

# define number of players
number_of_players = 4

# define whether to output each roll and result (WARNING: for large runs extremely processor intensive)
# 1 = output each roll
# 0 = no roll output
output_each_roll = 0

# display run summary stats and calculate and plot cumulative fatal outcomes for each run
plot_cumulative_results = 1

# calculate and plot predicted poisson stats and compare with observed
plot_poisson_stats = 1
############################################################################################################
# End of main values for editing                                                                           #
#                                                                                                          #
############################################################################################################

# define functions to roll the dice
def rollD20():
    roll = random.randint(1,20)
    return roll

def rollD100():
    roll = random.randint(1,100)
    return roll

######################################################################################
# Calculate ideal mathematical odds for d20 crits and fumbles per round, also fatal
# outcome per round for later comparison with observed stats from simulated data
predicted_chance_d20_fumble = (d20_fumble_cutoff / 20) * number_of_players
predicted_chance_d20_crit = (21 - d20_crit_cutoff ) / 20
predicted_chance_fatal_fumble = predicted_chance_d20_fumble * ( (101 - d100_fatal_fumble_cutoff ) / 100 )
predicted_chance_fatal_crit =  predicted_chance_d20_crit * (101 - d100_fatal_crit_cutoff ) / 100
predicted_total_chance_fatal_outcome = predicted_chance_fatal_fumble + predicted_chance_fatal_crit

# initialise variable to count observed poisson stats
# (records number of fatal outcomes in each run)
poisson_run_number = []
poisson_observed_fatal_outcomes_per_run = []

##########################################
# Loop to execute number_of_runs runs of the simulation
run_loop_counter = 0
for run_loop_counter in range(0,number_of_runs):

    print('\n\n----------------------------------------------------------------------------------- Starting run ->', run_loop_counter + 1, 'of', number_of_runs)

    #initialise fumble and crit counters
    d20_fumble_counter = 0
    d20_crit_counter = 0
    d100_fumble_fatal_outcome = 0
    d100_crit_fatal_outcome = 0

    # define variables to track and pyplot
    plot_round_number_X = []
    plot_total_number_of_fatal_outcomes_Y = []

    # initialise poisson fatal outcomes counter
    poisson_run_fatal_outcomes_counter = 0

    ###################################################################
    # Loop to execute number_of_rounds rounds
    round_loop_counter = 0
    for round_loop_counter in range(0,number_of_rounds):
        if output_each_roll:
            print('round ', round_loop_counter)

        # Get OS-generated random number as seed before each round
        random_data = os.urandom(64)
        seed = int.from_bytes(random_data, byteorder="big")
        random.seed(seed)

        # Player roll section
        # Simulates a player attacking a monster

        # Loop to execute number_of_players player rolls
        player_loop_counter = 0
        for player_loop_counter in range(0,number_of_players):
            # roll the d20 and check the result
            D20result = rollD20()
            if output_each_roll:
                print('   player ', player_loop_counter + 1, ' -> ', D20result)

            # If fumble, enter d20 fumble loop
            if D20result <= d20_fumble_cutoff:
                d20_fumble_counter += 1 # increment the d20_fumble_cutoff counter
                D100result = rollD100()
                if output_each_roll:
                    print('-------------------d20 Fumble!')
                    print('-------------------D100 roll--> ', D100result)

                # ... and enter the D100 check loop
                if D100result >= d100_fatal_fumble_cutoff:
                    d100_fumble_fatal_outcome +=1 # increment the d100_fumble_fatal_outcome counter
                    poisson_run_fatal_outcomes_counter +=1 # increment poisson run fatal outcomes counter
                    if output_each_roll:
                        print('-----------------------------------------FATAL d100 FUMBLE!------------------')
                        print('-----------------------------------------------------------------------------')


        # DM roll section
        # Simulates the DM rolling for a monster to attack a player

        # roll the d20 and check the result
        D20result = rollD20()
        if output_each_roll:
            print('   DM attack  -> ', D20result)
        # If crit, enter d20 crit loop
        if D20result >= d20_crit_cutoff:
            d20_crit_counter += 1 # increment the d20_crit_cutoff counter
            D100result = rollD100()
            if output_each_roll:
                print('-------------------d20 Crit!')
                print('-------------------D100 roll--> ', D100result)

            # ... and enter the D100 check loop
            if D100result >= d100_fatal_crit_cutoff:
                d100_crit_fatal_outcome +=1 # increment the d100_crit_fatal_outcome counter
                poisson_run_fatal_outcomes_counter +=1 # increment poisson run fatal outcomes counter
                if output_each_roll:
                    print('---------------------------------------------FATAL d100 CRIT!-------------------')
                    print('--------------------------------------------------------------------------------')

        # Append x and y values for plotting this round's total fatal outcomes
        plot_round_number_X.append(round_loop_counter)
        plot_total_number_of_fatal_outcomes_Y.append(d100_fumble_fatal_outcome + d100_crit_fatal_outcome)

    ######################
    # End the rounds loop

    # Append values for tracking poisson end run stats
    poisson_run_number.append(run_loop_counter)
    poisson_observed_fatal_outcomes_per_run.append(poisson_run_fatal_outcomes_counter)

    #####################################################
    # Calculate and print (per round) stats for whole run
    # from observed simulated data
    chance_d20_fumble = d20_fumble_counter / number_of_rounds
    chance_d20_crit = d20_crit_counter / number_of_rounds
    chance_fatal_fumble = d100_fumble_fatal_outcome / number_of_rounds
    chance_fatal_crit = d100_crit_fatal_outcome / number_of_rounds

    if plot_cumulative_results:
        print('\n\n\n-----------------------------------------------------------------------------------------------------')
        print('--------------------------- Summary stats for run number', run_loop_counter + 1)
        print('---------------------------', number_of_rounds, 'rounds with', number_of_players, 'players\n')
        print('--------------------------- ')

        # d20 fumble and crit stats per round, observed vs predicted
        print('d20 fumble and crit stats per round, observed vs predicted')
        print('----------------------------------------------------------\n')

        # d20 fumble stats per round, observed vs predicted
        if chance_d20_fumble > 0:
            print('  -- chance of d20 fumble per round from generated data is roughly 1 /', round (1 / chance_d20_fumble, 0), ' vs. 1 /', round (1 / predicted_chance_d20_fumble, 0),
                                ' predicted (abs number of d20 fumbles is', d20_fumble_counter, ')\n')
        else:
            print('  -- chance of d20 fumble per round from generated data is 0 vs. 1/', round (1 / predicted_chance_d20_fumble, 0), ' predicted (abs number of d20 fumbles is 0)\n')

        # d20 crit stats per round, observed vs predicted
        if chance_d20_crit > 0:
            print('  -- chance of d20 crit per round from generated data is roughly 1 / ', round (1 / chance_d20_crit, 0), ' vs. 1 /', round (1 / predicted_chance_d20_crit, 0),
                                ' predicted (abs number of d20 crits is', d20_crit_counter, ')\n\n')
        else:
            print('  -- chance of d20 crit per round from generated data is 0  vs. 1 /', round (1 / predicted_chance_d20_crit, 0) , ' predicted (abs number of d20 crits is 0)\n\n')

        # fatal fumble and crit stats per round, observed vs predicted
        print('fatal fumble and crit stats per round, observed vs predicted')
        print('------------------------------------------------------------\n')

        # fatal fumble stats per round, observed vs predicted

        if chance_fatal_fumble > 0:
            print('  -- chance of fatal fumble per round from generated data is roughly 1 / ', round (1 / chance_fatal_fumble, 0), ' vs. 1 /', round (1 / predicted_chance_fatal_fumble, 0) ,
                                ' predicted (abs number of fatal fumbles is', d100_fumble_fatal_outcome, ')\n')
        else:
            if predicted_chance_fatal_fumble > 0:
                print('  -- chance of fatal fumble per round from generated data is 0 vs. 1 /', round (1 / predicted_chance_fatal_fumble, 0) , ' predicted (abs number of fatal fumbles is 0)\n')
            else:
                print('  -- chance of fatal fumble per round from generated data is 0 vs. 0 predicted (abs number of fatal fumbles is 0)\n')

        # fatal crit stats per round, observed vs predicted
        if chance_fatal_crit > 0:
            print('  -- chance of fatal crit per round from generated data is roughly 1 / ', round (1 / chance_fatal_crit, 0), ' vs. 1 /', round (1 / predicted_chance_fatal_crit, 0),
                                ' predicted (abs number of fatal crits is', d100_crit_fatal_outcome, ')\n\n')
        else:
            if predicted_chance_fatal_crit > 0:
                print('  -- chance of fatal crit per round from generated data is 0 vs. 1 /', round (1 / predicted_chance_fatal_crit, 0) , ' predicted  (abs number of fatal crits is 0)\n')
            else:
                print('  -- chance of fatal crit per round from generated data is 0 vs. 0 predicted  (abs number of fatal crits is 0)\n')

        print('total fatal fumble and crit stats per round, observed vs predicted')
        print('------------------------------------------------------------------\n')

        # total fatal outcome stats per round, observed vs. predicted
        if chance_fatal_fumble + chance_fatal_crit > 0:
            print('  -- TOTAL chance of fatal outcome per round from generated data is roughly 1 /', round (1 / (chance_fatal_fumble + chance_fatal_crit), 0), ' vs. 1 /',
                                    round (1 / (predicted_total_chance_fatal_outcome), 0) , ' predicted (abs number of fatal crits is', d100_fumble_fatal_outcome + d100_crit_fatal_outcome, ')\n')
        else:
            print('  -- TOTAL chance of fatal outcome per round from generated data is 0 vs. 0 predicted (abs number of fatal crits is 0)\n')


        ########################################################
        # Plot total number of fatal outcomes versus round number
        plt.plot(plot_round_number_X,plot_total_number_of_fatal_outcomes_Y)

##############
# End run loop

if plot_cumulative_results:
    # Finalise and draw plot for fatal outcomes with axis labels and title
    plt.ylabel('Running total of fatal outcomes')
    plt.xlabel('No of rounds taken')
    # If predicted probabilities > 0 then express as 1/n
    if ( (predicted_chance_fatal_fumble > 0) and (predicted_chance_fatal_crit > 0) ):
        plot_title = ('Monte Carlo Simulation of fatal crits and fumbles over time\nVerticals represent fatal outcomes for characters from fumbles they make or crits against them\n' + str(number_of_runs) + ' run(s) of ' +
            str(number_of_rounds) + ' rounds & ' + str(number_of_players) + ' player(s) | fatal fumble d100 >= ' + str(d100_fatal_fumble_cutoff) + ' (ideal odds/round 1/' +
            str(round (1 / predicted_chance_fatal_fumble, 0)) + ')\n| fatal crit d100 >= ' + str(d100_fatal_crit_cutoff) +
            ' (ideal odds/round 1/' + str(round (1 / predicted_chance_fatal_crit, 0)) + ') | total ideal fatal odds/round 1/' +
            str(round (1 / (predicted_total_chance_fatal_outcome))))
    # ... otherwise use decimal expression to avoid div by zero
    else:
            plot_title = ('Monte Carlo Simulation of fatal crits and fumbles over time\nVerticals represent fatal outcomes for characters from fumbles they make or crits against them\n' + str(number_of_runs) + ' run(s) of ' +
                str(number_of_rounds) + ' rounds & ' + str(number_of_players) + ' player(s) | fatal fumble d100 >= ' + str(d100_fatal_fumble_cutoff) + ' (ideal odds/round ' +
                str(round (predicted_chance_fatal_fumble, 4)) + ')\n| fatal crit d100 >= ' + str(d100_fatal_crit_cutoff) +
                ' (ideal odds/round ' + str(round (predicted_chance_fatal_crit, 4)) + ') | total ideal fatal odds/round ' +
                str(round ((predicted_total_chance_fatal_outcome), 4)))
    plt.title(plot_title)
    plt.show()


if plot_poisson_stats:
    ######### Calculate poisson stats using a run as the measurement interval
    #######

    # Calculate expected number of fatal outcomes in a given run (event rate lambda)
    predicted_lambda_run = predicted_total_chance_fatal_outcome * number_of_rounds

    # Calculate relative frequencies in observed fatal outcomes per run
    print('Calculating relative frequencies in observed fatal outcomes per run...')
    max_value_poisson_observed_fatal_outcomes_per_run = max(poisson_observed_fatal_outcomes_per_run)
    observed_relative_frequencies_Y = scipy.stats.relfreq(poisson_observed_fatal_outcomes_per_run, numbins = (max_value_poisson_observed_fatal_outcomes_per_run + 1) )
    print('Raw outcomes per run:', poisson_observed_fatal_outcomes_per_run)
    print('Max value:', max_value_poisson_observed_fatal_outcomes_per_run)
    print('Observed relative frequencies', observed_relative_frequencies_Y.frequency)
    print('Observed relative frequencies sum to ', np.sum(observed_relative_frequencies_Y.frequency))

    # Set X axis with the correct range from observed frequencies
    plot_poisson_X = np.arange(max_value_poisson_observed_fatal_outcomes_per_run + 1)
    print('Plot X values: ', plot_poisson_X)

    # Calculate appropriate ideal poisson distribution
    predicted_poisson_probabilities_Y = scipy.stats.poisson.pmf(plot_poisson_X, predicted_lambda_run)

    predicted_plot_label, = plt.plot(plot_poisson_X, predicted_poisson_probabilities_Y, 'go--', linewidth=2, markersize=10, label='Predicted probability/run')
    observed_plot_label, = plt.plot(plot_poisson_X, observed_relative_frequencies_Y.frequency, color='r', marker='x', linestyle='dashed',
            linewidth=1, markersize=8, label='Observed probability/run')

    plt.title('Poisson distribution observed vs predicted fatal outcomes per run, ' + str(number_of_runs) + ' run(s) of ' +
        str(number_of_rounds) + ' rounds & ' + str(number_of_players) + ' player(s)\nfatal fumble d100 >= ' + str(d100_fatal_fumble_cutoff) + ' (ideal odds/round ' +
        str(round (predicted_chance_fatal_fumble, 4)) + ') | fatal crit d100 >= ' + str(d100_fatal_crit_cutoff) +
        ' (ideal odds/round ' + str(round (predicted_chance_fatal_crit, 4)) + ') | total ideal fatal odds/round ' +
        str(round ((predicted_total_chance_fatal_outcome), 4)) + '\nObserved probability per run in red, predicted probability per run in green | expected number per run $\lambda$=%i' % predicted_lambda_run)
    plt.xlabel('Number of fatal outcomes in given run')
    plt.ylabel('Probability of number of fatal outcomes in given run')
    plt.legend(handles=[predicted_plot_label, observed_plot_label])
    plt.show()
