# Spark SQL
## Creating tables from data in dbfs
```sql
CREATE TABLE IF NOT EXISTS events USING parquet OPTIONS (path "/mnt/training/ecommerce/events/events.parquet");
```

## Using scala to execute SQL

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

## Convert between dataframes and SQL
```scala
# SparkDF --> SQL view (local)
budgetDF.createOrReplaceTempView("budget")

# SparkDF --> SQL table (global)
budgetDF.write.mode("overwrite").saveAsTable("budget_s")

# SQL view --> spark df
val budgetDF = spark.sql("SELECT * FROM budget")
```

## Create and use a database other than `default`

```scala
val user_db = "my_new_database"
spark.sql(f"CREATE DATABASE IF NOT EXISTS $user_db")
spark.sql(f"USE $user_db")
```

## Using variables in SQL code
Ordinarily, you would need to use Python or Scala context in order to do string formatting / 
variable substitution in a SQL command, like so:

```python
myvar = 'mytable'
spark.sql(f"CREATE TABLE mytable USING DELTA LOCATION '/path/to/{myvar}'")
```

However, using widgets, you can specify what value you want to insert:

```python
# python

myvar = 'mytable'
dbutils.widgets.text('tablename', myvar)
```
```sql
-- sql 

CREATE TABLE mytable USING DELTA LOCATION "/path/to/$myvar"
```
