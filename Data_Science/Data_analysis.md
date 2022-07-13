# Data science overall
## Types of problems
classification | regression | clustering | dimensionality reduction

## Families of models
| family               | algorithms                   |
|----------------------|------------------------------|
| Regression           | linear                       |
|                      | logistic - fast, explainable |
|                      | OLSR                         |
| Clustering           | k-means                      |
|                      | k-medians                    |
| Instance-based       | k-Nearest neighbor           |
| Dimensionality redux | PCA                          |
|                      | PLSR                         |
|                      | PCR                          |
| Ensemble             | Random forest                |
|                      | Gradient boosting            |
|                      | Boosting                     |

Random forest and gradient boosting algorithms are slow but accurate. 

# Advice from a Medium article on Data Analysis

* too many software engineers apply machine learning tools without a thorough understanding of the statistical theories behind them

## Books to read
* _Intro to Statistical Learning_, Hastie, Tibshirani, Witten, James
* _Doing Bayesian Data Analysis_, Kruschke
* _Time Series Analysis and Applications_, Shumway, Stoffer

## 10 Techniques we must know: 
1. Linear regression
2. Classification
3. Resampling methods
4. Subset selection
5. Shrinkage
6. Dimension reduction
7. Nonlinear models
8. Tree-based methods
9. Support Vector Machines
10. Unsupervised learning

# Scaling Data
## When to use feature scaling
In gradient-descent-based algorithms: linear regression, logistic regression, neural network, etc.
Having features on a similar scale can help the gradient descent converge more quickly towards the
minima.

In distance-based algorithms: KNN, K-means, SVM, SVR. Higher weightings would be given to features
with higher magnitude, if we don't scale them. 

:x: _Not_ in tree-based algorithms, they're insensitive to the scale of the features because they 
are only splitting a node on a single feature, independent of the others.

## Normalization (Min-Max scaler)
Values are shifted and rescaled so they end up ranging between 0 and 1. 

$$ X^ \prime = \dfrac{X-X_{min}}{X_{max}-X_{min}}$$

Good when you know your data doesn't follow a Gaussian distribution (KNN, neural networks don't
assume a distribution).

## Standardization
Values are centered around the mean with a unit standard deviation. The mean of
the attribute becomes 0 and resultant distribution has a unit standard 
deviation. 

$$ X^ \prime = \dfrac{X-\mu}{\sigma}$$

Helpful when data follows Gaussian distributions. Outliers will not be affected. **Note:** don't 
standardize one-hot encoded categorical features! Numeric features only.

:eight_spoked_asterisk: Fit your model to raw, normalized, and standardized
ddata and compare performance.

:eight_spoked_asterisk: Fit the scaler on the training data and use it to transform testing data,
to avoid data leakage. Scaling of target values generally not required.

# Math and Numbers
Hardin: 
> "Numeracy" means more than measuring and counting... many major discoveries were made with very little measuring and counting. The attitude science requires of its practitioners is respect, bording on reverence, for ration, proportions, and rates of change. 

# Data Mining literature
workbook slides from Witten, Frank, Hall)

> In processing loan applications, **a simple statistical method covers 90% of cases.** Borderline cases are referred to loan officers, but 50% of accepted cases default. This is where ML is used.

A grossly oversimplified historical difference:
* statistics = testing hypotheses
* machine learning = finding the right hypothesis
