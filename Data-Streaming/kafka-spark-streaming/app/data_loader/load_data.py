import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import when
import logging

logger = logging.getLogger("load_data")

logging.basicConfig(encoding='utf-8', level=logging.INFO,format='%(asctime)s-%(name)s: %(message)s')


def initialize_spark_context(app_name):
    logger.info("Initializing spark context")
    return SparkSession.builder.appName(app_name).getOrCreate()


def load_csv_data(sc,csv_path,header_boolean):
    logger.info("Loading csv data")
    return sc.read.option("header", header_boolean).csv(csv_path)


def process_temp_csv(sc,df):
    logger.info("Processing dataframe")
    indian_temperature_df = df.withColumn("City", when(df.City == "Bombay (Mumbai)", "Mumbai")
                                                      .when(df.City == "Chennai (Madras)", "Chennai")
                                                      .otherwise(df.City))

    logger.info("Cleaned city names")

    indian_temperature_df = indian_temperature_df.withColumn("State",
                                                             when(indian_temperature_df.City == "Mumbai", "Maharastra")
                                                             .when(indian_temperature_df.City == "Chennai",
                                                                   "Tamil Nadu")
                                                             .when(indian_temperature_df.City == "Calcutta",
                                                                   "West Bengal")
                                                             .when(indian_temperature_df.City == "Delhi", "New Delhi")
                                                             .otherwise(indian_temperature_df.State))

    logger.info("Updated State names")

    return indian_temperature_df.filter(indian_temperature_df.Country == "India")


def write_to_json(df,write_path):
    df.write.mode('overwrite').json(write_path)
