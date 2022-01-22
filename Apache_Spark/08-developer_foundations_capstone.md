# Developer Foundations Capstone
registration ID: 2425327

## If I find a bug
* https://help.databricks.com/s/contact-us
* set issue field to "Training"
* set subject field to "Developers Fundamentals Capstone"

batch_2019 = (batch_2019
              .withColumnRenamed('orderId', 'order_id')
              .withColumnRenamed('customerId', 'customer_id')
              .withColumnRenamed('salesRepId', 'sales_rep_id')
              .withColumnRenamed('salesRepSsn', 'sales_rep_ssn')
              .withColumnRenamed('salesRepFirstName', 'sales_rep_first_name')
              .withColumnRenamed('salesRepLastName', 'sales_rep_last_name')
              .withColumnRenamed('salesRepAddress', 'sales_rep_address')
              .withColumnRenamed('salesRepCity', 'sales_rep_city')
              .withColumnRenamed('salesRepState', 'sales_rep_state')
              .withColumnRenamed('salesRepZip', 'sales_rep_zip')
              .withColumnRenamed('shippingAddressAttention', 'shipping_address_attention')
              .withColumnRenamed('shippingAddressAddress', 'shipping_address_address')
              .withColumnRenamed('shippingAddressCity', 'shipping_address_city')
              .withColumnRenamed('shippingAddressState', 'shipping_address_state')
              .withColumnRenamed('shippingAddressZip', 'shipping_address_zip')
              .withColumnRenamed('productId', 'product_id')
              .withColumnRenamed('productQuantity', 'product_quantity')
              .withColumnRenamed('productSoldPrice', 'product_sold_price')
             )

productsDF = (productsDF
              .withColumn('product_id', col('_product_id'))
              .withColumn('base_price', col('price._base_price'))
              .withColumn('color_adj', col('price._color_adj'))
              .withColumn('size_adj', col('price._size_adj'))
              .withColumn('price', col('price.usd'))
              .filter(col('price').isNotNull())
             )

```python
stream_df = (stream_df
             .withColumnRenamed('submittedAt', 'submitted_at')
             .withColumnRenamed('orderId', 'order_id')
             .withColumnRenamed('customerId', 'customer_id')
             .withColumnRenamed('salesRepId', 'sales_rep_id')
             .withColumn('shipping_address_attention', col('shippingAddress.attention'))
             .withColumn('shipping_address_address', col('shippingAddress.address'))
             .withColumn('shipping_address_city', col('shippingAddress.city'))
             .withColumn('shipping_address_state', col('shippingAddress.state'))
             .withColumn('shipping_address_zip', col('shippingAddress.zip'))
			 .withColumn('ingest_file_name', lit(stream_path))
			 .withColumn('ingested_at', current_timestamp())
			 .withColumn('submitted_at', col('submitted_at').cast('timestamp'))
			 .withColumn('submitted_yyyy_mm', date_format(col('submitted_at'), 'yyyy-MM'))
            )
```

## 3B
```python
# Johanna's solution
from pyspark.sql.functions import explode, col, input_file_name, current_timestamp, date_format 

staticDF = spark.read.option("inferSchema","true").json(stream_path)
streamDF = spark.readStream.format("json").schema(staticDF.schema).option("maxFilesPerTrigger", 1).load(stream_path) 
# staticDF.printSchema() 
df2 = streamDF.select(col("submittedAt").cast("timestamp").alias("submitted_at"), \
         col("orderId").alias("order_id"), \
         col("customerId").alias("customer_id"), \
         col("salesRepId").alias("sales_rep_id"), \
         col("shippingAddress.attention").alias("shipping_address_attention"), \
         col("shippingAddress.address").alias("shipping_address_address"), \
         col("shippingAddress.city").alias("shipping_address_city"), \
         col("shippingAddress.state").alias("shipping_address_state"), \
         col("shippingAddress.zip").cast("int").alias("shipping_address_zip")) \
  .withColumn("ingest_file_name", input_file_name()) \
  .withColumn("ingested_at", current_timestamp()) \
  .withColumn("submitted_yyyy_mm", date_format(col("submitted_at"),"yyyy-MM"))

# df2.show(5)
# df2.printSchema()   

df2.writeStream.outputMode("append").format("delta").partitionBy("submitted_yyyy_mm").queryName(orders_table).option("checkpointLocation",orders_checkpoint_path).table(orders_table) 
```

## 3D
```python
from pyspark.sql.functions import from_unixtime, col, date_format
from pyspark.sql.types import IntegerType

orders_df = (spark.sql(f'SELECT * from {batch_temp_view}')
             .withColumn('submitted_at', from_unixtime('submitted_at').cast('timestamp'))
             .withColumn('shipping_address_zip', col('shipping_address_zip').cast(IntegerType()))
            )

drop_cols = """sales_rep_ssn, sales_rep_first_name, sales_rep_last_name, sales_rep_address, sales_rep_city, sales_rep_state, sales_rep_zip, product_id, product_quantity, product_sold_price""".split(', ')
orders_df = orders_df.drop(*drop_cols)

dupe_subset = list(set(orders_df.columns) - {'ingest_file_name', 'ingested_at'})
orders_df = orders_df.drop_duplicates(dupe_subset)

yyyy_mm_col_name = 'submitted_yyyy_mm'
orders_df = (orders_df
             .withColumn(yyyy_mm_col_name, date_format(col('submitted_at'), 'yyyy-MM'))
            )

(orders_df.write.format('delta')
 .mode('overwrite')
 .partitionBy(yyyy_mm_col_name)
 .option('overwriteSchema', 'true')
 .saveAsTable(orders_table)
)
```
