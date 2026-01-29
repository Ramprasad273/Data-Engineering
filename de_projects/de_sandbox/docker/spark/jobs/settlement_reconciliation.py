
import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def run_spark_job(spark, transactions_table, settlement_files_path, output_table):
    """
    This is the main function for the Spark job.
    """

    # Read the transactions data
    transactions_df = spark.read.table(transactions_table)

    # Read the settlement files
    settlement_df = spark.read.csv(settlement_files_path, header=True, inferSchema=True)

    # Join the transactions and settlement data
    reconciliation_df = transactions_df.join(settlement_df, "transaction_id", "left_outer")

    # Detect mismatches and compute settlement status
    reconciliation_df = reconciliation_df.withColumn(
        "is_reconciled",
        when(
            col("settlement_amount").isNotNull() & (col("transaction_amount") == col("settlement_amount")),
            True,
        ).otherwise(False),
    )
    reconciliation_df = reconciliation_df.withColumn(
        "mismatch_reason",
        when(col("settlement_amount").isNull(), "missing_settlement")
        .when(col("transaction_amount") != col("settlement_amount"), "amount_mismatch")
        .otherwise(None),
    )

    # Generate a unique settlement ID
    reconciliation_df = reconciliation_df.withColumn(
        "settlement_id", sha2(concat_ws("||", col("transaction_id"), col("settlement_date")), 256)
    )

    # Select the columns for the output table
    output_df = reconciliation_df.select(
        "settlement_id",
        "transaction_id",
        "settlement_date",
        "settlement_amount",
        "is_reconciled",
        "mismatch_reason",
    )

    # Write the data to the output table
    output_df.write.mode("append").saveAsTable(output_table)


if __name__ == "__main__":
    # Create a Spark session
    parser = argparse.ArgumentParser()
    parser.add_argument("--transactions-table", required=True)
    parser.add_argument("--settlement-files-path", required=True)
    parser.add_argument("--output-table", required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.appName("SettlementReconciliation").getOrCreate()

    # Run the Spark job
    run_spark_job(spark, args.transactions_table, args.settlement_files_path, args.output_table)

    # Stop the Spark session
    spark.stop()

