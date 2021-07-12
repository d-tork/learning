# Spark/Scala Data Ingest

## Reading by file type (in practice)

| format  | example                                             |
|---------|-----------------------------------------------------|
| csv     | `spark.read.option("sep", ",").csv("path/to/file")` |
| json    | `spark.read.json("path/to/file")`                   |
| parquet | `spark.read.parquet("path/to/file")`                |
| delta   | `spark.read.format("delta").load("path/to/file")`   |
| xml     |                                                     |

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
80% faster):

to match the schema (the result of `usersDF.printSchema()`)
```
root
  |-- user_id: string(nullable = true)
  |-- user_first_touch_timestamp: long (nullable = true)
  |-- email: string (nullable = true)
```

create it with
```scala
import org.apache.spark.sql.types{LongType, StringType, StructType, StructField}

val userDefinedSchema = StructType(Seq(
	StructField("user_id", StringType, true),
	StructField("user_first_touch_timestamp", LongType, true),
	StructField("email", StringType, true)
))
```

and use it with
```scala
val usersDF = spark.read
	.option("sep", "\t")
	.option("header", true)
	.schema(userDefinedSchema)
	.csv(usersCsvPath)
```

Alternatively, define the schema with a DDL formatted string
```scala
val DDLSchema = "user_id string, user_first_touch_timestamp long, email string"
val usersDF = spark.read
	.option("sep", "\t")
	.option("header", true)
	.schema(DDLSchema)
	.csv(usersCsvPath)
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

# Writing to storage or tables

## Convert data to Delta table
```scala
val deltaPath = workingDir + "/delta-events"
eventsDF.write.format("delta").mode("overwrite").save(deltaPath)
```

## Create Delta table in the metastore
```scala
eventsDF.write.format("delta").mode("overwrite").saveAsTable("delta_events")
```

## Time travel with Delta Lake
(this command uses spark.sql in order to do string substitution with `deltaPath`)
```scala
spark.sql(f"CREATE TABLE train_delta using DELTA LOCATION '$deltaPath'")
```

This command gives the overwrite histories of that `deltaPath`
```sql
DESCRIBE HISTORY train_delta
```

Access a different version of the history:
```scala
val df = spark.read.format("delta").option("versionAsOf", 0).load(deltaPath)
```

In order to `vacuum` (clean up) old commit histories, create a `DeltaTable` variable first:
```scala
import io.delta.tables._

val deltaTable = DeltaTable.forPath(spark, deltaPath)
deltaTable.vacuum(0)
```
