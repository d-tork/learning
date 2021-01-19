/* Program: example_regexp_extract_parseing_fields.scala
   Description: sample code using regexp_extract to parse from string field
   Date: 2020-01-19 
   Programmers: DT and EC */

import org.apache.spark.sql.functions.regexp_extract;

/* Input */
val df_raw = spark.createDataFrame(
  Seq( ("5000001","Brandon Louis","brandname{0abcd}modelname{1efgh}serial{123456abcdefg}"),
       ("5000002","Marilyn Ham","honda{0abcd}cbr600{1efgh}vin{123456abcdefg}"),
       ("5000003","Mister Tee","yamaha{0abcd}r6{1efgh}vin{123456abcdefg}"), 
       ("5000004","Nunya Beeswax","triumph{0abcd}trident660{1efgh}vin{123456abcdefg}"), 
       ("5000005","Michael Eller","aprilla{0abcd}rs660{1efgh}vin{123456abcdefg}")
        )).toDF("id","name","file")

/* Show Schema */
// df_raw.printSchema
// df_raw.show

/* Parse File into 6 fields  */
/* Method 1 via withColumn */
val regexp_pattern = "(.*?)\\{(.*?)\\}(.*?)\\{(.*?)\\}(.*?)\\{(.*?)\\}"
val df = df_raw.withColumn("brand",regexp_extract($"file",regexp_pattern,1)).
                withColumn("brand_hash",regexp_extract($"file",regexp_pattern,2)).
                withColumn("model",regexp_extract($"file",regexp_pattern,3)).
                withColumn("model_hash",regexp_extract($"file",regexp_pattern,4)).
                withColumn("serial",regexp_extract($"file",regexp_pattern,5)).
                withColumn("serial_hash",regexp_extract($"file",regexp_pattern,6))
df.show

/* Method 2 via select */
vs df2 = df.select($"*", regexp_extract($"file", regexp_pattern, 1).alias("brand"),
                         regexp_extract($"file", regexp_pattern, 2).alias("brand_hash"))

df2.show

/* Method 3 - to-do - using variables and loop */