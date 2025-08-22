import sys

from company_data import FossilFuelCompanyYear
from functools import partial
from extract_13F_data import get_share_value_from_13F
from generate_bloomberg_template import urgewald_tickers

HOLDINGS_DATA_COLLECTION = partial(get_share_value_from_13F, aggregation_method=sum)
FINANCIAL_INSTITUTIONS = [
    "BMO", 
    "Brookfield Asset Management", 
    "CIBC", 
    "Fairfax", 
    "Healthcare of Ontario Pension Plan Trust Fund",
    "Intact Financial",
    "Investment Management of Ontario",
    "Manulife",
    "National Bank of Canada",
    "OMERS",
    "OPSEU",
    "OTPP",
    "Power Corp of Canada",
    "RBC",
    "Scotiabank",
    "TD"
]


import os
from typing import List

def main(fi_data_dir: str, fossil_csv_dir: str, years: List[int], output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for year in years:
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)

        for filename in os.listdir(fossil_csv_dir):
            if not filename.endswith(".csv"):
                continue

            company_csv_path = os.path.join(fossil_csv_dir, filename)
            try:
                company = FossilFuelCompanyYear(company_csv_path, fi_data_dir, year)
                output_path = os.path.join(year_dir, f"{company.ticker}_{year}.csv")
                company.export_with_financed_data_to_csv(output_path)
            except StopIteration:
                print(f"[WARN] Skipping {filename}: no data for year {year}")
            except Exception as e:
                print(f"[ERROR] Failed processing {filename} for year {year}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        fi_data_dir = "data/13f_data"
        fossil_csv_dir = "data/Bloomberg"
        output_dir = "data/processed_fi_info"
    else:
        fi_data_dir = sys.argv[1]
        fossil_csv_dir = sys.argv[2]
        output_dir = sys.argv[3]
    years = [int(arg) for arg in sys.argv[4:]]


    main(fi_data_dir, fossil_csv_dir, years, output_dir)