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


## Seeding the data and calculating the emissions from the command line

```
The scripts should be run in the following order:

scripts/script_import_region.py -> time taken = seconds
scripts/script_import_sites.py -> time taken = 30 minutes
scripts/script_import_organizations.py -> time taken = 10 minutes
scripts/script_import_emission_data.py (Gir4)-> time taken = 1 minutes
scripts/script_import_emission_data.py (Gir1)-> time taken = 10 minutes
scripts/script_import_ets.py -> time taken = ~1 minute
scripts/link_emissions_to_codes.py -> time taken = 10 minutes
scripts/script_calculate_emissions.py -> time taken = 1 minute per year requested
```

Each script can be run by typing:
```python <name_of_script.py> --<expected_arg1> <value> --<expected_arg2> <value2>```

Usage instructions and accepted params can be shown by running <name_of_script.py> --help

A sample shell script on how to run the data can be found in the root folder.

Optional: You can generate pickles needed for the tests, by running:
```
python scripts/script_generate_pickles.py
```

!!!Important!!!

For the factory data the file (2020.05월말기준)_전국공장등록현황.xlsx was used. Other files have different structures and will not work. (except the 2023 file that includes business registration numbers)
```
