# Review of all DataFrame Actions
Drop duplicate rows, but name columns may be in mis-matching case and some SSNs are hyphenated
but others are not. Save as 8 partitions of a parquet file. 

## My solution
```scala
// Set input _and_ output locations at the top
val sourceFile = "dbfs:/mnt/training/dataframes/people-with-dups.txt"
val destFile = workingDir + "/people.parquet"
```

```scala
val rawDF = spark.read
	.option("header", true)
	.option("sep", ":")
	.option("inferSchema", true)
	.csv(sourceFile)

import org.apache.spark.sql.functions._

val combinedIdDF = rawDF
	.withColumn("full_id", upper(concat_ws(" ", $"firstName", $"middleName", $"lastName")))
	.withColumn("full_id", concat_ws("-", $"full_id", $"birthDate"))
	.cache()

val finalDF = combinedIdF
	.dropDuplicates(Seq("full_id"))
	.drop("full_id")
	.repartition(8)

finalDF.write.parquet(destFile)
```

## Alternate solution
```scala
val dedupedDF = df
	.select($"*",
		lower($"firstName").as("lcFirstName"),
		lower($"middleName").as("lcmiddleName"),
		lower($"lastName").as("lcLastName"),
		translate($"ssn", "-", "").as("ssnNums")
		// regexp_replace($"ssn", "-", "").as("ssnNums")
		// regexp_replace($"ssn", """^(\d{3})(\d{2})(\d{4})$""", "$1-$2-$3").alais("ssnNums")
	.dropDuplicates("lcFirstName", "lcMiddleName", "lcLastName", "ssnNums", "gender", "birthDate", "salary")
	.drop("lcFirstName", "lcMiddleName", "lcLastName", "ssnNums")

import org.apache.spark.sql.SaveMode
dedupedDF.write
	.mode(SaveMode.Overwrite)
	.option("compression", "snappy")
	.parquet(destFile)
```
