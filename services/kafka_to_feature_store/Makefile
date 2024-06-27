run-dev:
	poetry run python src/main.py

build:
	docker build -t kafka-to-feature-store .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		--env-file .env \
		kafka-to-feature-store

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format