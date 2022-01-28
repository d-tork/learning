# Data Science - Computerphile - Dr. Mike Pound

## Data Transformation

### Scaling data
Scale it around 0, with a standard deviation of 1. In r: 

```r
echonest <- music[,528:ncol(music)]
music.std <- as.data.frame(scale(echonest))
```

Codify nominal and ordinal variables (often text) so they are more amenable to things like decision
trees.

#### General approach
1. Create a new dataframe of just the numeric attributes
2. Normalize: move all our data between 0 and 1, per attribute
	1. "take away" (subtract) the minimum [from each point], so the minimum is now 0
	2. subtract min from max, and that becomes the max value (or 1 value)
	3. divide step 1 by step 2 to get a new value that is a "percent of maximum" (value between 0 
	and 1)
	4. in r: `normalise <- function(x){(x-min(x))/(max(x)-min(x))}`

Methods like PCA require _standardized_ data (not normalized), which is centered around 0, has a 
mean of 0, and a standard deviation of 1. The `scale` function in r does this for you (you don't 
have to write your own function like above).

```r
census.stand <- as.data.frame(scale(num_census))
```

### Joining datasets
i.e. joining US census data with Spanish census

* Be cognizant of conversions that need to take place (like EUR to USD) and _when_ they need to
occur (i.e. what was the exchange rate _when the census was taken_?)
* The distributions must be similar, e.g. the distribution of age in both the US and Spanish census
need to be approximately the same, otherwise the data will be skewed.
	- a good method is a stacked histogram
* Depending on what you want to do with your combined datasets, you should not rescale any data
before combining the sets. If you want to do the same analysis for all countries so you can compare
between them, of course, you can scale each set individually. But if you want to combine datasets
just to increase your sample size or achieve a better representation of, say, the global population
(without distinction based on country), you'll want to first combine all the datasets and then
do the rescaling. 

## Data Reduction
### Reducing dimensions

#### Correlation Analysis
If the correlation between two attributes is very strong (> 0.6, approximately), you may be able to
remove one of the attributes.

Pitch all the attributes vs. all the other attributes, look for high correlations, and decide
ourselves whether to remove them. 

```r
# Correlation analysis of features from echonst
cqt_k = select(music, contains("chroma_cqt_kurtosis"))
names(cqt_k) = c("kurt1", "kurt2", "kurt3", "kurt4", "kurt5")
cor_m = cor(cqt_k)
ggcorrplot(cor_m, hc.order = TRUE, type = "lower", lab = TRUE)+ggtitle("Correlations within Cens_Kurtosis")
```

#### Forward or Backward Attribute Selection
Maybe we have an ML model or clustering algorithm in mind, we can measure the performance of that, 
and then we can remove features and see if the performance remains the same. 

Train the model on a 720-dimension dataset, record the level of accuracy. Then remove one of the 
attributes and try it again (with 719 attributes). If the accuracy is the same, you can proceed
with the attribute permanently removed. If the accuracy plummets, you put the attribute back in and
remove a different one.

#### Forward Attribute Selection
Train the model on just one attribute, see what the accuracy is, and keep adding attributes and
retraining until our performance plateaus. 

In which order do you choose attributes? Usually randomly.

## Principal Component Analysis (PCA)
Trying to find a different view for our data in which we can separate it better. 

Orders the axes by most- to least-useful.

The ultimate goal is to find out which attributes are useful to our analysis and which aren't (and
should be discarded).

You're trying to find the direction through your data that maximizes the variance of the points (or
minimizes the error---the distance from each point to the line). Each principal component (line
drawn) is orthogonal (90º) to the previous axis. 

Scaling data properly is extremely important!

In r (prcomp function): it'll create a covariance matrix, and then use singular value decomposition
to find the eigenvectors and eigenvalues, and those are the things we actually want on PCA. 

```r
pca <- prcomp(music.std.scale=T)
```

What it's done is it has found the directions through our data which maximize the variance. And
it's projected our data into that space. In the result (the same number of dimensions as our 
original data), each PCA accounts for a certain amount of the variance (in %), but it's also
tracking the cumulative variance as you go further down the list. 

A common rule of thumb for data reduction (dropping attributes) is to find the PCA at which you
have 99% cumulative variance, and drop the rest.

## Clustering

Unsupervised: we don't have any labels

### K-means
Splits data into _k_ groups. Picks random points, assigns them to one of the groups. Then reevaluate 
the center points of each group, iteratively. 

Drawbacks: for an outlier (that you weren't expecting and didn't get rid of in cleaning), it's going to pull
the mean of a group towards itself. This can cause instability.

### Partitioning Around Medoids
Instead of calculating a mean for the cluster and moving those means around, it uses actual points
from the cluster. Then calculates the error for each cluster (from that random point). 

Avoids the issue of outliers.

### DBscan
Not a clustering method, but a way to help determine the number of clusters you expect to find. 

## Classification
Lets us pick one or the other, or some small number of labels for our data.

1. Create sets: training (70%), validation (15%), testing (15%)

### Baseline Algorithms
1. zero r: guess the most common answer, gives you a baseline accuracy
2. one r: pick one of our attributes, make a classification only based on that, then pick the best
of those attributes

### k-nearest neighbors (k-NN)
For a given new data point (unclassified), we take the majority vote/average of the nearest _k_
points. The output is: what, in the existing dataset, have we already seen nearby, and can we use
that to make a prediction. 

Choosing _k_ is difficult to do. With lots of dimensions and lots of observations, it tends to get
slow very quickly. 

### Decision Trees
e.g. J48, DecisionStump, HoeffdingTree, LMT, RandomForest, RandomTree, REPTree

Nice benefit that once we've created a decision tree, we can actually look at the rules and see how
a particular decision was made. 

Weka: a tool that makes applying things like decision trees very simple. 

### Support Vector Machine (SVM)
A little bit more common nowadays, a little bit more powerful than decision trees.

### F-score
Recall: for all the people that should have been granted credit, how many of them actually were? 
i.e. how good is our algorithm at spotting that class?

Precision: of the ones it spotted, what percentage of them were correct?

A good algorithm is one that has a very high precision and a very high recall. We combine these 
measures into one score: F<sub>1</sub>, or F-score, a value between 0 and 1. 

## Regression
When life doesn't fit into the neat categories of classification; trying to predict actual values.

### Linear Regression
Produces a linear equation that predicts output values. 

An Artificial Neural Network (ANN) is a type of linear regression technique. 

Measuring error: often mean error, but basically if you over-predict half the time and under-
predict half the time, you could potentially end up with 0 mean error, which is not accurate. 
Instead, using absolute error (if predicted is -x, just take the absolute value) or root mean
squared error.

R<sup>2</sup> is a measure of how tightly correlated our predictions (y^) and our actual (y) points were.

