# Academic Research
mloss.org - Machine Learning Open Source Software

## Sculley - Tech Debt in ML Systems
* "Developing and deploying ML is relatively fast and cheap, but maintaining them over time is difficult and expensive."
* "The tempting re-use or chaining of input signals may unintentionally couple otherwise disjoint systems."
* "calibration layers can lock in assumptions"
* Mitigating entanglement: where Changing Anything Changes Everything (CACE)
	- isolate models and serve ensembles
* Underutilized data dependencies (watch out for dependencies in general, too!) are input signals
that provide little incremental modeling benefit. Handle them w/ PCA. 
	- "can be detected via exhaustive leave-one-feature out evaluations, which should be run 
	regularly to identify and remove unnecessary ffeatures."
	- also consider: models should be logging and in those logs they should publish their 
	dependencies (shout it). Something needs to be listening for all the dependencies of all models
	in production so we can know how changes will cascade. 
* "Glue code" is what it takes to get data in & out of a general-purpose package, rather than doing
it by hand--a clean native solution
	- "wrap black-box packages into common APIs"
* Plain-Old-Data types: inputs/outputs as raw floats and integers lack important info. "A model 
parameter should know if it is a log-odds multiplier or a decision threshold, and a prediction
should know about the model that produced it & how it should be consumed."

## Sculley - Unit testing & Monitoring
* What to monitor? 
	- check predicted distributions vs. observed distributions of labels; kinda like a null model
	that predicts average|most common | random w/o input
	- "slicing prediction bias by various dimensions isolates issues quickly, and can be used for 
	automated alerting"
* Basic sanity checks on input data

Cultural "debt": not incentivizing the right behaviors. Reward these behaviors...
* deleting of features
* reduction of complexity
* improvements in reproducibility, stability, monitoring
...just as much as accuracy!

## Measuring tech/data debt
* How easily can an entirely new algorithmic approach be tested at full scale? 
* What is the transitive closure of all dependencies?
* How precisely can the impact of a new change to the system be measured? 
* Does improving one model or signal degrade others? 
* How quickly can new members of the team be brought up to speed? 
