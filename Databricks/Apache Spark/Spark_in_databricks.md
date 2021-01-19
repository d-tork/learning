# Apache Spark Programming

## 1.2 Databricks Platform

### Creating tables from data in dbfs
```sql
CREATE TABLE IF NOT EXISTS events USING parquet OPTIONS (path "/mnt/training/ecommerce/events/events.parquet");
```

## 1.3 Spark SQL
### Using scala to execute SQL

With SQL
```
val budgetDF = spark.sql("""
SELECT name, price
FROM products
WHERE price < 200
ORDER BY price
""")
```

With DataFrame API
```
val budgetDF = spark.table("products")
	.select("name", "price")
	.where("price < 200")
	.orderBy("price")

budgetDF.show()  	# in spark-shell
display(budgetDF)  	# table format for Databricks notebook
```

### Convert between dataframes and SQL
```
# SparkDF --> SQL view
budgetDF.createOrReplaceTempView("budget")

# SQL view --> spark df
val budgetDF = spark.sql("SELECT * FROM budget")
```

## 1.4 Reader & Writer
### Read from CSV
```
val usersCsvPath = "/mnt/training/ecommerce/users/users-500k.csv"
val usersDF = spark.read
	.option("sep", "\t")
	.option("header", true)
	.option("inferSchema", true)
	.csv(usersCsvPath)

usersDF.printSchema()
```

### Read from JSON
```
val eventsJsonPath = "/mnt/training/ecommerce/events/events-500k.json"
val eventsDF = spark.read
	.option("inferSchema", true)
	.json(eventsJsonPath)

eventsDF.printSchema()
```

## Common Spark DF commands

| command            | description                        |
| ----------------   | -----------                        |
| `df.show()`        | print text representation of table |
| `df.printSchema()` | print columns and datatypes        |
| `df.count()`       | number of rows                     |
| `df.take(n)`       | stick _n_ rows into an Array       |

# Misc.
## Creating an RDD
```
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
```

## Working with RDDs
There are two things you can do with an rdd: [transformations and actions](https://spark.apache.org/docs/2.1.0/programming-guide.html#transformations). 

## Dataframes vs RDDs
from https://blog.knoldus.com/difference-between-rdd-df-and-ds-in-spark/

DataFrames are an abstraction which gives a view of the data with a schema (column names and type info).

```
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

```
import org.apache.spark.sql.functions.regexp_extract

df.select(
	regexp_extract($"year_artist", "^(\\d{4})_(.*)", 1).alias("year"),
	regexp_extract($"year_artist", "^(\\d{4})_(.*)", 2).alias("artist")
)
```
