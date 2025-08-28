import os
from typing import Any
from utilities.helper_functions import safe_to_float
import csv

DIR_loan_data = "./data/BOCC Big 5"
DIR_share_data = "./data/IICC"


def get_BOCC_loan(ticker: str, company_name: str, bank: str, year: int) -> float:
    path_to_csv = os.path.join(DIR_loan_data, bank+".csv")
    try:
        with open(path_to_csv, mode='r', newline='') as source_file:
            reader : Any = csv.reader(source_file)
            reader = (row for row in reader if row and any(cell.strip() for cell in row))
            return sum(safe_to_float(row[2], 0) for row in reader if row[2] != '' and row[1].lower() in ticker.lower() and year==2022)
    except FileNotFoundError:
        return 0

def get_IICC_share(ticker: str, company_name: str, fi: str, year: int) -> float:
    path_to_csv = os.path.join(DIR_share_data, fi+".csv")
    try:
        with open(path_to_csv, mode='r', newline='') as source_file:
            reader : Any = csv.reader(source_file)
            reader = (row for row in reader if row and any(cell.strip() for cell in row))
            return sum(safe_to_float(row[3], 0) * safe_to_float(row[1], 0) for row in reader if row[0] != '' and row[0].lower() in company_name.lower() and year==2022)
    except FileNotFoundError:
        return 0
