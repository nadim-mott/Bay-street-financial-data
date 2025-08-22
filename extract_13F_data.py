import os
import csv
from utilities import safe_to_float
from typing import Any

def get_share_value_from_13F(company_ticker : str , financial_institution_name : str, year : int, aggregation_method = sum) -> float:
    DIR_13F = './data/13f_data'

    company_directory = os.path.join(DIR_13F, financial_institution_name)
    return get_share_value_from_directory(company_ticker, company_directory, year, aggregation_method=aggregation_method)

def get_share_value_from_directory(company_ticker: str, directory: str, year: int, aggregation_method = sum)->float:
    aggregated_so_far = 0
    for filename in os.listdir(directory):  
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and str(year) in filename:
            aggregated_so_far = aggregation_method((get_share_value_from_management_csv(company_ticker, filepath), aggregated_so_far))
        elif os.path.isdir(filepath):
            aggregated_so_far = aggregation_method((get_share_value_from_directory(company_ticker, filepath, year), aggregated_so_far))
    return aggregated_so_far



def get_share_value_from_management_csv(company_ticker: str, path_to_csv: str) -> float:
    with open(path_to_csv, mode='r', newline='') as source_file:
        reader : Any = csv.reader(source_file)
        reader = (row for row in reader if row and any(cell.strip() for cell in row))
        return sum(safe_to_float(row[6], 0) for row in reader if row[0] != '' and row[0].split('.')[0] in company_ticker)


if __name__ == "__main__":
    banks = ["RBC", "CIBC", "TD", "BMO", "Scotiabank"]
    company_names = ["Suncor", "Chevron", "Enbridge", "EQT", "Exxon"]
    company_tickers = ["SU", "CVX", "ENB", "EQT", "XOM"]
    years = [year for year in range(2019, 2025)]
    for i in range(len(company_names)):
        company_name = company_names[i]
        company_ticker = company_tickers[i]
        print("\n")
        print(company_name+":")
        print("\n")
        print("|Holder name:|" + "|".join(str(year) for year in years) + "|")
        print("| ---- | --- | --- | ---| ----| ---- | ---- |")
        for bank in banks:
            all_shares = []
            for year in years:
                all_shares.append(get_share_value_from_13F(company_ticker, bank, year))
            print(f"|{bank}|{"|".join(str(share) for share in all_shares)} |")
                