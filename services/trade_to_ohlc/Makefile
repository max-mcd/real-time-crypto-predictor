build:
	docker build -t trade_to_ohlc .

run: build
	docker run -it \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trade_to_ohlc

start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

lint:
	ruff check --fix

format:
	ruff format .
