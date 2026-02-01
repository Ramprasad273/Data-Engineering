from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("DummyPipelineJob")
        .getOrCreate()
    )

    try:
        # Create dummy data
        data = [
            (1, "Alice", 25),
            (2, "Bob", 30),
            (3, "Charlie", 35),
            (4, "Diana", 28),
            (5, "Evan", 40),
        ]

        columns = ["id", "name", "age"]

        df = spark.createDataFrame(data, columns)

        print("=== SCHEMA ===")
        df.printSchema()

        print("=== SAMPLE DATA ===")
        df.show()

        print("=== RECORD COUNT ===")
        print(f"Total records: {df.count()}")
        
        print("=== JOB COMPLETED SUCCESSFULLY ===")
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
