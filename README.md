# EcoLoop GHGIA

Ecoloop microservice for Greenhouse Gas Emission Inventory Analysis

> Note: The endpoints are not guarded. It is recommended to not to expose the endpoints to public. The recommendation is to access it through the `ecoloop-server`.

## Tech Stack

- python
- fastapi
- pandas

## Install

TBD:

### Using Docker

* Build docker image

    ```bash
    # Usie script
    ./docker --build
    # Or build it manually
    docker build -t ecoloop-platform/ecoloop-ghgia .
    ```

* Run application from docker

    ```bash
    docker run --rm --name ecoloop-ghgia  -p 9090:9090 ecoloop-platform/ecoloop-ghgia-arm:latest
    ```

### Manual Setup

* Install poetry package manager (see [official doc](https://python-poetry.org/docs/))

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    source ~/.poetry/env
    ```

* Install dependency packages

    ```bash
    poetry install
    ```

* Run server

    ```bash
    python main.py
    ```

    or run by `uvicorn` with reload option for easy development

    ```bash
    uvicorn main:app --reload --port 9090
    ```
