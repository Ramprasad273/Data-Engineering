# Data Engineering Projects

This repository contains a collection of sample data engineering projects.

## 1. Data Streaming 101

This section focuses on projects related to data streaming technologies.

### i. Kafka Projects

These projects demonstrate the use of Apache Kafka with Python.

#### Kafka 101

This project provides a basic example of a Kafka producer and consumer implementation in Python.

**Project Structure:**

-   `kafka_producer.py`: A Python script to send messages to a Kafka topic.
-   `kafka_consumer.py`: A Python script to consume messages from a Kafka topic.
-   `kafka_configurations.py`: Contains configuration settings for the Kafka producer and consumer.

**Code Improvements:**

*   **Improved Documentation:** Added detailed docstrings to all functions to improve code readability and maintainability.
*   **`.gitignore`:** Included a comprehensive `.gitignore` file to exclude unnecessary files from version control.
*   **Producer Optimization:** The producer script has been refactored to use a single producer instance for better performance.

## Getting Started

### Prerequisites

*   Python 3.x
*   Apache Kafka
*   `kafka-python` library

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Install the required Python library:**
    ```bash
    pip install kafka-python
    ```
3.  **Start your Kafka server.** Make sure the server is running on `localhost:9092`.

## Usage

### Running the Kafka Producer

To send messages to the `topic1` topic, run the following command:

```bash
python de_projects/Kakfa_projects/Kafka_101/kafka_producer.py
```

### Running the Kafka Consumer

To consume messages from the `topic1` topic, run the following command:

```bash
python de_projects/Kakfa_projects/Kafka_101/kafka_consumer.py
```
