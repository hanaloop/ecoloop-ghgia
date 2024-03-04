# GHGIA Microservice Manual Setup

This document provides instructions for manually starting the server.

## Preparing Database

The Postgres dbms needs to be up. A database can be created with

```sql
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


## Install

You will need to have poetry in your computer in order to manage the dependencies. If you haven't done so already, follow the installation instructions provided below.

* Install poetry package manager (see [official doc](https://python-poetry.org/docs/))

  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  source ~/.poetry/env
  ```
* Install application's dependency packages

  ```bash
  poetry install
  ```

Now you should be able to run `poetry shell` which is basically virtualenv.

The application requires Postgres database. It can be started using docker compose:

* Start docker compose with runtime dependencies

  ```sh
  docker compose up
  ```

## Migrating DB with Prisma

The application uses [Prisma](https://www.prisma.io/) as the ORM (Data adapter). Prisma comes with its own schema definition language and db migration tool.

**To create sync schema with DB (Dev mode)** 

This method bypasses the creation of migration file (that should be checked in the repo), and applying it, shortening the cycle.

  ```sh
  prisma db push
  ```

For production, use the migration file generation method below. 

**To create a new migration file** after extending or modifying `prsima/schema.prisma`

  ```sh
  prisma migrate dev --create-only --name <migration_name>
  ```

**To actually apply the migration file**

  ```sh
  prisma migrate deploy
  ```

## Running the server

Once the tables are created with through the DB migration process, you can now run the server.

* Run server

  ```bash
  uvicorn app.main:app --reload --port 9091
  ```

* Run tests

  ```bash
  [root]$ python3 -m pytest
  ```

* Usage
