import sys

from company_data import FossilFuelCompanyYear

from generate_bloomberg_template import urgewald_tickers

import os
from typing import List


YEARS_OF_INTEREST = (str(i) for i in range(2018,2024))



def main(fossil_csv_dir: str, years: List[int], output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for year in years:
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)

        for filename in os.listdir(fossil_csv_dir):
            if not filename.endswith(".csv"):
                continue

            company_csv_path = os.path.join(fossil_csv_dir, filename)
            try:
                print(f"Creating company from file {company_csv_path}, {year}")
                company = FossilFuelCompanyYear(company_csv_path, year)
                output_path = os.path.join(year_dir, f"{company.ticker}_{year}.csv")
                company.export_with_financed_data_to_csv(output_path)
                print("success!")
            except StopIteration:
                print(f"[WARN] Skipping {filename}: no data for year {year}")
            except Exception as e:
                print(f"[ERROR] Failed processing {filename} for year {year}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        fossil_csv_dir = "data/Bloomberg"
        output_dir = "data/processed_fi_info"
    else:
        fossil_csv_dir = sys.argv[1]
        output_dir = sys.argv[2]
    years = YEARS_OF_INTEREST


    main(fossil_csv_dir, years, output_dir)