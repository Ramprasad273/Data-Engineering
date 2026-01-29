
import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline


def run_spark_job(spark, fraud_features_table, output_table):
    """
    This is the main function for the Spark job.
    """

    # Read the fraud features data
    fraud_features_df = spark.read.table(fraud_features_table)

    # Pivot the features to a wide format
    pivot_df = fraud_features_df.groupBy("customer_id").pivot("feature_name").agg(first("feature_value"))

    # Assemble the feature vector
    assembler = VectorAssembler(
        inputCols=[
            "distinct_devices_24h",
            "distinct_ips_24h",
            "transaction_count_1h",
            "transaction_sum_1h",
            "transaction_count_24h",
            "transaction_sum_24h",
        ],
        outputCol="features",
    )

    # Placeholder for the ML model
    # In a real-world scenario, you would train a model and use it to predict the risk score.
    # For now, we'll just generate a random risk score.
    # Create a dummy label column
    pivot_df = pivot_df.withColumn("label", rand())
    lr = LinearRegression(featuresCol="features", labelCol="label")
    pipeline = Pipeline(stages=[assembler, lr])
    model = pipeline.fit(pivot_df)

    # Make predictions
    predictions = model.transform(pivot_df)

    # Generate customer risk scores
    customer_risk_scores_df = predictions.select(
        col("customer_id").alias("entity_id"),
        lit("customer").alias("entity_type"),
        col("prediction").alias("risk_score"),
        current_timestamp().alias("score_generation_time"),
        lit("v1.0").alias("ml_model_version"),
    ).withColumn("score_id", sha2(concat_ws("||", col("entity_id"), col("score_generation_time")), 256))

    # Write the customer risk scores to the output table
    customer_risk_scores_df.write.mode("append").saveAsTable(output_table)

    # You can do the same for merchant risk scores if you have merchant features


if __name__ == "__main__":
    # Create a Spark session
    parser = argparse.ArgumentParser()
    parser.add_argument("--fraud-features-table", required=True)
    parser.add_argument("--output-table", required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.appName("RiskScoring").getOrCreate()

    # Run the Spark job
    run_spark_job(spark, args.fraud_features_table, args.output_table)

    # Stop the Spark session
    spark.stop()

