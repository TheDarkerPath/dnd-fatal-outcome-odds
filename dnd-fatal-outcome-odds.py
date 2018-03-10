import random
import sys, signal

# Code to allow graceful termintation
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# define number of turns over which to run the simulation
number_of_turns = 1000000

#initialise fumble and crit counters
d20_fumble_counter = 0
d20_crit_counter = 0
d100_fumble_fatal_outcome = 0
d100_crit_fatal_outcome = 0

# define cutoffs for crits and fumbles on the d20
d20_fumble_cutoff = 1
d20_crit_cutoff = 20

#define cutoffs for fatal or character-retiring outcomes on d100 following crit or fumble on d20
d100_fatal_fumble_cutoff = 98
d100_fatal_crit_cutoff = 98

# define functions to roll the dice
def rollD20():
    roll = random.randint(1,20)
    return roll

def rollD100():
    roll = random.randint(1,100)
    return roll

# Now, start a loop to run many iterations
loop_counter = 0
for loop_counter in range(0,number_of_turns):
    #roll the d20 and check the result
    D20result = rollD20()
    print(loop_counter, ' ', D20result)

    # If fumble, enter d20 fumble loop
    if D20result <= d20_fumble_cutoff:
        d20_fumble_counter += 1 # increment the d20_fumble_cutoff counter
        D100result = rollD100()
        print('   d20 Fumble!')
        print('   D100 roll--> ', D100result)

        # ... and enter the D100 check loop
        if D100result >= d100_fatal_fumble_cutoff:
            d100_fumble_fatal_outcome +=1 # increment the d20_fumble_fatal_outcome counter
            print('   FATAL d20 FUMBLE!-------------------------------')

    # If crit, enter d20 crit loop
    elif D20result >= d20_crit_cutoff:
        d20_crit_counter += 1 # increment the d20_crit_cutoff counter
        D100result = rollD100()
        print('   d20 Crit!')
        print('   D100 roll--> ', D100result)

        # ... and enter the D100 check loop
        if D100result >= d100_fatal_crit_cutoff:
            d100_crit_fatal_outcome +=1 # increment the d20_fumble_fatal_outcome counter
            print('   FATAL d20 CRIT!-------------------------------')

print('-------------------------------------')
print('Results: In', number_of_turns, 'turns')
print('-- % chance of fatal fumble is', 100 * d100_fumble_fatal_outcome / number_of_turns, '(abs number of fatal fumbles is', d100_fumble_fatal_outcome, ')')
print('-- % chance of fatal crit is', 100 * d100_crit_fatal_outcome / number_of_turns, '(abs number of fatal crits is', d100_crit_fatal_outcome, ')')
