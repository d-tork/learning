Partner Readiness Assessment: Apache Spark Programming on Databricks
=====================================================================
Read _Spark: The Definitive Guide_ by Chambers & Zaharia (O'Reilly). Sections I, II, and IV

Course Welcome - Databricks Overview
------------------------------------
* Can you describe the Databricks ecosystem?
    - Data Science Workspace (MLflow and BI integrations)
    - Unified Data Service (Spark and Delta Lake)
    - Enterprise Cloud Service (AWS or Azure)
* Can you describe the components of the Unified Data Analytics Platform?
    - an online environment where data practitioners can collaborate on data science projects and
    workflows
* Can you explain the foundational concepts behind Apache Spark?
    - distributed computing on distributed datasets, where a dataflow engine handles the entire
    workflow as one job instead of frequent materialization of intermediate states such as in 
    MapReduce
* The course "Apache Spark Programming on Databricks" makes use of the BedBricks case study - are 
    - a store that sells mattresses, pillows, etc.
you familiar with the case study used in this course?
* The course "Apache Spark Programming on Databricks" makes use of the custom content in the form 
of Notebooks, distributed as a DBC file - have you imported the DBC file containing the notebooks 
referenced by this course?
    - It can be done by uploading the .dbc file or pointing to its URL.

Course Welcome - The Databricks Platform
----------------------------------------
* Can you describe the components of the Databricks Workspace?
    - organizes objects (notebooks, libraries, experiments) into folders, provides access to data,
    and provides access to clusters and jobs (under "compute")
    - can be managed by 1) Databricks UI, 2) CLI, 3) REST API
* Can you apply the notebook utilities to execute code in multiple languages and markdown?
    - The notebook defines a default language for all cells, but each cell's language can be 
    overwritten by adding at the top either `%sql`, `%python`, `%scala`, or `%md`.
* Can you access the Databricks File System (DBFS) and create tables from files?
    ```scala
    // scala

    val inputPath = "dbfs:/path/to/file.parquet"
    val df = spark.read.parquet(inputPath)

    val deltaPath = "dbfs:/path/to/delta"
    df.write.format("delta").mode("overwrite").save(deltaPath)
    df.write.format("delta").mode("overwrite").saveAsTable("delta_events")
    spark.sql(f"CREATE TABLE train_delta USING DELTA LOCATION '$deltaPath'"
    ```

    The point of DBFS is to mount your object storage there (S3, Azure, etc.) so you can skip over
    the credentials and whatnot, and also be able to interact with it using directory and file
    semantics. 

* Can you use Databricks notebooks to execute SQL queries and visualize results?
    - prefix the cell with the magic command `%sql`, or else use `spark.sql("SELECT * FROM TABLE")`
* Can you configure and use widgets to parameterize a notebook?
    ```sql
    -- sql

    CREATE WIDGET TEXT state DEFAULT "CA"

    SELECT *
    FROM events
    WHERE geo.state = getArgument("state")
    ```

DataFrames - Spark Interfaces
-----------------------------
* Can you describe the core interfaces to Apache Spark's (SQL, DataFrames, Datasets)
* Can you describe what a DataFrame is?
    - an abstraction which gives a view of the data with a schema
* Can you describe what a DataFrame Schema is?
    - provides column names and datatype info for each column
* Can you describe what a DataFrame Transformation is?
    - performs some operation on the dataframe, creating a new one
* Can you describe what a DataFrame Action is?
    - perform some operation and return a result as a single value, instead of a new DF/RDD
* Can you describe what a SparkSession is?
    - a connection to the cluster and a namespace in which jobs, tasks, and actions are run
    - a reference to the Spark Application currently running on your cluster
* Can you describe the Spark execution model including what is and isn't eagerly or lazily executed?
* Do you know how to navigate the Spark docs for including API docs for Java, Scala, Python, and R?
    - https://spark.apache.org/docs/latest
* Can you demonstrate how DataFrames are created and evaluated in Spark?

DataFrames - Readers & Writers
------------------------------
* Can you provide multiple examples of what type of data sources can be used by Apache Spark
    - csv, json, parquet, xml; they come from HDFS, DBFS, S3
