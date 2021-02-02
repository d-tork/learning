# Apache Spark Programming

## Good resources
* https://sparkbyexamples.com

## 1.2 Databricks Platform

### Creating tables from data in dbfs
```sql
CREATE TABLE IF NOT EXISTS events USING parquet OPTIONS (path "/mnt/training/ecommerce/events/events.parquet");
```

## 1.3 Spark SQL
### Using scala to execute SQL

With SQL
```scala
val budgetDF = spark.sql("""
SELECT name, price
FROM products
WHERE price < 200
ORDER BY price
""")
```

With DataFrame API
```scala
val budgetDF = spark.table("products")
	.select("name", "price")
	.where("price < 200")
	.orderBy("price")

budgetDF.show()  	// in spark-shell
display(budgetDF)  	// table format for Databricks notebook
```

### Convert between dataframes and SQL
```scala
# SparkDF --> SQL view
budgetDF.createOrReplaceTempView("budget")

# SQL view --> spark df
val budgetDF = spark.sql("SELECT * FROM budget")
```

## 1.4 Reader & Writer
### Read from CSV
```scala
val usersCsvPath = "/mnt/training/ecommerce/users/users-500k.csv"
val usersDF = spark.read
	.option("sep", "\t")
	.option("header", true)
	.option("inferSchema", true)
	.csv(usersCsvPath)

usersDF.printSchema()
```

### Read from JSON
```scala
val eventsJsonPath = "/mnt/training/ecommerce/events/events-500k.json"
val eventsDF = spark.read
	.option("inferSchema", true)
	.json(eventsJsonPath)

eventsDF.printSchema()
```

### Read from multiple paths
```scala
val folder_path = List("folder_1","folder_2","folder_x")
val rawDF = sqlContext.read.parquet(folder_path: _*)

//With regex (untested)
val inputpath = "/root/path/todir/2015{0[1-6]}[0-3]*"
val rawDF = spark.read.csv(inputpath)
```

**Note**: you can read data faster by creating the schema yourself with a `StructType` (perhaps
80% faster)

## Common Spark DF commands

| command            | description                        |
| ----------------   | -----------                        |
| `df.show()`        | print text representation of table |
| `df.printSchema()` | print columns and datatypes        |
| `df.count()`       | number of rows                     |
| `df.take(n)`       | stick _n_ rows into an Array       |

# Misc.
## Creating an RDD
```scala
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
```

## Working with RDDs
There are two things you can do with an rdd: [transformations and actions](https://spark.apache.org/docs/2.1.0/programming-guide.html#transformations). 

## Dataframes vs RDDs
from https://blog.knoldus.com/difference-between-rdd-df-and-ds-in-spark/

DataFrames are an abstraction which gives a view of the data with a schema (column names and type info).

```scala
case class Person(name : String, age:Int)

// Create spark session object
import org.apache.spark.sql.SparkSession
val spark = SparkSession
.builder()
.appName("Spark SQL basic example")
.config("spark.some.config.option", "some-value")
.getOrCreate()

//Convert RDD to dataframe
import spark.implicits._

val df = List(Person("shubham",21),Person("rahul",23)).toDF
df.show()
```

## Column Operators and Methods
https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Column.html

| operator/method            | description                                                                 |
| ---------------            | -----------                                                                 |
| `&&, \|\|`                 | Boolean AND, OR                                                             |
| `\*, +, <, >=`             | Math and comparison operators                                               |
| `===, =!=`                 | Equality and inequality tests                                               |
| `alias, as`                | Gives the column an alias (**as** only in Scala)                            |
| `cast`                     | Casts the column to a different data type                                   |
| `isNull, isNotNull, isNan` | Is null                                                                     |
| `asc, desc`                | Returns a sort expression based on ascending/descending order of the column |
| `startsWith, endsWith`     | String starts/ends with "..."                                               |
| `isInCollection`           | Test column value for membership in iterable                                |
| `contains`                 | Test column value for containing a given other (simple strings only)        |

## DataFrame Transformation Methods

| method                     | description                                                                                        |
| ---------------            | -----------                                                                                        |
| `select`                   | Returns a new DataFrame by computing given expression for each element                             |
| `drop`                     | Returns a new DataFrame with a column dropped                                                      |
| `withColumnRenamed`        | Returns a new DataFrame with a column renamed                                                      |
| `withColumn`               | Returns a new DataFrame by adding a column or replacing the existing column that has the same name |
| `filter, where`            | Filters rows using the given condition                                                             |
| `sort, orderBy`            | Returns a new DataFrame sorted by the given expressions                                            |
| `dropDuplicates, distinct` | Returns a new DataFrame with duplicate rows removed                                                |
| `limit`                    | Returns a new DataFrame by taking the first n rows                                                 |
| `groupBy`                  | Groups the DataFrame using the specified columns, so we can run aggregation on them                |

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

### Filtering rows
```scala
val purchasesDF = eventsDF.filter("ecommerce.total_item_quantity > 0")

val androidDF = eventsDF.filter((col("traffic_source") =!= "direct") && (col("device") === "Android"))

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

## Empty function
Need to force Spark to execute an action on data, but don't care what it is? 
```scala
df.foreach(x => ())
```

## Create a really big dataframe
Union it to itself
```scala
sc.setJobDescription("Step X: Create a really big dataframe")

var bigDF = initialDF

for (i <- 0 to 6) {
	bigDF = bigDF.union(bigDF).reparition(sc.defaultParallelsim)
}

bigDF.foreach(_=>())
```
