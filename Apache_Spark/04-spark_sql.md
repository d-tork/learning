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