* Can you employ a DataFrameReader to read data from tables, CSV, JSON, Delta, and Parquet files?
    ```scala
    // scala

    val df = spark.read.option("sep", ",").option("header", true).csv("path/to/file")
    val df = spark.read.json("path/to/file")
    val df = spark.read.format("delta").load("path/to/file")
    val df = spark.read.parquet("path/to/file")
    ```
* Can you employ a DataFrameWriter to write data to tables, CSV, JSON, Delta, and Parquet files?
    ```scala
    // scala

    df.write.format("delta").mode("overwrite").saveAsTable("table_name")
    df.coalesce(1).write.format("csv").mode("overwrite").option("header", "true").save("path"
    // json
    df.write.format("delta").mode("overwrite").save("path/to/file")
    df.write.option("compression", "snappy").mode("overwrite").parquet("path/to/file")
    ```
* Can you describe how inferring a DataFrame's schema affects performance?
    - it can be 80% faster to declare the schema beforehand and pass it to the reader
* Can you create a DataFrame while employing a StructType schema?
    ```scala
    // scala

    import org.apache.spark.sql.types{LongType, StringType, StructType, StructField}

    val userDefinedSchema = StructType(Seq(
        StructField("user_id", StringType, true),
        StructField("user_first_touch_timestamp", LongType, true),
        StructField("email", StringType, true),

    val df = spark.read
        .option("header", true)
        .schema(userDefinedSchema)
        .csv("path/to/file")
    ```
* Can you create a DataFrame while employing a DDL formatted schema?
    ```scala
    // scala

    val DDLSchema = "user_id string, user_first_touch_timestamp long, email string"
    val df = spark.read
        .option("header", true)
        .schema(DDLSchema)
        .csv("path/to/file")
    ```

DataFrames - Columns & Rows
---------------------------
* Can you create and employ a Column object for use with DataFrame Transformations and Actions?
    ```scala
    // scala

    df.withColumn("new_column", $"old_column".cast("timestamp"))

    df.select($"old_column".cast("timestamp").alias("new_column"))
    ```
* Can you apply column operators and methods to construct expressions?
* Can you apply DataFrame transformations to subset, add, and replace columns?
* Can you apply DataFrame transformations to subset, add sort rows?
* Can you employ methods of a Row object in both Scala and Python?

Transformations - Aggregation
-----------------------------
* Can you describe the groupBy operation and grouped data object?
* Can you apply group data methods to aggregate data?
* Can you apply math and aggregate built-in functions to process data?

Transformations - Datetime
--------------------------
* Can you convert between multiple representations of times, dates, timestamps, and strings?
* Can you use Datetime Patterns to format and parse strings?
* Can you extract values from datetime objects such as the month of the year or hour of the day?

Transformations - Complex Types
-------------------------------
* Can you identify the various string and collection functions used to manipulate DataFrames?
* Can you apply string and collection functions to transform data

Transformations - Additional Functions
--------------------------------------
* Can you identify additional non-aggregate functions?
* Can you identify functions from the DataFrameNaFunctions submodule?
* Can you employ non-aggregate and NA functions to process and join data?

Transformations - User-Defined Functions
----------------------------------------
* Can you describe what a User-Defined Function is?
* Can you articulate the performance drawbacks of User-Defined Functions?
* Can you describe what a vectorized UDF is (sometimes referred to as a Panda UDF)?
    - a user-defined function that can be applied to a Pandas structure (DF or series) row-wise. 
* Can you create and apply a UDF?
    ```scala
    // scala

    // create local function
    def firstLetterFunction (email: String): String = {
        email(0).toString
    }

    // wrap function in UDF
    val firstLetterUDF = udf(firstLetterFunction _)
    ```

* Can you register a UDF for use in Spark SQL?
    ```scala
    // scala

    spark.udf.register("sql_udf", firstLetterFunction _)

    // apply to data
    salesDF.createOrReplaceTempView("sales")
    spark.sql("""SELECT sql_udf(email) AS newcol FROM sales""")
    ```

Spark Optimization - Spark Architecture
---------------------------------------
* Can you identify the components of a Spark cluster?
    - a group of nodes, comprised of a single driver node and multiple executors. In Databricks, 
    each node has only one executor (but YARN may run two executors on the same node). Each node
    has shared resources (RAM, disk, network). Each executor has slots/threads/cores to which a 
    task can be assigned.
