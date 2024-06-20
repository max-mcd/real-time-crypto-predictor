build:
	docker build -t trade_producer .

run: build
	docker run -it \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trade_producer

start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

lint:
	ruff check --fix

format:
	ruff format .
