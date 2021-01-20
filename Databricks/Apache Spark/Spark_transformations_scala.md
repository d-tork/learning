# Spark Transformations (in Scala)

## 2.1 Aggregation
Importing built-in functions: `org.apache.spark.sql.functions._`

### Grouped Data Operations
| command          | description                                                                     |
| ---------------- | -----------                                                                     |
| `agg`            | Specify a series of aggregate columns                                           |
| `avg`            | Mean value for each numeric column for each group                               |
| `count`          | Number of rows for each group                                                   |
| `max`            | Max value for each numeric column for each group                                |
| `mean`           | Average value for each numeric column for each group                            |
| `min`            | Min value for each numeric column for each group                                |
| `pivot`          | Pivots a column of the current dataframe and performs the specified aggregation |
| `sum`            | Sum for each numeric column for each group                                      |

### Aggregate functions
| function                | description                                                        |
| ----------------        | -----------                                                        |
| `approx_count_distinct` | Returns the approximate number of distinct items in a group        |
| `avg`                   | Returns the average of the values in a group                       |
| `collect_list`          | Returns a list of objects with duplicates                          |
| `corr`                  | Returns the Pearson Correlation Coefficient for two columns        |
| `max`                   |                                                                    |
| `mean`                  |                                                                    |
| `stddev_samp`           | Returns the sample standard deviation of the expression in a group |
| `sumDistinct`           | Returns the sum of distinct values in the expression               |
| `var_pop`               | Returns the population variance of the values in a  group          |

### Math functions
| function         | description                                                                           |
| ---------------- | -----------                                                                           |
| `ceil`           | Computes the ceiling of the given column                                              |
| `log`            | Computes the natural logarithm of the given value                                     |
| `round`          | Returns the value of the column e rounded to 0 decimal places with HALF_UP round mode |
| `sqrt`           | Computes the square root of the specified float value                                 |

### GroupBy examples

```scala
val eventCountsDF = df.groupBy("event_name").count()

val avgStatePurchasesDF = df.groupBy("geo.state").avg("ecommerce.purchase_revenue_in_usd")
```

Aggregate functions
```scala
import org.apache.spark.sql.functions.sum

val statePurchasesDF = df.groupBy("geo.state").agg(sum("ecommerce.total_item_quantity").alias("total_purchases"))
```

```scala
import org.apache.spark.sql.functions.{avg, approx_count_distinct}

val stateAggregatesDF = df.groupBy("geo.state").agg(
	avg("ecommerce.total_item_quantity").alias("avg_quantity"),
	approx_count_distinct("user_id").alias("distinct_users"))
```
