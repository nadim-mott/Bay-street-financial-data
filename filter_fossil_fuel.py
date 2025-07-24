import yfinance as yf
import csv
from typing import Set, Callable
import time
import os
from functools import cmp_to_key

fossil_fuel_symbols : Set[str] = set()
non_fossil_fossil_symbols : Set[str] = set()

import pycountry

# Global caches
fossil_fuel_symbols = set()
non_fossil_fossil_symbols = set()
fossil_fuel_country_codes = set()  # Store tuples: (symbol, bloomberg_code)

# Bloomberg-style suffix mapping for major exchanges
EXCHANGE_TO_BLOOMBERG = {
    # US markets
    "NYSE": "US", "NYS": "US", "NASDAQ": "US", "NMS": "US", "BATS": "US",
    # London Stock Exchange
    "LSE": "LN", "LON": "LN",
    # Euronext Paris
    "EPA": "FP", "PAR": "FP",
    # Frankfurt / Xetra
    "FRA": "GY", "XETRA": "GY", "GER": "GY",
    # Hong Kong
    "HKG": "HK",
    # Tokyo
    "TYO": "JP", "TSE": "JP",
    # Toronto
    "TSE": "CN", "TSX": "CN",
    # Australia (ASX)
    "ASX": "AU",
    # Shanghai/Shenzhen (approximation)
    "SHG": "CH", "SHA": "CH", "SHE": "CH",
}

def _to_bloomberg_code(symbol: str, exchange: str, country: str) -> str:
    """
    Convert Yahoo Finance exchange/country to a Bloomberg-style suffix.
    Uses a predefined exchange mapping first; falls back to ISO country codes.
    """
    exchange = exchange.upper() if exchange else ""
    
    # Use predefined Bloomberg mapping for known exchanges
    if exchange in EXCHANGE_TO_BLOOMBERG:
        return f"{symbol}_{EXCHANGE_TO_BLOOMBERG[exchange]}"
    
    # Otherwise, try ISO Alpha-2 country code
    if country:
        try:
            iso_code = pycountry.countries.lookup(country).alpha_2
            return f"{symbol}_{iso_code}"
        except LookupError:
            pass
    
    # Fallback if nothing else works
    return f"{symbol}_UN"  # UN = Unknown

def is_fossil_fuel_company(symbol: str) -> bool:
    """
    Check if a company is a fossil fuel company by querying Yahoo Finance,
    and store its Bloomberg-style exchange code in `fossil_fuel_country_codes`.
    """
    symbol = symbol.split("/")[0]
    if symbol in fossil_fuel_symbols:
        return True
    elif symbol in non_fossil_fossil_symbols:
        return False

    if not isinstance(symbol, str) or not symbol.strip():
        return False

    for _ in range(3):  # retry up to 3 times
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            sector = str(info.get("sector", "")).lower()
            industry = str(info.get("industry", "")).lower()
            
            fossil_keywords = ["oil", "gas", "coal", "fossil", "petroleum"]

            is_fossil = any(keyword in sector for keyword in fossil_keywords) or \
                        any(keyword in industry for keyword in fossil_keywords)

            if is_fossil:
                fossil_fuel_symbols.add(symbol)
                
                # Retrieve exchange and country
                exchange = info.get("exchange", "")
                country = info.get("country", "")

                # Convert to Bloomberg-style format
                bloomberg_code = _to_bloomberg_code(symbol, exchange, country)
                fossil_fuel_country_codes.add((symbol, bloomberg_code))
                
                return True

            non_fossil_fossil_symbols.add(symbol)
            return False

        except Exception as error:
            print(f"{error}: {symbol}")
            print("pausing for request limit")
            time.sleep(5 * 60)
            print("Resuming.")

    non_fossil_fossil_symbols.add(symbol)
    return False



def filter_csv(source_path: str, destination_path: str, top_number: int = -1) -> None:
    """
    Given a path to a csv file, filter the CSV to only include fossil fuel 
    companies and save it as a new csv

    if top_number >= 0 only report the first top_number of fossil fuel companies
    based on the order of the csv
    """
    number_of_fossil_fuels_needed = top_number
    with open(source_path, mode ='r', newline='')as source_file:
        reader = csv.reader(source_file)
        with open(destination_path, mode= 'w', newline='')as destination_file:
            writer = csv.writer(destination_file)
            writer.writerow(next(reader)) # copy header
            for line in reader:
                ticker = line[0]
                is_fossil_fuel = is_fossil_fuel_company(ticker)
                if is_fossil_fuel:
                    number_of_fossil_fuels_needed -= 1
                    # include
                    writer.writerow(line)
                if number_of_fossil_fuels_needed <= 0:
                    return


