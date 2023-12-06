# EcoLoop GHGIA

Ecoloop microservice for Greenhouse Gas Emission Inventory Analysis

> Note: The endpoints are not guarded. It is recommended to not to expose the endpoints to public. The recommendation is to access it through the `ecoloop-server`.

## Tech Stack

- python
- fastapi
- pandas
- pytest
- asyncio

## Install

Using Docker

* Install poetry package manager (see [official doc](https://python-poetry.org/docs/))

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  source ~/.poetry/env
  ```
* Install dependency packages

  ```bash
  poetry install
  ```
* Start docker container

  ```bash
  docker compose up
  ```
* Run server

  ```bash
  uvicorn app.main:app --reload --port 9090
  ```
* Run tests

  ```bash
  python3 -m pytest
  ```
* Usage

The api can be accessed at ``http://localhost:9090/docs``. You can upload iorgsites using the ``/api/iorgsites/upload`` endpoint. The data can also be read from a local file, by providing a path to the file. This can only be done by creating a script that directly imports and runs the service, since python packages cannot be directly executed.