* What is the difference between a Spark driver and Spark executor?
* Can you identify the components of a Spark job?
    - a job is the instructions, and consists of one or more stages. A stage consists of one or 
    more tasks. A task is the single unit of work against a single partition.
* Can you describe Apache Spark's model for distributed computing?
    - a driver node splits up a dataset and tasks among multiple executor nodes and then collects 
    the results of the tasks at the end of each stage. If a node is too slow on a task, the driver
    can cancel it and give the task to another node.
* Can you illustrate for someone else how Apache Spark executes a single-stage job such as 
filtering?
    - the work of removing the unwanted rows (or keeping the desired ones) is split up among nodes
* Can you illustrate for someone else how Apache Spark executes a multi-stage job such as counting 
records?
    - each node counts values within its own partition, then writes the output of the local count
    to disk. In the second stage, a single executor is nominated to combine the local counts into
    a global count, as a single task.
* Can you illustrate for someone else how Apache Spark employs a shuffle operation to map & reduce 
data between multiple stages of a spark job in a multi-stage job such as producing a distinct set 
of records?
    - in the first stage, executors pick out the distinct values in their partitions and write
    them to disk. In the second stage, executors responsible for one or more distinct values will
    collect up only the values they are responsible for by reading from the disk of the other 
    executors. Finally, when like values are consolidated onto single executors, they are reduced
    to a single value and then all are sent to the driver.

Spark Optimization - Shuffles & Caching
---------------------------------------
* Can you describe the difference between wide and narrow transformations and their effect on 
Spark's execution and performance?
    - wide requires multiple stages, and narrow can be done in a single stage. The most expensive
    part of a transformation is the shuffling that occurrs between stages (writing and reading 
    to disk, for example).
    - wide examples: repartition, join, sort, groupby, wide, cross join
    - narrow examples: select, coalesce, sample, map, filter, union
* Can you describe how Spark uses shuffle files and caching to skip operations?
* Can you apply DataFrame methods to cache and uncache DataFrames?
* Can you describe the various best practices around caching?
* Describe the advantages and disadvantages of caching data at various storage levels.
* What causes data to shuffle?

Spark Optimization - Query Optimization
---------------------------------------
* Can you describe each stage of a spark query?
* Can you define what Adaptive Query Execution (AQE) is?
* Can you demonstrate for someone else a logical optimization?
* Can you demonstrate for someone else a predicate pushdown?
 
Spark Optimization - Spark UI
-----------------------------
* Can you navigate the execution details of a spark query through the Spark UI?
* Can you plot the execution timeline of a spark query through the Spark UI?
* Can you identify and describe all the metrics of a spark job presented through the Spark UI?
* Can you interpret the query diagram presented through the Spark UI?

Spark Optimization - Partitioning
---------------------------------
* Can you describe the relationship between cores, spark-partitions, and disk-partitions as it 
relates to writing data?
* Do you know what the key differences are between the repartition and coalesce transformations?
* Can you demonstrate for someone else how to use the repartition and coalesce transformations?
* Can you configure the default shuffle partitions to control the number of partitions created 
after a shuffle operation?
* Can you describe for someone else the best practices around managing spark-partitions?
    - one practice is to partition streaming data on the ingest date, and alias that column
    as 'p_ingestdate' so people know how it's partitioned by just looking at the schema
* Can you describe for someone else the difference between a spark-partition and a disk-partition?

Structured Streaming - Streaming Query
--------------------------------------
* Can you describe the processes for streaming data?
* Can you identify the different configuration options specific to reading a streaming query?
* Can you execute a streaming query?
* Can you monitor a streaming query?

Structured Streaming - Processing Streams
-----------------------------------------
* Can you read data from a stream?
    ```python
    # python

    display(spark.readStream.table('health_tracker_plus_silver'), streamName='display_silver')

    # where health_tracker_plus_silver is a table registered in the Metastore
    ```
    _Note: `streamName` seems to be an optional parameter to the `display()` function. What happens
    if I specify a streamname with a static dataframe?_
