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

You will need to have poetry in your computer in order to manage the dependencies. If don't have it yet, install following the instruction below.

* Install poetry package manager (see [official doc](https://python-poetry.org/docs/))

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  source ~/.poetry/env
  ```

* Install dependency packages

  ```bash
  poetry install
  ```

Now you should be able to run `poetry shell` which is basically virtualenv.

The application requires Postgres database. It can be started using docker compose:

* Start docker compose with runtime dependencies 

  ```bash
  docker compose up
  ```

## Preparing Database

The Postgres dbms needs to be up. A database can be created with
```
CREATE DATABASE ecoloop_ghgia_local
  ENCODING utf8
  LC_COLLATE 'C.UTF-8'
  LC_CTYPE 'C.UTF-8'
  TEMPLATE template0;

CREATE USER ecoloopghgia_local WITH PASSWORD 'ecoloopghgia_local';

GRANT ALL ON DATABASE "ecoloop_ghgia_local" to ecoloopghgia_local;

CREATE DATABASE ecoloop_ghgia_shadow_local
  ENCODING utf8
  LC_COLLATE 'C.UTF-8'
  LC_CTYPE 'C.UTF-8'
  TEMPLATE template0;

GRANT ALL ON DATABASE "ecoloop_ghgia_shadow_local" to ecoloopghgia_local;
```

**NOTE**: Once the database is created you need to connect as super admin (not the user you just created), and grant privileges to the public schema.

```sql
GRANT ALL ON SCHEMA public TO ecoloopghgia_local;
```

## Migrating Prisma 

**To create a new migration file** after extending or modifying `prsima/schema.prisma`

```sh
prisma migrate dev --create-only --name <migration_name>
```

**To actually apply the migration file**
```sh
prisma migrate deploy
```

## Running the application

* Run server

  ```bash
  uvicorn app.main:app --reload --port 9090
  ```
* Run tests

  ```bash
  cd app
  python3 -m pytest
  ```
* Usage

The api can be accessed at ``http://localhost:9090/docs``. You can upload iorgsites using the ``/api/iorgsites/upload`` endpoint. The data can also be read from a local file, by providing a path to the file. This can only be done by creating a script that directly imports and runs the service, since python packages cannot be directly executed.


## Seed the data

Suggested order to seed the data:

1. Import Code and Region

  As of 12/21, this process is just restoring the tables from EcoLoop.

2. ISite

  2.1. Import FactoryOn

3. IOrganization
