# From _Algorithms to Live By_

## The optimal stopping problem
How much time do you dedicate to defining a baseline (looking at houses, circling a parking lot, looking for a mate) before switching to a mode of 'comit immediately to the one that meets your criteria'? 

Answer: 37%

* look before you leap
* popularly, "the secretary problem"

## Explore vs. Exploit
* favorite restaurant or a new one; recipes, menu ordering, music listening; reach out to new friend to develop or old friend for familiarity
* in computer science, it's embodied in the multi-arm bandit problem: pulling the arms on various slot machines and favoring the most promising ones
* nothing matters as much as **the interval over which we enjoy a thing**. Seize the day because you'll die shortly, but seize the lifetime (i.e. start learning an instrument) because you'll live longer than you think.
* the value of exploration can only go down over time, as the remaining opportunities to savor it dwindle
* value of exploitation goes up over time
* Win-Stay, Lose-Shift: choose an arm at random, keep pulling as long as it pays off

## The Gittins Index
* originally for drug trials
* "discounting": valuing the present more highly than future
* Deal or No Deal: offering contestants money (a bribe) to _not_ open a briefcase
* "dynamic allocation index": a guaranteed payout rate which, if offered in lieu of pulling the slot machine arm, will make us content to never pull its handle again.
* it is a pre-calculated matrix of scores per number of wins vs. number of losses (for a single "arm"), often discounting the future at 90% the value of the present

## the grass is always greener
The unknown has a chance of being better, and exploration has value.

## Regret Minimization Framework
Upper confience bound algorithm: pick the option (slot machine) for which the top of the confidence interval is highest

## A/B testing

## Sorting
### Big O Notation
| notation         | name             | metaphor                       |
|------------------|------------------|--------------------------------|
| O(1)             | constant time    | clean for the party            |
| O(n)             | linear time      | pass around the roast          |
| O(n<sup>2</sup>) | quadratic time   | each new guest hugs all others |
| O(2<sup>n</sup>  | exponential time | work doubles for each guest    |
| O(n!)            | factorial time   | hell                           |

* Bubble sort: scan and look for out-of-order pairs
* Insertion sort: pull everything off the shelf and put them back in order
* Merge sort: sort stacks of items separately, then when you merge stacks simply compare the two top (one from each stack) and move the smaller to the new stack. This worked in "linearithmic " time
* Bucket sort: pre-group into sorted categories with no regard for finer, intracategory sorting. (me: so it's like Spark's Z-ordering?)

Tradeoff between sorting and searching: sometimes searching a messy group is faster.

Sports: single elimination tournaments, round-robin, ladder tournaments; noise from imperfect outcomes. Comparison counting sort.

Races are better than fights, they are cardinal rather than ordinal outcomes.

## Caching
LRU (least recently used). Consider hardware performance *and* distances. Random Eviction, FIFO, or LRU. What you've used recently is a _great_ approximation of what you'll use in the future. 

Noguchi Filing System: left-insertion rule (or "top of the pile")
