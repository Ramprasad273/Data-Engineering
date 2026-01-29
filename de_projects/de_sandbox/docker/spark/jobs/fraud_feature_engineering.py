
import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import *


def run_spark_job(spark, transactions_table, output_table):
    """
    This is the main function for the Spark job.
    """

    # Read the transactions data
    transactions_df = spark.read.table(transactions_table)

    # 1. Rolling transaction windows
    window_spec_1h = (
        Window.partitionBy("customer_id").orderBy(col("transaction_time").cast("long")).rangeBetween(-3600, 0)
    )
    window_spec_24h = (
        Window.partitionBy("customer_id").orderBy(col("transaction_time").cast("long")).rangeBetween(-86400, 0)
    )

    # 2. Geo/device anomalies
    # Number of distinct devices and IP addresses used by a customer in the last 24 hours
    device_anomaly_df = transactions_df.withColumn("distinct_devices_24h", count("device_id").over(window_spec_24h))
    ip_address_anomaly_df = transactions_df.withColumn("distinct_ips_24h", count("ip_address").over(window_spec_24h))

    # 3. Velocity rules
    # Transaction count and sum in the last 1 hour and 24 hours
    velocity_df = (
        transactions_df.withColumn("transaction_count_1h", count("transaction_id").over(window_spec_1h))
        .withColumn("transaction_sum_1h", sum("transaction_amount").over(window_spec_1h))
        .withColumn("transaction_count_24h", count("transaction_id").over(window_spec_24h))
        .withColumn("transaction_sum_24h", sum("transaction_amount").over(window_spec_24h))
    )

    # Combine all features
    features_df = (
        device_anomaly_df.join(ip_address_anomaly_df, "transaction_id", "inner").join(
            velocity_df, "transaction_id", "inner"
        )
    )

    # Unpivot the features to a long format
    features_unpivoted_df = features_df.selectExpr(
        "transaction_id",
        "customer_id",
        "merchant_id",
        "stack(6, 'distinct_devices_24h', distinct_devices_24h, "
        + "'distinct_ips_24h', distinct_ips_24h, "
        + "'transaction_count_1h', transaction_count_1h, "
        + "'transaction_sum_1h', transaction_sum_1h, "
        + "'transaction_count_24h', transaction_count_24h, "
        + "'transaction_sum_24h', transaction_sum_24h) as (feature_name, feature_value)",
    )

    # Generate a unique feature ID
    features_unpivoted_df = features_unpivoted_df.withColumn(
        "feature_id", sha2(concat_ws("||", col("transaction_id"), col("feature_name")), 256)
    )

    # Add the feature generation time
    features_unpivoted_df = features_unpivoted_df.withColumn("feature_generation_time", current_timestamp())

    # Select the columns for the output table
    output_df = features_unpivoted_df.select(
        "feature_id",
        "customer_id",
        "merchant_id",
        "feature_name",
        "feature_value",
        "feature_generation_time",
    )

    # Write the data to the output table
    output_df.write.mode("append").saveAsTable(output_table)


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--transactions-table", required=True)
    parser.add_argument("--output-table", required=True)
    args = parser.parse_args()

    # Create a Spark session
    spark = SparkSession.builder.appName("FraudFeatureEngineering").getOrCreate()

    # Run the Spark job
    run_spark_job(spark, args.transactions_table, args.output_table)

    # Stop the Spark session
    spark.stop()

