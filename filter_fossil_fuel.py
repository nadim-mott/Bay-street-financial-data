import yfinance as yf
import csv
from typing import Set, Callable
import time
import os
from functools import cmp_to_key

fossil_fuel_symbols : Set[str] = set()
non_fossil_fossil_symbols : Set[str] = set()
def is_fossil_fuel_company(symbol: str) -> bool:
    """
    Check if a company (given a ticker) is likely a fossil fuel company
    by querying Yahoo Finance for its sector and industry classification.
    Code written with the help of chatGPT.
    
    Doctests:
    >>> print(is_fossil_fuel_company("XOM"))
    True
    >>> print(is_fossil_fuel_company("CVX"))
    True
    >>> print(is_fossil_fuel_company("EFA"))
    False

    Returns True if the sector or industry matches oil, gas, coal, or fossil fuels.
    """
    if symbol in fossil_fuel_symbols:
        return True
    elif symbol in non_fossil_fossil_symbols:
        return False

    if not isinstance(symbol, str) or not symbol.strip():
        return False
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        sector = str(info.get("sector", "")).lower()
        industry = str(info.get("industry", "")).lower()
        
        # Check for energy-related sectors/industries
        fossil_keywords = ["oil", "gas", "coal", "fossil", "petroleum", "energy"]
        
        if any(keyword in sector for keyword in fossil_keywords):
            fossil_fuel_symbols.add(symbol)
            return True
        if any(keyword in industry for keyword in fossil_keywords):
            fossil_fuel_symbols.add(symbol)
            return True
        
    except Exception as error:
        # If ticker lookup fails, default to False
        print(f"{error}: {symbol} defaulting to not fossil fuel")
        non_fossil_fossil_symbols.add(symbol)
        return False
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
    # filter_csv("data/raw_data/test.csv", "./data/filtered_data/test.csv")
    reorder_bulk_csv("./data/raw_data", "./data/sorted_by_value", 4)
    filter_bulk_csv("./data/sorted_by_value", "./data/filtered_data", top_number = 20)