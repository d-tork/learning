# Spark Optimization in Scala

## Caching
Insert a `cache` step in your staging to force a cache (otherwise, shuffling can occur 
automatically).

### Best practices
* Don't cache unless you're sure a DataFrame will be used multiple times 
* Omit unneeded columns to reduce the storage footprint
* After calling `.cache()`, ensure all partitions are accessed with fast action (e.g. `count`)
* Evict DataFrame from cache when no longer needed

### Simple process
```scala
// Read and select
val df = spark.read
	.option("inferSchema", true)
	.json(eventsJsonPath)

// Perform transformation and action
df.orderBy("event_timestamp").count()

// Cache it
df.cache()
```

**Note**: a call to `cache()` does not immediately materialize the data in cache. An action must
be executed for Spark to actually cache the data, even if it's an empty function.

#### Empty function
```scala
df.foreach(x => ())
```

Remove cache when you're done
```scala
df.unpersist()
```

### Cache table for RDD name
```scala
df.createOrReplaceTempView("Pageviews_DF_Scala")
spark.catalog.cacheTable("Pageviews_DF_Scala")
df.count()
```

## Optimization
**Don't do this**
```scala
val limitEventsDF = df
  .filter(col("event_name") =!= "reviews")
  .filter(col("event_name") =!= "checkout")
  .filter(col("event_name") =!= "register")
  .filter(col("event_name") =!= "email_coupon")
  .filter(col("event_name") =!= "cc_info")
  .filter(col("event_name") =!= "delivery")
  .filter(col("event_name") =!= "shipping_info")
  .filter(col("event_name") =!= "press")
```

**Instead, do this**
```scala
val betterDF = df.filter( 
  (col("event_name").isNotNull) &&
  (col("event_name") =!= "reviews") &&
  (col("event_name") =!= "checkout") && 
  (col("event_name") =!= "register") && 
  (col("event_name") =!= "email_coupon") && 
  (col("event_name") =!= "cc_info") && 
  (col("event_name") =!= "delivery") && 
  (col("event_name") =!= "shipping_info") && 
  (col("event_name") =!= "press")
)
```

## Partitioning
| method          | description                                                             |
| --------------- | -----------                                                             |
| `coalesce()`    | Returns new DF w/ exactly N partitions when N < current # partitions    |
| `repartition()` | Returns new DF w/ exactly N partitions (but slower, requires shuffling) |

### Guidelines
* Always err on the side of too many small partitions, rather than too few large partitions
* But try not to let partition size increase above 200MB per 8GB of slot total memory