* Can you apply basic transformations to a stream?
* Can you identify which operations are available to a static DataFrame vs a Streaming DataFrame?
    - major difference is
    ```python
    # python

    staticDF.write.save('path') 
    # versus
    streamDF.writeStream.start('path')
    ```
* Can you execute a streaming query using the Databricks proprietary display() function and plot 
the results within a notebook?
* Can you execute a streaming query using a DataStreamWriter?
    > while you _can_ write directly to tables using the `.table()` notation, this will create
    > fully managed tables by writing output to a default location on DBFS. This is not a best 
    > practice and should be avoided in nearly all cases.

    - When writing a stream back after processing, specify a `checkpointLocation` option so that if
    the streaming job stops for some reason and you restart it, it will continue from where it left
    off. 
    - Also, every streaming job should have its own checkpoint directory: **no sharing**
* Can you enumerate all the active streams?
    ```python
    # python

    for stream in spark.streams.active:
        print(stream.name)
    ```
* Can you stop one and only one stream given a collection of active streams?
    ```python
    # python

    from pyspark.sql.session import SparkSession

    def stop_named_stream(spark: SparkSession, namedStream: str) -> bool:
        stopped = False
        for stream in spark.streams.active:
            if stream.name == namedStream:
                stream.stop()
                stopped = True
        return stopped
    ```


Structured Streaming - Aggregating Streams
------------------------------------------
* Can you describe aggregation and windowing concepts?
* Can you configure a stream to aggregate a stream of data by a moving window?
* Can you adjust the default shuffle partitions as they pertain to the unique requirements of a 
stream?

Structured Streaming - Delta Lake
---------------------------------
* Can you describe the core components of Delta Lake?
    - Data files (parquet, in object storage, accessed by DBFS)
    - Transaction log (all transactions done on the table, stored as JSON, single source of truth)
    - Metastore registration (query plan for retrieving from object storage)
* Can you describe what the Delta transaction log is and how it works?
    - It's a log of all the operations that took place to bring a Delta table to its current state. 
    - These operations break down into one or more of these steps:
    ```
    Add file
    Remove file
    Update metadata
    Set transaction
    Change protocol
    Commit info
    ```
* Can you use Delta's history and versioning features to work with an older version of a dataset 
given a specific point in history?
    ```sql
    -- sql

    DESCRIBE HISTORY health_tracker_plus_bronze;  -- as long as it's been registered in Metastore

    SELECT * FROM events TIMESTAMP AS OF timestamp_expression;
    SELECT * FROM events VERSION AS OF version;

    /* Where timestamp_expression can be a string cast to a timestamp, explicit timestamp, date 
    string, or more complex time/date expressions */
    ```
    `Version` can be obtained from the output of `DESCRIBE HISTORY`, or with Python:
    ```python
    # python

    from delta.tables import DeltaTable

    bronzeTable = deltaTable.forPath(spark, bronzePath)
    display(bronzeTable.history())
    ```

    **Time traveling with Python API**
    ```python
    # python

    df1 = (
        spark.read.format('delta')
        .option('timestampAsOf', timestamp_string)
        .load('/mnt/delta/events')
    df2 = (
        spark.read.format('delta')
        .option('versionAsOf', version)
        .load('/mnt/delta/events')

    # - or -
    spark.read.format("delta").load("/mnt/delta/events@20190101000000000")
    spark.read.format("delta").load("/mnt/delta/events@v123")
    ```

Additional Exam Prep
====================
Basics
------
* Cluster architecture: nodes, drivers, workers, executors, slots, etc.
    - Worker nodes are the nodes of a cluster that perform computations.
    - An executor is a JVM running on a worker node.
    - What happens to the Spark application if the driver shuts down?
    - If spark is running in cluster mode, there is a single worker node that contains the Spark
    driver and the executors.
* Spark execution hierarchy: applications, jobs, stages, tasks, etc.
    - applications > jobs > tasks > stages
* Shuffling
    - when data needs to move between executors (i.e. for wide transformations)
* Partitioning
* Lazy evaluation
    - refers to the idea that Spark waits until the last moment to execute a series of operations.
    Builds up a plan of transformations to apply to data, and only executed when you call an action.
