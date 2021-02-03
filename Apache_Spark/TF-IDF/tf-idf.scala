//convert to scala
//val raw = table("raw_table")
val raw = spark.read.options(Map("inferSchema"->"true","delimiter"->",","header"->"true")).csv("sample.csv")

import org.apache.spark.sql.functions
import org.apache.spark.sql.functions._

val df2 = raw
//val doc_count = raw.count
val doc_count = df2.select(countDistinct("machine")).collect()(0)(0).
  toString.toDouble
println("Machine count: " + doc_count)

//count up term frequencies
val tf_grp = df2.groupBy("machine", "device").agg(sum("dummy") as "tf")
tf_grp.show

//count up document frequencies
val df_grp = df2.groupBy("device").agg(countDistinct("machine") as "df")
df_grp.show

//helper function to calculate individual inverse document frequency
def calcIdf(docCount: Double, docfreq: Double): Double= {
  val idf = math.log10(docCount / (docfreq+1))
  return idf
}

//apply inverse doc frequency function to column with a UDF 
def calcIdfUdf = udf { df: Double => calcIdf(doc_count, df)}
val df_grp_inverse = df_grp.withColumn("idf", calcIdfUdf(col("df")))
df_grp_inverse.show

//join TF and IDF, then get their product
val joined = tf_grp.
  join(df_grp_inverse, Seq("device"), "left").
  withColumn("tf_idf", col("tf") * col("idf"))
joined.show

joined.coalesce(1).write.format("com.databricks.spark.csv").mode("overwrite").option("header", "true").save("tf_idf-final.csv")
