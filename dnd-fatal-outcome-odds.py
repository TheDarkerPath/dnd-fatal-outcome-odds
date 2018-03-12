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
import matplotlib
import matplotlib.pyplot as plt

# Code to allow graceful termintation
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#################################################################################################
# Change values below to play with cutoffs for crits and fumbles on the d20 and fatal outcomes on the d100
#
#################################################################################################
# define cutoffs for crits and fumbles on the d20
d20_fumble_cutoff = 1
d20_crit_cutoff = 20

#define cutoffs for fatal or character-retiring outcomes on d100 following crit or fumble on d20
d100_fatal_fumble_cutoff = 98
d100_fatal_crit_cutoff = 98

# define number of turns over which to run the simulation
number_of_turns = 10000

#define number of runs
number_of_runs = 20
#################################################################################################
#################################################################################################

# define functions to roll the dice
def rollD20():
    roll = random.randint(1,20)
    return roll

def rollD100():
    roll = random.randint(1,100)
    return roll

##########################################
# Start run loop
run_loop_counter = 0
for run_loop_counter in range(0,number_of_runs):

    #initialise fumble and crit counters
    d20_fumble_counter = 0
    d20_crit_counter = 0
    d100_fumble_fatal_outcome = 0
    d100_crit_fatal_outcome = 0

    # define variables to track and pyplot
    plot_turn_number_X = []
    plot_total_number_of_fatal_outcomes_Y = []

    # Get OS-generated random number as seed
    random_data = os.urandom(4)
    seed = int.from_bytes(random_data, byteorder="big")
    random.seed(seed)

    ###################################################################
    # Now, start the main loop to run many iterations of the simulation
    loop_counter = 0
    for loop_counter in range(0,number_of_turns):
        #roll the d20 and check the result
        D20result = rollD20()
    #    print(loop_counter, ' ', D20result)

        # If fumble, enter d20 fumble loop
        if D20result <= d20_fumble_cutoff:
            d20_fumble_counter += 1 # increment the d20_fumble_cutoff counter
            D100result = rollD100()
    #        print('   d20 Fumble!')
    #        print('   D100 roll--> ', D100result)

            # ... and enter the D100 check loop
            if D100result >= d100_fatal_fumble_cutoff:
                d100_fumble_fatal_outcome +=1 # increment the d20_fumble_fatal_outcome counter
    #            print('   FATAL d20 FUMBLE!-------------------------------')

        # If crit, enter d20 crit loop
        elif D20result >= d20_crit_cutoff:
            d20_crit_counter += 1 # increment the d20_crit_cutoff counter
            D100result = rollD100()
    #        print('   d20 Crit!')
    #        print('   D100 roll--> ', D100result)

            # ... and enter the D100 check loop
            if D100result >= d100_fatal_crit_cutoff:
                d100_crit_fatal_outcome +=1 # increment the d20_fumble_fatal_outcome counter
    #            print('   FATAL d20 CRIT!-------------------------------')
        # Append values for plotting
        plot_turn_number_X.append(loop_counter)
        plot_total_number_of_fatal_outcomes_Y.append(d100_fumble_fatal_outcome + d100_crit_fatal_outcome)

    ################################################################################
    #Calculate mathematical odds for later comparison with stats from generated data
    predicted_chance_fatal_fumble = (d20_fumble_cutoff / 20) * ( (101 - d100_fatal_fumble_cutoff ) / 100 )
    predicted_chance_fatal_crit =  ( (21 - d20_crit_cutoff ) / 20 ) * ( (101 - d100_fatal_crit_cutoff ) / 100 )

    #########################################
    # Calculate and print stats for whole run
    chance_fatal_fumble = d100_fumble_fatal_outcome / number_of_turns
    chance_fatal_crit = d100_crit_fatal_outcome / number_of_turns
    print('\n-------------------------------------')
    print('Run number', run_loop_counter)
    print('  Results: In', number_of_turns, 'turns')
    print('  -- chance of fatal fumble per turn from generated data is roughly 1 / ', round (1 / chance_fatal_fumble, 0), '(abs number of fatal fumbles is', d100_fumble_fatal_outcome, ')')
    print('  -----> prediced mathematical odds for this are roughly 1 / ', round (1 / predicted_chance_fatal_fumble, 0) )
    print('  -- chance of fatal crit per turn generated data is roughly 1 / ', round (1 / chance_fatal_crit, 0), '(abs number of fatal crits is', d100_crit_fatal_outcome, ')')
    print('  -----> predicted mathematical odds for this are roughly 1 / ', round (1 / predicted_chance_fatal_crit, 0) )
    print('  -- TOTAL chance of fatal crit per turn generated data is roughly 1 /', round (1 / (chance_fatal_fumble + chance_fatal_crit), 0), '(abs number of fatal crits is', d100_fumble_fatal_outcome + d100_crit_fatal_outcome, ')')
    print('  -----> predicted mathematical odds for this are roughly 1 / ', round (1 / (predicted_chance_fatal_fumble + predicted_chance_fatal_crit), 0) )

    ########################################################
    # Plot total number of fatal outcomes versus turn number
    plt.plot(plot_turn_number_X,plot_total_number_of_fatal_outcomes_Y)
# End run loop

plt.ylabel('Running total of fatal outcomes')
plt.xlabel('No of turns taken')
plot_title = str(number_of_runs) + ' run(s) of ' + str(number_of_turns) + ' turns | fumble cutoff ' + str(d100_fatal_fumble_cutoff) + ' | crit cutoff ' + str(d100_fatal_crit_cutoff)
plt.title(plot_title)
plt.show()
