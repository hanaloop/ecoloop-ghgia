#!/bin/sh
python scripts/script_import_region.py --path .seed_data/region.ecoloop.import.csv
python scripts/script_import_sites.py --path .seed_data/sites.전국공장등록현황.xlsx
python scripts/script_import_organizations.py --path .seed_data/CORPCODE.xml
python scripts/script_import_emission_data.py --path .seed_data/emission_data.gir4.import.xls
python scripts/script_import_emission_data.py --path .seed_data/emission_data.gir1.import.csv
python scripts/script_calculate_emissions.py --year_from 2017 --year_to 2020