* Transformations vs. actions
    - Transformations (lazy) modify a DataFrame, but are not completed when you execute the code
        - e.g. `select`, `distinct`, `groupBy`, `sum`
    - Actions (eager) compute a result and are completed as soon as you execute the code
        - e.g. `show`, `count`, `collect`, `save`
* Narrow vs. wide transformations
    - Narrow: data required to compute the records in a single partition reside in at most one 
    partition of the parent dataset; work can be computed and reported back to the executor without
    changing the way data is partitioned over the system
    - Wide: data required to compute the records in a single partition may reside in many partitions
    of the parent dataset; require that data be redistributed over the system (shuffled)

Spark architecture application
------------------------------
Apply knowledge of the following to make optimal decisions. How do they affect a Spark session? 
How can they be used to improve performance?
* Execution deployment modes
* Stability
* Garbage collection
    - Describe garbage collection strategies in Spark: 
* Out-of-memory errors
* Storage levels
* Repartitioning
* Coalescing
* Broadcasting
* DataFrames

DataFrame API basics
--------------------
Be intimately familiar with applying all of these:
* Subsetting (select, filter)
* Column manipulation (casting, creating columns, manipulating existing columns, complex column 
types)
    - Cast a column from a numeric type to a string type
    - Create a new DataFrame by mathematically combining two existing columns
* String manipulation (splitting strings, regular expressions)
    - Split a string column into two columns based on a regular expression
* Performance-based operations (repartitioning, shuffle partitions, caching)
    - Cache a DataFrame to a specific storage level
* Combining DataFrames (joins, broadcasting, unions)
* Reading/writing DataFrames (schemas, overwriting)
* Working with dates (extraction, formatting)
    - Extract the month from a DataFrame column of date type
* Aggregations
* Miscellaneous (sorting, missing values, typed UDFs, value extraction, sampling)
    - Create a UDF to use in a Spark SQL statement


Intro to Apache Spark
=====================

Course sections and what concept they represent
1. Filtering: distributed computing
    - splitting the work (of removing brown candies) amongst all the students in a classroom
