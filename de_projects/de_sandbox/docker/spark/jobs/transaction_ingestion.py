
import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def run_spark_job(spark, input_path, output_table):
    """
    This is the main function for the Spark job.
    """

    # Read the input data
    df = spark.read.json(input_path)

    # Deduplicate the data
    df = df.dropDuplicates(["transaction_id"])

    # Add the ingestion date
    df = df.withColumn("ingestion_date", current_date())

    # Write the data to the output table
    df.write.mode("append").partitionBy("ingestion_date").saveAsTable(output_table)


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-table", required=True)
    args = parser.parse_args()

    # Create a Spark session
    spark = SparkSession.builder.appName("TransactionIngestion").getOrCreate()

    # Run the Spark job
    run_spark_job(spark, args.input_path, args.output_table)

    # Stop the Spark session
    spark.stop()
