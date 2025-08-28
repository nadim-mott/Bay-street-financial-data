import os
from typing import Any
from utilities.helper_functions import safe_to_float
import csv

DIR_loan_data = "./data/Loan Data"


def get_loan_value(company_name: str, bank: str, year: int) -> float:
    path_to_csv = os.path.join(DIR_loan_data, bank+".csv")
    try:
        with open(path_to_csv, mode='r', newline='') as source_file:
            reader : Any = csv.reader(source_file)
            reader = (row for row in reader if row and any(cell.strip() for cell in row))
            return sum(safe_to_float(row[4], 0) for row in reader if row[2] != '' and row[2].lower() in company_name.lower() and str(year) in row[1])
    except FileNotFoundError:
        return 0

if __name__ == "__main__":
    print(get_loan_value("American Tower Corp","RBC", 2018))