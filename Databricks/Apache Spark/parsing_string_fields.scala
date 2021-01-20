/* Program: example_regexp_extract_parseing_fields.scala
   Description: sample code using regexp_extract to parse from string field
   Date: 2020-01-19 
   Programmers: DT and EC 

A note on performance:
  https://sparkbyexamples.com/spark/spark-dataframe-withcolumn/#add-replace-update-multiple-columns

  When adding, replacing, or updating multiple columns in a Spark DataFrame, it is advised to
  not to chain the withColumn() function, but rather use select() after creating a temporary view.

Method 3 based on
  - https://stackoverflow.com/a/41400588/6217208 (new columns) 
  - https://stackoverflow.com/a/2213528/6217208 (looping with index)

  This answer (https://stackoverflow.com/a/59842429/6217208) says Spark does not do well with loop
  logic and they suggest avoiding loops when dealing with columns. Maybe Method 2 is the best then.

*/

import org.apache.spark.sql.functions.regexp_extract;

/* Input */
val df_raw = spark.createDataFrame(
  Seq( ("5000001","Brandon Louis","brandname{0brnd}modelname{1mdln}serial{123456abcdefg}"),
       ("5000002","Marilyn Ham","honda{5hnda}cbr600{3cbr0}hondacbr2{293847japrntk}"),
       ("5000003","Mister Tee","yamaha{3ymha}r6{9r600}yamahar66{683964qwertyu}"), 
       ("5000004","Nunya Beeswax","triumph{2trmf}trident660{5trdt}triumphtrident0{016598dvoraku}"), 
       ("5000005","Michael Eller","aprilla{8aprl}rs660{0rs60}aprillars9{926593rlstnem}")
        )).toDF("id","name","file")

/* Show Schema */
// df_raw.printSchema
// df_raw.show

/* Parse File into 6 fields  */
/* Method 1 via withColumn */
val regexp_pattern = "(.*?)\\{(.*?)\\}(.*?)\\{(.*?)\\}(.*?)\\{(.*?)\\}"
val df1 = df_raw.withColumn("brand",regexp_extract($"file",regexp_pattern,1)).
                withColumn("brand_hash",regexp_extract($"file",regexp_pattern,2)).
                withColumn("model",regexp_extract($"file",regexp_pattern,3)).
                withColumn("model_hash",regexp_extract($"file",regexp_pattern,4)).
                withColumn("serial",regexp_extract($"file",regexp_pattern,5)).
                withColumn("serial_hash",regexp_extract($"file",regexp_pattern,6))
df1.show()

/* Method 2 via select */
val df2 = df_raw.select($"*",
                        regexp_extract($"file", regexp_pattern, 1).alias("brand"),
                        regexp_extract($"file", regexp_pattern, 2).alias("brand_hash"),
                        regexp_extract($"file", regexp_pattern, 3).alias("model"),
                        regexp_extract($"file", regexp_pattern, 4).alias("model_hash"),
                        regexp_extract($"file", regexp_pattern, 5).alias("serial"),
                        regexp_extract($"file", regexp_pattern, 6).alias("serial_hash")
                        )
df2.show()

/* Method 3 - using variables and loop */
import spark.implicits._

val newCols: Seq[String] = Seq("brand", "brand_hash", "model", "model_hash", "serial", "serial_hash")

// Simple loop to access items with index (0-indexed)
newCols.zipWithIndex.foreach{ case (new_col, i) =>
  println(i+1, new_col)
  }

// Simple loop with index beginning at 1 (but 'for loop' not allowed in `select()` statement)
for ((new_col, i) <- newCols.zip(Stream from 1)) {
  println(i, new_col)
  }

// Failed attempt to concatenate columns with looped column creator, based on SO answer
/*
val df3 = df_raw.select($"*" +: newCols.zipWithIndex.foreach{ case (new_col, i) =>
    regexp_extract($"file", regexp_pattern, i+1).alias(new_col)
    })
*/

// Working attempt with a sequence of tuples and anonymous function using `case`
val newCols2 = Seq(
  (1, "brand"), (2, "brand_hash"), (3, "model"), (4, "model_hash"), (5, "serial"), (6, "serial_hash")
  )
val df3 = df_raw.select($"*" +: newCols2.map({case (i, new_col) =>
    regexp_extract($"file", regexp_pattern, i).alias(new_col)
}): _*)
// map(...)     maps column names to a regex extract
// $"*" +: ...  prepends all pre-existing columns
// ... : _*     unpacks combined sequence
df3.show()