2. Counting: stages
    - local count, where students count their own candies, then a global count, where local counts 
    are summed
    - the intermediate results (local counts) of the first stage are written to disk
    - a single executor is nominated to combine the local counts (it's a single task)
3. Distinct: The Shuffle
    - local distinct, global distinct
    - distinct values from the local distinct stage get consolidated, through the network, to a
    single slot/thread per color. In stage 2, executors fetch their distinct values from the other
    executors.
    - Then each executor has all the distinct data values from the others, and it does a reduce
    to get the truly distinct values. 
    - Finally, executors return their sets to the driver.

Keep wide transformations together, and narrow with narrow. Changing back and forth between them
is expensive.

Optimization strategies
-----------------------
* broadcast hash joins: reduce shuffling (google it)
    - Shuffle hash join: most basic type; data from each side of the join is shuffled into 
    partitions by key, but no sort is required. Can be used with large tables, but they ust be 
    monitored for data skew
    - Shuffle sort merge join: used with data of any size, requires that data be shuffled and 
    sorted
    - Broadcast hash join: requires that one side of the join is small enough to be broadcast. No
    shuffle or sort required because it makes data available to each executor. Very fast.
    - Shuffle nested loop: (aka Cartesian Product Join) does not shuffle; instead, does an 
    all-pairs comparison between all join keys of each executor. Useful for very small workloads
* bucketing: avoids the exchange operation by pre-sorting the data on disk
    - only works when you're in the terabyte range

Databricks Platform
===================

Run filesystem commands on DBFS
```
%fs ls

%fs head /databricks-datasets/README.md
```
DBFS commands are basically unix commands, except that `mkdirs` is plural and it's `unmount` 
instead of `umount`. For a list of commands at any time, run `%fs help`

Types of tables
---------------

| Managed                          | Unmanaged                                            |
| -------------------------------- | ---------------------------------------------------- |
| registered in Metastore          | registered in Metastore                              |
| stored in default location       | stored in the path you specify                       |
| `DROP TABLE` will delete both    | `DROP TABLE` will only affect Metastore              |
| `df.write.saveAsTable('events')` | `df.write.save('/path/to/events')`                   |
|  `CREATE TABLE events`           | `CREATE TABLE events LOCATION '/path/to/events'`[^1] |

[^1]: Alternatively, `CREATE TABLE events OPTIONS (path "/path/to/events")`

When in doubt, you can tell if a table is managed or not by running:

```sql
-- sql

DESCRIBE TABLE EXTENDED events

-- or, without schema info:
SHOW TABLE EXTENDED LIKE 'events';
DESCRIBE DETAIL events;
```
* If you want to see `Type: MANAGED` or `Type: EXTERNAL`, you must use the second syntax
(`SHOW TABLE EXTENDED LIKE`)

### Global tables
* `df.write.saveAsTable('events')`
* registered in Hive Metastore, available across all clusters

### Local tables
* `df.createOrReplaceTempView('events')`
* a.k.a. temporary view, only on your cluster and not in the Metastore

### Inspecting tables in python
A useful snippet:
```python
# python
for table in spark.catalog.listTables():
    print(table)
```
```
Table(name='derog_population', database='into_derog', description=None, tableType='EXTERNAL', isTemporary=False)
Table(name='foreign_gpe_lkp_raw', database='into_derog', description=None, tableType='EXTERNAL', isTemporary=False)
Table(name='full_population', database='into_derog', description=None, tableType='EXTERNAL', isTemporary=False)
Table(name='nonderog_population', database='into_derog', description=None, tableType='EXTERNAL', isTemporary=False)
```


Create SQL tables from files in DBFS
--------------------------------------
```sql
-- sql

CREATE TABLE IF NOT EXISTS users USING parquet OPTIONS (path "/mnt/training/ecommerce/users/users.parquet");
```
* this is an _unmanaged table_, i.e. dropping it will not affect the underlying file
* alternatively, ...`USING parquet LOCATION '/mnt/training/ecommerce/users/users.parquet'`

Create dataframe from SQL table
-------------------------------
```scala
// scala

val usersDF = spark.table("users")
```

Create SQL table/view from existing Spark Dataframe
---------------------------------------------------
```scala
// scala

usersDF.createOrReplaceTempView("users")
```
* this is a _temporary view_ or _local table_, and is not in the Hive Metastore

Writing dataframes to files
---------------------------
```scala
// scala

val usersOutputPath = workingDir + "/users.parquet"

usersDF.write
    .option("compression", "snappy")
    .mode("overwrite")
    .parquet(usersOutputPath)
```

Create and use a database
-------------------------
To avoid contention with commonly named tables in others' workspaces
```scala
// scala

val db_name = "user_db"
spark.sql(f"CREATE DATABASE IF NOT EXISTS '$db_name'")
spark.sql(f"USE '$db_name'")
```

Convert to Delta table and add to metastore
-------------------------------------------
taken from learning/01-ingest
```scala
// scala

val deltaPath = workingDir + "/delta-events"
eventsDF.write.format("delta").mode("overwrite").save(deltaPath)

eventsDF.write.format("delta").mode("overwrite").saveAsTable("delta_events")
```
* :question: does this ^ line create a _second_ copy of the data, now as a managed table? 
* or does it simply register the table in the Metastore, like executing the SQL:
	- `CREATE TABLE delta_events USING delta LOCATION /working/dir/delta-events`
* in other words, can I combine `option('path', '/path/to/events')` with `saveAsTable()` in
the same line in order to skip using an additional SQL command (in order to create as unmanaged)?
    - it appears that, yes, these accomplish the same thing
    - **however:** I tried this again and got `org.apache.hadoop.hive.ql.metadata.HiveException: Unable to alter table.`
    - a better approach might be to first `df.write.save('path')` to change the underlying files,
    then simply `REFRESH TABLE <tablename>` (as recommended by the databricks docs)

An alternative to overwrite + SQL refresh:
```python
# python
(df.write.format('delta')
    .mode('overwrite')
    .option('overwriteSchema', 'true')
    .option('path', '<your-table-path>')  # for a managed table, leave this one out)
    .partitionBy('your-partition-columns')
    .saveAsTable('<your-table>')
)
```

Partition with unique values in a given column
```scala
// scala

val stateEventsDF = eventsDF.withColumn("state", $"geo.state")
stateEventsDF.write.format("delta").mode("overwrite").partitionBy("state").option("overwriteSchema", "true").save(deltaPath)
```

Registering a Delta table (that we created in object storage) in the Metastore as a table allows us 
to query it using SQL.
```python
# python

spark.sql("""DROP TABLE IF EXISTS health_tracker_plus_bronze""")

spark.sql(
    f"""
CREATE TABLE health_tracker_plus_bronze
USING DELTA
LOCATION "{bronzePath}"
"""
)
```

Tip for easily working in unmanaged tables
------------------------------------------
via James Carbonaro. To make your life easier, run
```python
# python

spark.sql("CREATE DATABASE dtorkelson location '/path/to/my/tables-root'")
```
Then, if at the top of your notebook you set the default database (`USE dtorkelson`), you can just
use `df.write.format('delta').saveAsTable(tablename)` and your tables will always be written to 
the expected location. (Confirmed, and if it's the first time you are writing it, the Delta file
will be named the same as your table).
* :warning: This creates a **managed table**, even though it is saved to a specific path in your
object storage! It follows that dropping the table will delete the files. 
* If you want to modify that table later, go through the standard steps of overwriting the file
with `mode('overwrite').save('path/to/delta')` followed by SQL `REFRESH tablename`

Lakehouse
=========
* What is Databricks Lakehouse?
    - single platform to unify ingest, analytics, and AI. Combines popular functionality of data 
    lakes and warehouses.
* What are the origins of the Lakehouse data management paradigm?
    - Orgs/businesses were having to piece together solutions for big data, different technology
    stacks.
* How do most enterprises struggle with data?
    - Tech stacks are proprietary, incompatible. They fail at consolidated security.
* For each practitioner role, what are the popular components of Lakehouse?
    - Data engineers: Delta Lake offers management and governance
    - Data analysts: SQL-native interface for querying
    - Data scientists: workspace, model pipeline

Data lakes (like HDFS) support _any_ kind of data: CSV, JSON, videos, free text, images

Data Ingestion Pipeline
=======================
* **EDSS**: Enterprise Decision Support Systems
    - see the course _Fundamentals of Delta lake_
    - used in OLAP, for making data-driven business decisions
    - should be a Silver Delta table, and is the single source of truth
* **ODS**: Operational Data Store
    - a transactional database which records all measurements from a raw data collector (like 
    health trackers)
* Delta Lake is _not_ used for building transactional databases

Unit Tests and Verification
===========================

Verify file ingestion
---------------------
```python
# python

rawPath = 'dbfs:/some/folder/to/raw/data'
file_2020_1 = 'health_tracker_data_2020_1.json'
assert file_2020_1 in [item.name for item in dbutils.fs.ls(rawPath)], 'File not present in raw path'
print('Assertion passed.')
```

Verify the schema of a new table you created
--------------------------------------------
```python
# python

from pyspark.sql.types import _parse_datatype_string

schema string = 'datasource STRING, ingesttime TIMESTAMP, value STRING, p_ingestdate DATE'
assert bronze_health_tracker.schema == _parse_datatype_string(schema_string), 'File not present in Bronze Path'
print('Assertion passed.')
```

Working with notebooks practically
==================================
Want to write a plaintext python file meant for importing into Databricks? 
* Separate cells with `# COMMAND ----------` (10 hyphens)
* Any magic commands are preceded by `# MAGIC ` (each and every line, not just the cell)
    * Each line in a markdown cell also needs to be prefixed

A minimal working example file:
```python
# MAGIC %md
# MAGIC # Databricks notebook-compatible Python file
# MAGIC This will be your introduction markdown cell

# COMMAND ----------

import pandas as pd

# COMMAND ----------

def create_my_dataframe():
    df = pd.DataFrame([1, 2, 3, 4], columns=['A'])
    return df

# COMMAND ----------

# DBTITLE 1,Insert your cell title here

sample_df = create_my_dataframe()
sparkDF = spark.createDataFrame(sample_df)  # must convert to spark dataframe
sparkDF.createOrReplaceTempView('sample_data')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from sample_data;

# COMMAND ----------

```
