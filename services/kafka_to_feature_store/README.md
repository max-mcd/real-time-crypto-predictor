# Kafka to Feature Store Service

## What does this service do?

This Python microservice

- reads OHLC data from a kafka topic
- saves that data to a HopsWorks Feature Store

## How to run this service?

## Set up
To run this service locally you first need to start locally the message bus (Redpanda in this case).
```
$ cd ../../docker-compose && make start-redpanda
```

The following services must also be running:
- Trade Producer
- Trade to OHLC

### Without Docker

- Create an `.env` file with the KAFKA_BROKER_ADDRESS
    ```
    $ cp .sample.env .env
    # add the info and save it
    ```
    
- `poetry run python src/main.py`

### With Docker

Build the Docker image for this service, and run the container
```
$ make run
```