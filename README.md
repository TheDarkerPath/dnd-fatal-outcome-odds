# dnd-fatal-outcome-odds

Monte Carlo Simulation to plot fatal outcomes over time on fumble and crit
homebrew rules in DnD

Author: Geoff Moore

![fatal_outcomes_20runs_2000turns_98cutoffs](https://user-images.githubusercontent.com/37242207/37293305-cf374828-260a-11e8-979a-ce743902fb1d.png)

Monte Carlo Simulation of fatal outcomes on DnD dice rolls. My current game
involves homebrew rules with some fatal or character retiring outcomes
for fumbles and crits. This program simulates this scenario and plots the
cumulative occurrence of fatal outcomes over time. It also calculates
probabilities of fatal outcomes from the generated data which can be used
to check the model against ideal mathematical probabilities.

Values for cutoffs for crits and fumbles on the d20 and fatal outcomes
on the d100 can be varied. The number of turns per run and the number of
runs can also be adjusted. Runs are plotted as different colour lines and
superimposed on the same axes for easy comparison. Verticals in the plot
represent fatal outcomes. The text console output shows summary details
for each run by default and can be tweaked to display each and every dice
roll if desired. This is turned off by default to minimise execution time.

The counterintuitive aspect of the results from this simulation are that
unlikely events (ie. fatal outcomes) start to creep into actual dice rolls 
earlier and more regularly between runs than our intuition would suggest based
solely on the predicted probabilities. This means that care needs to be taken
in tuning the fatal outcome cutoffs to arrive at a satisfactory balance of
risk versus maintaining enjoyment for players.
