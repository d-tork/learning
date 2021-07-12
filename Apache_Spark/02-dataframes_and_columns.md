# Spark DataFrames and Columns

## Column Operators and Methods
https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Column.html

| operator/method            | description                                                                 | example                              |
| ---------------            | -----------                                                                 | -------                              |
| `&&, \|\|`                 | Boolean AND, OR                                                             |                                      |
| `\*, +, <, >=`             | Math and comparison operators                                               |                                      |
| `===, =!=`                 | Equality and inequality tests                                               |                                      |
| `alias, as`                | Gives the column an alias (**as** only in Scala)                            |                                      |
| `cast`                     | Casts the column to a different data type                                   |                                      |
| `isNull, isNotNull, isNan` | Is null                                                                     | `.filter($"items.coupon".isNotNull)` |
| `asc, desc`                | Returns a sort expression based on ascending/descending order of the column |                                      |
| `startsWith, endsWith`     | String starts/ends with "..."                                               |                                      |
| `isInCollection`           | Test column value for membership in iterable                                |                                      |
| `contains`                 | Test column value for containing a given other (simple strings only)        |                                      |

## DataFrame Transformation Methods

| method                     | description                                                                                        | example                    |
| ---------------            | -----------                                                                                        | -------                    |
| `select`                   | Returns a new DataFrame by computing given expression for each element                             |                            |
| `drop`                     | Returns a new DataFrame with a column dropped                                                      |                            |
| `withColumnRenamed`        | Returns a new DataFrame with a column renamed                                                      |                            |
| `withColumn`               | Returns a new DataFrame by adding a column or replacing the existing column that has the same name |                            |
| `filter, where`            | Filters rows using the given condition                                                             |                            |
| `sort, orderBy`            | Returns a new DataFrame sorted by the given expressions                                            | `df.sort($"colname".desc)` |
| `dropDuplicates, distinct` | Returns a new DataFrame with duplicate rows removed                                                |                            |
| `limit`                    | Returns a new DataFrame by taking the first n rows                                                 |                            |
| `groupBy`                  | Groups the DataFrame using the specified columns, so we can run aggregation on them                |                            |

## DataFrame Action Methods

| method              | description                                               |
| ---------------     | -----------                                               |
| `show`              | Displays the top n rows of DataFrame in a tabular form    |
| `count`             | Returns the number of rows in the DataFrame               |
| `describe, summary` | Computes basic statistics for numeric and string columns  |
| `first`             | Returns the first row                                     |
| `head`              | Returns the first n rows                                  |
| `collect`           | Returns an array that contains all rows in this DataFrame |
| `take`              | Returns an array of the first n rows in the DataFrame     |

### Subselecting and aliasing columns
```scala
import org.apache.spark.sql.functions.col

val locationsDF = eventsDF.select(col("user_id"),
	col("geo.city").alias("city"),
	col("geo.state").alias("state"))
```

### Dropping columns
```scala
val anonymousDF = eventsDF.drop("user_id", "geo", "device")
```

### Add or replace columns
```scala
val mobileDF = eventsDF.withColumn("mobile", col("device").isin("iOS", "Android"))
```

### Reordering columns (manually or alphabetically)
```scala
val manualColumns = Seq("zulu", "yankee", "x_ray").map(str => col(str))
df.select(manualColumns:_*)

val alphaCols = df.columns.sorted.map(str => col(str))
df.select(alphaCols:_*)
```

## Filtering
### Filtering rows
```scala
val purchasesDF = eventsDF.filter("ecommerce.total_item_quantity > 0")

val androidDF = eventsDF.filter((col("traffic_source") =!= "direct") && (col("device") === "Android"))
val android = eventsDF.where("device = 'Android'")

// with varargs
val items = Seq("item1", "item2")
val filtered = df.filter($"col".isin(items:_*))  //or
val filtered = df.filter($"col".isInCollection(items))
```

### Filtering strings (handling case-sensitivity)
```scala
// Convert the column values
df.filter(lower(df.col("vendor")).equalTo("fortinet"))  //or
df.filter(upper(df.col("vendor")).equalTo("FORTINET"))

df.where(lower($"vendor") === "fortinet")

// use rlike
df.where($"vendor".rlike("(?i)^fortinet$"))  //where (?i) is case-insensitive flag
```

### More regex `rlike` filtering
Just remember to double escape `\\` any regex characters you want to actually match (or use `Pattern.quote()`)
```scala
// Constructing a pipe-delimited OR filter
val animals = List("cat", "dog")
df.withColumn(
  "contains_cat_or_dog", col("phrase").rlike(animals.mkString("|"))
)
```

### Regex string pattern notes
```scala
val pattern = raw"[A-Z]{4}-[A-Z]{2}-\w+"  	//a string (raw prefix)
val pattern = """[A-Z]{4}-[A-Z]{2}-\w+"""  	//a string (triple quotes)
val pattern = "[A-Z]{4}-[A-Z]{2}-\\w+"  	//a string (escaped \w)
val pattern = "[A-Z]{4}-[A-Z]{2}-\w+".r		//ERROR invalid escape character \w
val pattern = "[A-Z]{4}-[A-Z]{2}-\w+"		//ERROR invalid escape character \w
val pattern = """[A-Z]{4}-[A-Z]{2}-\w+""".r  	//a Regex (triple quotes)
val pattern = "[A-Z]{4}-[A-Z]{2}-\\w+".r  	//a Regex (escaped \w)
```

## Duplicates and Sorting
### Drop duplicates with subset of cols
```scala
val distinctUsersDF = eventsDF.dropDuplicates(Seq("user_id"))
```

### Sorting
```scala
val increaseTimestampDF = eventsDF.sort("event_timestamp")

val decreaseTimestampDF = eventsDF.sort(col("event_timestamp").desc)

val increaseSessionsDF = eventsDF.orderBy("user_first_touch_timestamp", "event_timestamp")
```

## Splitting a string column
https://stackoverflow.com/questions/44750844/how-to-split-column-to-two-different-columns

Solving:
```
splitting year_artist with 

+--------------------+-----+
|         year_artist|count|
+--------------------+-----+
|    1945_Dick Haymes|    5|
|1949_Ivory Joe Hu...|    1|
|     1955_Tex Ritter|    1|
```

```scala
import org.apache.spark.sql.functions.regexp_extract

df.select(
	regexp_extract($"year_artist", "^(\\d{4})_(.*)", 1).alias("year"),
	regexp_extract($"year_artist", "^(\\d{4})_(.*)", 2).alias("artist")
)
```

Edmond's version
```scala
val regexp_pattern = "(.*?)\\{(.*?)\\}(.*?)\\{(.*?)\\}(.*?\\{(.*?)\\}"
val df = df_raw.withColumn("brand",regexp_extract($"file", regexp_pattern,1)).
			    withColumn("brand_hash",regexp_extract($"file", regexp_pattern,2)).
			    withColumn("model",regexp_extract($"file", regexp_pattern,3)).
			    withColumn("model_hash",regexp_extract($"file", regexp_pattern,4)).
			    withColumn("serial",regexp_extract($"file", regexp_pattern,5)).
			    withColumn("serial_hash",regexp_extract($"file", regexp_pattern,6)).
```
