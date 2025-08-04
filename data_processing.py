import sys

from company_data import FossilFuelCompanyYear


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
    fi_data_dir = sys.argv[1]
    fossil_csv_dir = sys.argv[2]
    output_dir = sys.argv[3]
    years = [int(arg) for arg in sys.argv[4:]]

    main(fi_data_dir, fossil_csv_dir, years, output_dir)