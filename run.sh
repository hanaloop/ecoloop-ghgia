# !/bin/sh
python scripts/script_import_region.py --path .seed_data/region.ecoloop.import.csv
python scripts/script_import_sites.py --path .seed_data/sites.전국공장등록현황.xlsx
python scripts/script_import_code.py --path .seed_data/code.ecoloop.import.csv
python scripts/script_import_organizations.py --path .seed_data/CORPCODE.xml
python scripts/script_import_emission_data.py --path .seed_data/emission_data.gir4.import.xls
python scripts/script_import_emission_data.py --path .seed_data/emission_data.gir1.import.csv
python scripts/script_import_ets.py --path '.seed_data/[붙임1] 2022년 업체별 명세서 주요정보(23.12.22 기준).xlsx'
python scripts/script_calculate_emissions.py --year_from 2017 --year_to 2020

