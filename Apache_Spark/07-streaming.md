# Streaming data

## 4.3 Streaming Query
1. Declare the schema
2. Chain the reader and options together as a dataframe variable
3. Add transformations or filtering query
4. Write the stream back out

### Build streaming dataframe
```scala
val schema = "device STRING, ecommerce STRUCT<purchase_revenue_in_usd: DOUBLE, total_item_quantity: BIGINT, unique_items: BIGINT>, event_name STRING, event_previous_timestamp BIGINT, event_timestamp BIGINT, geo STRUCT<city: STRING, state: STRING>, items ARRAY<STRUCT<coupon: STRING, item_id: STRING, item_name: STRING, item_revenue_in_usd: DOUBLE, price_in_usd: DOUBLE, quantity: BIGINT>>, traffic_source STRING, user_first_touch_timestamp BIGINT, user_id STRING"

val df = spark.readStream
	.schema(schema)
	.option("maxFilesPerTrigger", 1)
	.parquet(eventsPath)

val emailTrafficDF = df.filter(col("traffic_source") === "email")
	.withColumn("mobile", col("device").isin("iOS", "Android"))
	.select("user_id", "event_timestamp", "mobile")
```

### Write streaming query results
```scala
import org.apache.spark.sql.streaming.Trigger

val checkPointPath = workingDir + "/email_traffic/checkpoint"
val outputPath = userhome + "/email_traffic/output"

val devicesQuery = emailTrafficDF.writeStream
	.outputMode("append")
	.format("parquet")
	.queryName("email_traffic_s")
	.trigger(Trigger.ProcessingTime("1 second"))
	.option("checkpointLocation", checkpointPath)
	.start(outputPath)

// ...
devicesQuery.stop()
```

### Listing and stopping active streams 
```scala
for (s <- spark.streams.active) {
	println(s.name)
	s.stop()
}
```

## 4.4 Aggregating Streams

### Windowing
```scala
streamingDF.groupBy(
	window($"time", "1 hour"),
	$"device"
).count()
```

**Performance consideration**: the `groupBy` shuffles among the partitions, and each partition must
maintain an in-memory state map in each window, in each partition. Reduce the number of partitions
to a 1-to-1 mapping of partitions to cores in order to improve performance.

### Watermarking
Defining a cutoff point after which structured streaming is allowed to throw saved windows away. 
Therefore late data can update aggregates of old windows as long as it's within the threshold.
```scala
streamingDF
	.withWatermark("time", "2 hours")
	.groupBy(
		window($"time", "1 hour"),
		$"device")
	.count()
```
