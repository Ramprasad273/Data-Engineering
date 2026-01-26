#!/bin/bash

# Exit on error
set -e

# Function to check if a service is up
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3

    echo "Waiting for ${service_name} at ${host}:${port}..."
    while ! nc -z ${host} ${port}; do
        sleep 1
    done
    echo "${service_name} is up!"
}

# Wait for Postgres and Redis
wait_for_service postgres ${POSTGRES_PORT} "Postgres"
wait_for_service redis 6379 "Redis"


# Initialize Airflow DB and create user
airflow db init
airflow users create \
    --username ${AIRFLOW_USER} \
    --password ${AIRFLOW_PASSWORD} \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email ${AIRFLOW_EMAIL} || true # Ignore error if user already exists

# Add connections here if needed
# airflow connections add ...

# Start the scheduler in the background
airflow scheduler &

# Start the webserver in the foreground
exec airflow webserver
