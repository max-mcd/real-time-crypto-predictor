# The Trade-to-OHLC service

## What does this service do?

This Python microservice

- Reads trades from a kafka topic
- Transforms them into OHLC candles, and
- Saves them in another kakfa topic

## How to run this service?

## Set up
To run this service locally you first need to start locally the message bus (Redpanda in this case).
```
$ cd ../../docker-compose && make start-redpanda

```

### Without Docker

- Create an `.env` file with the KAFKA_BROKER_ADDRESS
    ```
    $ cp .sample.env .env
    # add the info and save it
    ```
    
- `poetry run python src/main.py`

### With Docker

Build the Docker image for this service, and run the containers:
- `trade_producer`
- `trade_ohlc_service`
```
$ cd ../trade_producer
$ make run
$ cd ../trade_to_ohlc
$ make run
```