# dnd-fatal-outcome-odds

Monte Carlo Simulation to statistically analyse and plot fatal outcomes over
time on fumble and crit homebrew rules in DnD. Poisson statistics are calculated
and plotted showing theoretical predicted vs actual observed probabilities.

Author: Geoff Moore

![cumulative](https://user-images.githubusercontent.com/37242207/37547879-2110662a-296c-11e8-8541-6d7b66ffa70a.png)

![poisson](https://user-images.githubusercontent.com/37242207/37547884-2897ebf2-296c-11e8-90f8-7aa125593b93.png)

My current DnD game involves homebrew rules with some fatal or character retiring
outcomes for fumbles and crits (we use the blanket term "fatal outcomes" in
the simulation but we also mean very serious or character-retiring outcomes). On
a fumble or crit, a d100 is rolled and the result checked against a fumble or crit
table which specifies the outcome. This program simulates this scenario using a
Monte Carlo approach and plots the cumulative occurrence of fatal outcomes over time
for each run (ie. for each iteration of the simulation). It also calculates
observed probabilities of fatal outcomes from the generated data for each run
which can be used to check the model against predicted ideal probabilities.

In the cumulative fatal outcomes plot, individual runs are plotted as different
colour lines and superimposed on the same figure for easy comparison. Verticals
in the plot represent fatal outcomes for player characters. The text console
output shows summary stats for each run by default and but full dice rolls can
also be displayed. (CAUTION: this is turned off by default to minimise execution
time. If changing this setting be careful not to run a large simulation or you may
find the program becomes unresponsive)

An ideal Poisson distribution is also calculated and plotted on a separate figure
for the given starting parameters. Observed probability of a given total fatal
outcome across multiple simulation runs is tracked and plotted in the same figure
to see how well observed probabilities compare with theoretical predictions.

This model uses a highly simplified version of combat. It does not attempt
to model creatures with multi-attack or similar skills. It also does not
take account of spells which would play a major role in real combat. For the
purposes of the simulation each round consists of:
- each player rolling one d20 to attack a monster. We
  track when a player fumbles their attack (ie. <= d20_fumble_cutoff)
  AND rolls a fatal outcome on the d100 (ie. >= d100_fatal_fumble_cutoff)
- the DM rolling one d20 to attack a player (we track when the DM gets a
  crit (ie. >= d20_crit_cutoff) AND the player rolls a fatal
  outcome on the d100 (ie. >= d100_fatal_crit_cutoff)

Starting parameters can be varied as follows:
- cutoffs for crits and fumbles on the d20 (must be between 1 and 20)
- fatal outcome cutoffs on the d100 (can be > 100 which means no fatal
    outcomes for that type of roll)
- the number of players
- the number of turns per run (a turn represents the DM and all players attacking once)
- the number of runs (number of iterations of the simulation)
- whether to display every roll or only show a summary for each run
- whether to display predicted vs observed Poisson statistics for probability of given
    number of fatal outcomes per run

NOTE: If options are set to plot both graphs (cumulative fatal outcomes per run AND
Poisson statistics), the first plot must be closed to display the second plot.

The interesting and counterintuitive aspect of the results from this simulation
is that, depending on starting parameters, unlikely events (ie. fatal outcomes) start
to creep into simulated dice rolls earlier and more regularly than our intuition might
suggest. This magnitude of this effect depends greatly on the starting parameters
(dice cutoffs, number of runs, number of rounds per run) and is driven by the underlying Poisson
statistics at work. For small values of lambda (expected number of fatal outcomes per
run) the Poisson distribution is narrow and located close to the origin. As lambda
increases (expected number of fatal outcomes per run increases) the Poisson distribution
becomes progressively broader with a long tail projecting to higher fatal outcomes. As a
consequence of the increasing width of the Poisson distribution, surprisingly high
numbers of fatal outcomes per run become possible. This means that care needs to be taken
in tuning the fatal outcome cutoffs to arrive at a satisfactory balance of risk versus
maintaining enjoyment for players.
