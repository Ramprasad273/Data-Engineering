
import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def run_spark_job(
    spark,
    customer_input_path,
    merchant_input_path,
    customer_output_table,
    merchant_output_table,
):
    """
    This is the main function for the Spark job.
    """

    # Read the customer input data
    customer_df = spark.read.csv(customer_input_path, header=True, inferSchema=True)

    # Validate compliance fields
    customer_df = customer_df.withColumn(
        "kyc_status",
        when(col("kyc_status").isin(["verified", "pending", "failed"]), col("kyc_status")).otherwise("pending"),
    )

    # Write the data to the output table
    customer_df.write.mode("overwrite").saveAsTable(customer_output_table)

    # Read the merchant input data
    merchant_df = spark.read.csv(merchant_input_path, header=True, inferSchema=True)

    # Validate compliance fields
    merchant_df = merchant_df.withColumn(
        "is_compliant",
        when(col("is_compliant").isNull(), False).otherwise(col("is_compliant")),
    )

    # Write the data to the output table
    merchant_df.write.mode("overwrite").saveAsTable(merchant_output_table)


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer-input-path", required=True)
    parser.add_argument("--merchant-input-path", required=True)
    parser.add_argument("--customer-output-table", required=True)
    parser.add_argument("--merchant-output-table", required=True)
    args = parser.parse_args()

    # Create a Spark session
    spark = SparkSession.builder.appName("CustomerMerchantMaster").getOrCreate()

    # Run the Spark job
    run_spark_job(
        spark,
        args.customer_input_path,
        args.merchant_input_path,
        args.customer_output_table,
        args.merchant_output_table,
    )

    # Stop the Spark session
    spark.stop()

