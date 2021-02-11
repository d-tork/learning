# Spark Transformations (in Scala)

## 2.1 Aggregation
Importing built-in functions: `org.apache.spark.sql.functions._`

See [this StackOverflow answer](https://stackoverflow.com/questions/45131481/how-to-use-collect-set-and-collect-list-functions-in-windowed-aggregation-in-spa) for using `Window.partitionBy`

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

## 2.2 [Datetimes](https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html)
Based on the [Java DateTimeFormatter](https://docs.oracle.com/javase/10/docs/api/java/time/format/DateTimeFormatter.html)

### Built-in functions
| function         | description                                                                                          |
| ---------------- | -----------                                                                                          |
| `date_format`    | Converts a date/timestamp/string to a value of string in the format specified by the second argument |
| `add_months`     | Returns the date that is numMonths after startDate                                                   |
| `date_add`       | Returns the date that is the given number of days after startDate                                    |
| `from_unixtime`  | Converts unixtime (seconds) to a string timestamp                                                    |
| `minute`\*       | Extracts minutes as an integer from a given date/timestamp/string                                    |
| `dayofweek`      | Extracts the day of the month as an integer from a given date/timestamp/string                       |
| `unix_timestamp` | Converts timestring with given pattern to Unix timestamp (in seconds)                                |

\* Extraction methods exist for `year`, `month`, `second`, etc.

### Patterns
| symbol     | meaning                    | examples               |
| ---------- | -----------                | --------               |
| `G`        | era                        | AD; Anno Domini        |
| `y`        | year                       | 2020; 20               |
| `D`        | day-of-year                | 189                    |
| `M/L`      | month-of-year              | 7; 07; Jul; July       |
| `d`        | day-of-month               | 28                     |
| `Q/q`      | quarter-of-year            | 3; 03; Q3; 3rd quarter |
| `E`        | day-of-week                | Tue; Tuesday           |
| `F`        | week-of-month              | 3                      |
| `a`        | am-pm-of-day               | PM                     |
| `h`        | clock-hour-of-am-pm (1-12) | 12                     |

### Getting a timestamp from a string
```scala
val datetimeDF = df.withColumn("ts", (col("ts") / 1e6).cast("timestamp"))
	.withColumn("date", to_date(col("ts")))  // bonus, just the date column
```

### Format existing timestamp as other format
```scala
import org.apache.spark.sql.functions.date_format

val formattedDF = timestampDF.withColumn("date_string", date_format(col("timestamp"), "MMM dd, yyyy"))
	.withColumn("time_string", date_format(col("timestamp), "HH:mm:ss.SSSSSS"))
```

## 2.3 Complex Types

### String functions
| function         | description                                                                     |
| ---------------- | -----------                                                                     |
| `translate`      | Translate any character in the src by a character in replaceString              |
| `regexp_replace` | Replace all substrings of the specified string value that match regexp with rep |
| `regexp_extract` | Extract a specific group matched by a regex, from the specified string column   |
| `lower`          | Converts a string column to lowercase                                           |
| `split`          | Splits str around matches of the given pattern                                  |

### Collection functions
| function         | description                                                                                  |
| ---------------- | -----------                                                                                  |
| `array_contains` | Returns null if the array is null, true if the array contains value, and false otherwise     |
| `explode`        | Creates a new row for each element in the given array or map column                          |
| `slice`          | Returns an array containing all the elements in x from index start with the specified length |

### Filter for item in array
```scala
import org.apache.spark.sql.functions._

val mattressDF = detailsDF.filter(array_contains(col("details"), "Mattress"))
```

Pick out items from an array
```scala
val mattressDF = mattressDF.withColumn("size", element_at(col("details"), 2))
						   .withColumn("quality", element_at(col("details"), 1))
```

### Union two dataframes
```scala
val unionDF = mattressDF.unionByName(pillowDF)
	.drop("details")
```

## 2.4 Joins

**Note**: to access DataFrameNaFunctions like `drop`, `fill`, `replace`, you must use `.na` as the
accessor on the dataframe object. 

Drop duplicates from a selected column and add a dummy column
```scala
val convertedUsersDF = salesDF
	.select(col("email"))
	.dropDuplicates(Seq("email"))
	.withColumn("converted", lit("True"))
```

Two ways to "drop duplicates"
```scala
df.select("email").dropDuplicates(Seq("email"))
df.select("email").distinct()
```

Two ways to join on a column
```scala
usersDF.join(convertedUsersDF, usersDF("email") === convertedUsersDF("email"))
usersDF.join(convertedUsersDF, Seq("email"), "outer")
```
HOWEVER&mdash;the first one (based on online documentation) introduces _two_ 'email' columns, and
trying to work with email later introduces an ambiguous reference to 'email', so I went with the 
Dataframe lesson answer.

## 2.5 User-Defined Functions
1. define a local function
2. define a UDF which applies the local function to a column
3. register UDF in the SQL namespace

```scala
//Local function
def firstLetterFunction (email: String): String = {
	email(0).toString
}
firstLetterFunction("annagray@kaufman.com")

//UDF
val firstLetterUDF = udf(firstLetterFunction _)

import org.apache.spark.sql.functions.col
salesDF.select(firstLetterUDF(col("email")))

//register it
spark.udf.register("sql_udf", firstLetterFunction _)

//use it
salesDF.createOrReplaceTempView("sales")
```
```sql
SELECT sql_udf(email) AS firstLetter FROM sales
```