def reorder_csv(source_path: str, destination_path: str, column_index: int, comparison_function: Callable = lambda a,b : float(a) >= float(b) ) -> None:
    """
    Helper function, given a path to a csv file, reorder the rows such that they are sorted according to comparison_function
    where comparison_function(a,b) = true => a is before b in the destination csv. column_index is the column index (starting with 0)
    """
    with open(source_path, newline='', encoding='utf-8') as src_file:
        reader = list(csv.reader(src_file))
        
        if not reader:
            # Empty file, just write back an empty file
            with open(destination_path, 'w', newline='', encoding='utf-8') as dest_file:
                pass
            return

        header, rows = reader[0], reader[1:]

    def compare(row_a, row_b):
        val_a, val_b = row_a[column_index], row_b[column_index]
        # Attempt to convert to float for numeric sorting
        try:
            return -1 if comparison_function(val_a, val_b) else 1
        except:
            return 1

    sorted_rows = sorted(rows, key=cmp_to_key(compare))

    # Write the reordered CSV
    with open(destination_path, 'w', newline='', encoding='utf-8') as dest_file:
        writer = csv.writer(dest_file)
        writer.writerow(header)
        writer.writerows(sorted_rows)


def reorder_bulk_csv(source_root: str, destination_root: str, column_index: int,  comparison_function: Callable = lambda a, b : float(a.replace(',', '')) >= float(b.replace(',', ''))) -> None:
    """
    Given a path to a source directory, sort all the csv to using the comparison_function
    where comparison_function(a,b) = true => a is before b in the destination csv. column_index is the column index (starting with 0) 
    save the new ones to a new directory.
    
    New CSV names match the old names with '_sorted' appended at the end.
    For example if a csv is in 'source_root/directory/data.csv' would be saved
    as 'destination_root/directory/data_sorted.csv'
    """
    for root, _, files in os.walk(source_root):
        for file in files:
            if file.lower().endswith(".csv"):
                # Construct source file path
                source_path = os.path.join(root, file)

                # Preserve subdirectory structure under destination_root
                rel_dir = os.path.relpath(root, source_root)
                dest_dir = os.path.join(destination_root, rel_dir)
                os.makedirs(dest_dir, exist_ok=True)

                
                name, ext = os.path.splitext(file)
                dest_file = f"{name}_sorted{ext}"
                destination_path = os.path.join(dest_dir, dest_file)

                print(f"Sorting {source_path}...")
                reorder_csv(source_path, destination_path, column_index, comparison_function)
                print(f"Sorted to {destination_path}")


def filter_bulk_csv(source_root: str, destination_root: str, top_number : int = -1) -> None:
    """
    Given a path to a source directory, filter all the csv to only include 
    fossil fuel companies and save the new ones to a new directory.
    
    New CSV names match the old names with '_fossil_fuel' appended at the end.
    For example if a csv is in 'source_root/directory/data.csv' would be saved
    as 'destination_root/directory/data_fossil_fuel.csv'
    """
    for root, _, files in os.walk(source_root):
        for file in files:
            if file.lower().endswith(".csv"):
                # Construct source file path
                source_path = os.path.join(root, file)

                # Preserve subdirectory structure under destination_root
                rel_dir = os.path.relpath(root, source_root)
                dest_dir = os.path.join(destination_root, rel_dir)
                os.makedirs(dest_dir, exist_ok=True)

                
                name, ext = os.path.splitext(file)
                dest_file = f"{name}_fossil_fuel{ext}"
                destination_path = os.path.join(dest_dir, dest_file)

                print(f"Filtering {source_path}...")
                filter_csv(source_path, destination_path, top_number)
                print(f"Filtered to {destination_path}")



if __name__ == "__main__":
    # filter_csv("data/raw_data/test.csv", "./data/filtered_data/test.csv", top_number = 2)
    # reorder_bulk_csv("./data/raw_data", "./data/sorted_by_value", 4)
    filter_bulk_csv("./data/sorted_by_value", "./data/filtered_data", top_number = 20)
    print(f"found {len(fossil_fuel_symbols)} tickers")
    print(f"tickers are {"+".join(company[1] for company in list(fossil_fuel_country_codes))}")