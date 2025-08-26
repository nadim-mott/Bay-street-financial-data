import os
from typing import Any
from utilities import safe_to_float
import csv

DIR_loan_data = "./data/Loan Data"


def get_loan_value(company_name: str, bank: str, year: int) -> float:
    path_to_csv = os.path.join(DIR_loan_data, bank)
    with open(path_to_csv, mode='r', newline='') as source_file:
        reader : Any = csv.reader(source_file)
        reader = (row for row in reader if row and any(cell.strip() for cell in row))
        return sum(safe_to_float(row[3], 0) for row in reader if row[2] != '' and row[2].split('.')[2] in company_name and str(year) in row[1])


if __name__ == "__main__":
    print()