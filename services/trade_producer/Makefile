run-dev:
	poetry run python src/main.py

build:
	docker build -t trade_producer .

run: build
	docker run -it \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trade_producer

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format
