# dnd-fatal-outcome-odds

Monte Carlo Simulation to plot fatal outcomes over time on fumble and crit
homebrew rules in DnD

Author: Geoff Moore

![fatal_outcomes_20_runs_of_2000_rounds_98_and_99_cutoffs](https://user-images.githubusercontent.com/37242207/37359464-8eca82c4-26e5-11e8-9c91-e2bfe7be33bb.png)

Monte Carlo Simulation of fatal outcomes on DnD dice rolls. My current game
involves homebrew rules with some fatal or character retiring outcomes
for fumbles and crits (we use the blanket term "fatal outcomes" in the simulation
but we also mean very serious or character-retiring outcomes). This program
simulates this scenario using a Monte Carlo approach and plots the cumulative
occurrence of fatal outcomes over time. It also calculates probabilities of
fatal outcomes from the generated data for each run which can be used to
check the model against predicted ideal probabilities.

Values can be varied as follows:
- cutoffs for crits and fumbles on the d20 (must be between 1 and 20)
- fatal outcome cutoffs on the d100 (can be > 100 which means no fatal
    outcomes for that type of roll)
- the number of players
- the number of turns per run
- the number of runs
- whether to display every roll or only show a summary for each run

For the purposes of the simulation we simplified each round to
consist of:
- each player rolling one d20 to attack a monster. We
  track when a player fumbles their attack (ie. <= d20_fumble_cutoff)
  AND rolls a fatal outcome on the d100 (ie. >= d100_fatal_fumble_cutoff)
- the DM rolling one d20 to attack a player (we track when the DM gets a
  crit (ie. >= d20_crit_cutoff) AND the player rolls a fatal
  outcome on the d100 (ie. >= d100_fatal_crit_cutoff)

Runs are plotted as different colour lines and superimposed on the same
axes for easy comparison. Verticals in the plot represent fatal outcomes
for player characters. The text console output shows summary stats for each run
by default and but full dice rolls can also be displayed. (CAUTION: this is
turned off by default to minimise execution time. If changing this setting
be careful not to run a large simulation or you may find the program
becomes unresponsive)

The interesting and counterintuitive aspect of the results from this simulation
is that unlikely events (ie. fatal outcomes) start to creep into simulated dice
rolls earlier and more regularly than our intuition might suggest
based solely on the predicted probabilities. This means that care needs to be
taken in tuning the fatal outcome cutoffs to arrive at a satisfactory balance of
risk versus maintaining enjoyment for players.
