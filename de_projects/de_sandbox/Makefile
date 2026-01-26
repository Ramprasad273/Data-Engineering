.PHONY: up down build logs clean

# Default action
all: up

# Start all services
up:
	@echo "Starting up the data platform..."
	@docker compose up -d --build

# Stop all services
down:
	@echo "Stopping the data platform..."
	@docker compose down

# Rebuild images
build:
	@echo "Building images..."
	@docker compose build

# View logs for all services
logs:
	@docker compose logs -f

# Clean up all data
clean: down
	@echo "Cleaning up all data..."
	@docker compose down -v --remove-orphans
	@sudo rm -rf ./docker/airflow/logs/*
	@sudo rm -rf ./docker/airflow/plugins/*
	@echo "Done."

# Initialize environment
init:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
	fi
	@make up

# Run a command in the airflow webserver container
airflow:
	@docker compose exec airflow_webserver bash

# Run dbt commands
dbt:
	@docker compose exec airflow_webserver dbt $(filter-out $@,$(MAKECMDGOALS))

# Run great_expectations commands
ge:
	@docker compose exec airflow_webserver great_expectations $(filter-out $@,$(MAKECMDGOALS))