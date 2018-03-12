# dnd-fatal-outcome-odds

Monte Carlo Simulation to plot fatal outcomes over time on fumble and crit
homebrew rules in DnD

Author: Geoff Moore

![fatal_outcomes_20runs_98cutoffs](https://user-images.githubusercontent.com/37242207/37288154-6bb5ec02-25fe-11e8-9a09-550cc03e377c.png)

Monte Carlo Simulation of fatal outcomes on DnD dice rolls. My current game
involves homebrew rules with some fatal or character retiring outcomes
for fumbles and crits. This program simulates this scenario and plots the
cumulative occurrence of fatal outcomes over time. It also calculates
probabilities of fatal outcomes from the generated data which can be used
to check the model against actual probabilities.

Values for cutoffs for crits and fumbles on the d20 and fatal outcomes
on the d100 can be varied. You can also vary the number of turns per run,
and the number of runs. Runs are plotted as different colour lines and
plotted on the same axes for easy comparison.

The counterintuitive aspect of the results from this simulation are that
unlikely events (ie. fatal outcomes) start to creep into actual dice rolls
much earlier and more regularly than our intuition would suggest based
solely on the mathematical predicted probabilities. This means that much
care needs to be taken in tuning the fatal outcome cutoffs to arrive at a
satisfactory balance of risk versus maintaining enjoyment for players.

