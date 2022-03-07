out_stream.writeStream \
          #<TO DO... how can you write the windowed aggregation?
          .table("readings_agg")

query = (out_stream.writeStream
   .outputMode('complete')
   .format('delta')
   .option('checkpointLocation', f"/FileStore/flight/{dbfs_data_path}streaming_ckpnt")
   .table("readings_agg")
   .start()
)


"""MLflow"""
from pyspark.ml.feature import IndexToString, StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator 

import mlflow
from mlflow import spark as mlflow_spark # renamed to prevent collisions when doing spark.sql

import time


# Call this function to train and test the Decision Tree model
# We put this code into a function so you can easily create multiple runs by calling it with different parameters
# It uses MLflow to track runs
# Remember to run this cell before calling it.  You must also run this cell every time you change something in it.  Otherwise, your changes will not be "seen."

def training_run(p_max_depth = 2, p_owner = "default") :
  with mlflow.start_run() as run:
    
    # Start a timer to get overall elapsed time for this function
    overall_start_time = time.time()
    
    # Log a Tag for the run
    # 
    # TO DO... use the mlflow api to log a Tag named "Owner" and set the value to p_owner
    # 
    mlflow.set_tag('Owner', p_owner)
    
    #
    # END OF TO DO
    #
    
    # Log the p_max_depth parameter in MLflow
    # 
    # TO DO... use the mlflow api to log a Parameter named "Maximum Depth" and set the value to p_max_depth
    # 
    mlflow.log_param('Maximum Depth', p_max_depth)
    
    # 
    # END OF TO DO
    #
    
    # STEP 1: Read in the raw data to use for training
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    df_raw_data = spark.sql("""
      SELECT 
        device_type,
        device_operational_status AS label,
        device_id,
        reading_1,
        reading_2,
        reading_3
      FROM current_readings_labeled
    """)
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 1
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=1)
    # 
    # END OF TO DO
    #

    # STEP 2: Index the Categorical data so the Decision Tree can use it
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    # Create a numerical index of device_type values (it's a category, but Decision Trees don't need OneHotEncoding)
    device_type_indexer = StringIndexer(inputCol="device_type", outputCol="device_type_index")
    df_raw_data = device_type_indexer.fit(df_raw_data).transform(df_raw_data)

    # Create a numerical index of device_id values (it's a category, but Decision Trees don't need OneHotEncoding)
    device_id_indexer = StringIndexer(inputCol="device_id", outputCol="device_id_index")
    df_raw_data = device_id_indexer.fit(df_raw_data).transform(df_raw_data)

    # Create a numerical index of label values (device status) 
    label_indexer = StringIndexer(inputCol="label", outputCol="label_index")
    df_raw_data = label_indexer.fit(df_raw_data).transform(df_raw_data)
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 2
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=2)
    # 
    # END OF TO DO
    #

    # STEP 3: create a dataframe with the indexed data ready to be assembled
    # We'll use an MLflow metric to log the time taken in each step 
    
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    # Populated df_raw_data with the all-numeric values
    df_raw_data.createOrReplaceTempView("vw_raw_data")
    df_raw_data = spark.sql("""
    SELECT 
      label_index AS label, 
      device_type_index AS device_type,
      device_id_index AS device_id,
      reading_1,
      reading_2,
      reading_3
    FROM vw_raw_data
    """)
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 3
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=3)
    # 
    # END OF TO DO
    #
  
    # STEP 4: Assemble the data into label and features columns
    
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    assembler = VectorAssembler( 
    inputCols=["device_type", "device_id", "reading_1", "reading_2", "reading_3"], 
    outputCol="features")

    df_assembled_data = assembler.transform(df_raw_data).select("label", "features")
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 4
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=4)
    # 
    # END OF TO DO
    #

    # STEP 5: Randomly split data into training and test sets. Set seed for reproducibility
    
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    (training_data, test_data) = df_assembled_data.randomSplit([0.7, 0.3], seed=100)
    
    # Log the size of the training and test data
    #
    # TO DO... use the mlflow API to log 2 Metrics:
    # - "Training Data Rows" populated with the count of rows in training_data above
    # - "Test Data Rows" populated with the count of rows in test_data above
    # NOTE: these metrics only occur once... they are not series
    #
    mlflow.log_metric('Training Data Rows', training_data.count())
    mlflow.log_metric('Test Data Rows', test_data.count())
    # 
    # END OF TO DO
    #
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 5
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=5)
    # 
    # END OF TO DO
    #

    # STEP 6: Train the model
    
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    # Select the Decision Tree model type, and set its parameters
    dtClassifier = DecisionTreeClassifier(labelCol="label", featuresCol="features")
    dtClassifier.setMaxDepth(p_max_depth)
    dtClassifier.setMaxBins(20) # This is how Spark decides if a feature is categorical or continuous

    # Train the model
    model = dtClassifier.fit(training_data)
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 6
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=6)
    # 
    # END OF TO DO
    #    

    # STEP 7: Test the model
    
    # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    df_predictions = model.transform(test_data)
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 7
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=7)
    # 
    # END OF TO DO
    #

    # STEP 8: Determine the model's accuracy
    
     # We'll use an MLflow metric to log the time taken in each step 
    start_time = time.time()
    
    evaluator = MulticlassClassificationEvaluator(
    labelCol="label", predictionCol="prediction")
    accuracy = evaluator.evaluate(df_predictions, {evaluator.metricName: "accuracy"})
    
    # Log the model's accuracy in MLflow
    #
    # TO DO... use the mlflow API to log a Metric named "Accuracy" and set the value to the accuracy variable calculated above
    # NOTE: this is a 1-time metric, not a series
    #
    mlflow.log_metric('Accuracy', accuracy)
    # 
    # END OF TO DO
    #
    
    # Log the model's feature importances in MLflow
    #
    # TO DO... use the mlflow API to log a Parameter named "Feature Importances" 
    # and set the value to a model attribute called model.featureImportances (cast to a string)
    #
    mlflow.log_param('Feature Importances', str(model.featureImportances))
    #
    # END OF TO DO
    #
    
    # We'll use an MLflow metric to log the time taken in each step 
    end_time = time.time()
    elapsed_time = end_time - start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Step Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this will be a multi-step metric that shows the elapsed time for each step in this function.
    #       Set this call to be step 8
    mlflow.log_metric('Step Elapsed Time', elapsed_time, step=8)
    # 
    # END OF TO DO
    #
    
    # We'll also use an MLflow metric to log overall time
    overall_end_time = time.time()
    overall_elapsed_time = overall_end_time - overall_start_time
    #
    # TO DO... use the mlflow API to log a Metric named "Overall Elapsed Time" and set the value to the elapsed_time calculated above
    # NOTE: this is a 1-time metric, not a series
    #      
    mlflow.log_metric('Overall Elapsed Time', elapsed_time)
    # 
    # END OF TO DO
    #
    
    # Log the model itself
    #
    # TO DO... use the mlflow API to log the model itself.  Find the correct API call for logging a Spark Model
    # NOTES:
    #  - We imported the relevant library earlier, using "from mlflow import spark as mlflow_spark" to avoid name collisions, so prefix your API call with "mlflow_spark.<your-api-call>"
    #  - You only need to use the first two parameters of the call.  The first is the model itself, and the second should be "spark-model"
    mlflow_spark.log_model(model, 'spark-model')
    #
    # END OF TO DO
    #
    
    return run.info.run_uuid


"""Loading a model"""
from pyspark.sql.functions import format_string

df_model_selector = (
  df_client.select(
      col('experiment_id'),
      col('run_id'),
      col('end_time'),
      col('metrics.Accuracy').alias('accuracy'),
      format_string('{}/spark-model', col('artifact_uri')).alias('artifact_uri')
  )
)
