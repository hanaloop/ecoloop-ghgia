# EcoLoop GHGIA

Ecoloop Greenhouse Gas Emission Inventory Analysis (GHGIA) also known as GHG Registry

> Note: The endpoints are not guarded. It is recommended to not to expose the endpoints to public. The recommendation is to access it through a gated server.

## Tech Stack

The server is a python FastAPI-based application, and uses the following libraries among others (see ) 
- python
- fastapi
- pandas
- pytest
- asyncio


## Running the application

### Required environment

Before running the server, setup the `.env-docker` file with using template below:

  ```sh
  # Used by the Docker compose
  DB_USERNAME=your_db_username
  DB_PASSWORD=your_db_password
  DB_DATABASE_NAME=your_database_name

  ECOLOOP_GHGIA_IMAGE=ecoloop-platform/ecoloop-ghgia-arm:latest

  TEST_DB_DATABASE_NAME=your_test_database_name

  # Used by the app
  DATABASE_URL=postgresql://{your_db_username}:{your_db_password}@postgres:5432/{your_database_name}?schema=public&connection_limit=25

  TEST_DATABASE_URL = postgresql://your_db_username:your_db_password@postgres:5432/your_test_database_name?schema=public&connect_timeout=0&connection_limit=80
  API_KEY=
  KAKAO_API_KEY = kakao_api_for_map
  KAKAO_API_BURL = https://dapi.kakao.com/v2/local/search/address.json
  ```

### Starting the postgres(db) and server with docker-compose

The easiest way to running the server is by starting the docker compose.
The docker compose will start Postgres, initialize the DB and start the ghgia server.

Use below script to run start docker compose:

```sh
./service-up.sh
```

If the application is up, you should be able to access the api docat ``http://localhost:9091/docs``. 

You can ingest iorgsites data using the ``/api/iorgsites/upload`` endpoint. 

The data can also be read from a local file by providing a path to the file. 


## Seeding lookup data, ingesting data and calculating the emissions

When GHGIA is started for the first time, the database is empty, and it needs to be seeded before it can function properly. There is a command line script that seeds and ingests the db with the following data:

1. Code - Codes of IPCC (Source/Sink) Categories used in the system
2. Region - Countries and Korea province and districts
3. Sites  - Factories
4. Organizations -
5. GIR Emission data
6. GIR emission data

After seeding and ingesting data, the emission distribution is calculated.

```sh
# The scripts should be run in the following order:

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
