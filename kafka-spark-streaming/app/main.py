"""
Driver Program to start loading the data using spark.
convert raw data to json data and process them into the DBs.
"""
import logging
from data_loader import load_data

logger = logging.getLogger("main")

logging.basicConfig(encoding='utf-8', level=logging.INFO,format='%(asctime)s-%(logger)s: %(message)s')


def prepare_temp_data():
    df = load_data.load_csv_data(sc, read_csv_path, header_boolean)
    logger.info("Temperature Data frame created")
    df.printSchema()

    processed_df = load_data.process_temp_csv(sc, df)
    logger.info("Temperature Data frame processed")

    load_data.write_to_json(processed_df, write_path)
    logger.info("Temperature JSON File created.")


def prepare_rainfall_data():
    df = load_data.load_csv_data(sc, read_csv_path, header_boolean)
    logger.info("Rainfall Data frame created")
    df.printSchema()
    load_data.write_to_json(df, write_path)
    logger.info("Rainfall JSON File created.")


def prepare_water_quality_data():
    df = load_data.load_csv_data(sc, read_csv_path, header_boolean)
    logger.info("Water Quality Data frame created")
    df.printSchema()
    load_data.write_to_json(df, write_path)
    logger.info("Water Quality File created.")


def prepare_air_quality_data():
    df = load_data.load_csv_data(sc, read_csv_path, header_boolean)
    logger.info("Air Quality Data frame created")
    df.printSchema()
    load_data.write_to_json(df, write_path)
    logger.info("Air Quality File created.")


if __name__ == '__main__':
    logger.info("Program started...")
    logger.info("Loading data...")

    app_name = "data_analysis"
    header_boolean = True
    read_csv_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/city_temperature.csv"
    write_path ="/Github_repo/Data-Engineering/kafka-spark-streaming/data/temperatue_json"

    sc = load_data.initialize_spark_context(app_name)
    logger.info("Spark context retrieved: %s", sc)
    prepare_temp_data()

    read_csv_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/rainfall_data.csv"
    write_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/rainfall_json"
    prepare_rainfall_data()

    read_csv_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/water_quality_data.csv"
    write_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/water_quality_json"
    prepare_water_quality_data()

    read_csv_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/air_quality_data.csv"
    write_path = "/Github_repo/Data-Engineering/kafka-spark-streaming/data/air_quality_json"
    prepare_air_quality_data()








