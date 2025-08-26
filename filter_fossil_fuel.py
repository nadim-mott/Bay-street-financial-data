
import csv
from typing import Set, Callable, Tuple, Optional, Any, Dict
import os
from functools import cmp_to_key
from utilities import print_cond, contains_which
from datagen import generate_tables


urgewald_tickers = []
with open("data/urgewald GOGEL 2024.csv", 'r', encoding='iso-8859-1') as file:
    reader = csv.reader(file)
    found_ticker_index = False
    found_business_sector = False
    while not found_ticker_index or not found_business_sector:
        try:
            row = list(next(reader))
            if not found_business_sector:
                business_sector_index = row.index("Primary Business Sectors")
                found_business_sector = True
            bb_ticker_index = row.index("BB Ticker")
            found_ticker_index = True
        except ValueError:
            pass
        except StopIteration:
            raise Exception("Make sure the Urgewald file has a column 'BB Ticker' and Primary Business Sectors")
    tickers = [line[bb_ticker_index] for line in reader if line[bb_ticker_index] != "! - n.a." and line[bb_ticker_index] != "" and line[bb_ticker_index] != " " and "Oil & Gas" in line[business_sector_index]]
    urgewald_tickers.extend(tickers)

with open("data/urgewald GCEL 2024 for FI.csv", encoding='iso-8859-1') as file:
    reader = csv.reader(file)
    found_ticker_index = False
    found_business_sector = False
    while not found_ticker_index or not found_business_sector:
        try:
            row = list(next(reader))
            if not found_business_sector:
                business_sector_index = row.index("Coal Industry Sector")
                found_business_sector = True
            bb_ticker_index = row.index("BB Ticker")
            found_ticker_index = True
        except ValueError:
            pass
        except StopIteration:
            raise Exception("Make sure the Urgewald file has a column 'BB Ticker'")
    tickers = [line[bb_ticker_index] for line in reader if line[bb_ticker_index] != "! - n.a." and line[bb_ticker_index] != "" and line[bb_ticker_index] != " "]
    urgewald_tickers.extend(tickers)


def is_urgewald(ticker: str) -> Optional[Tuple[str,str]]:
    for urgewald_ticker in urgewald_tickers:
        if urgewald_ticker.split(" ")[0] == ticker.split(".")[0]:
            return ticker, urgewald_ticker
    return None

def filter_csv(source_path: str, destination_path: str, top_number: int = -1, filter_method : Callable[[str], Optional[Tuple[str,str]]] = is_urgewald) -> Set[Tuple[str, str]]:
    """
    Given a path to a csv file, filter the CSV to only include fossil fuel 
    companies and save it as a new csv

    if top_number >= 0 only report the first top_number of fossil fuel companies
    based on the order of the csv

    return a set containing all fossil fuel companies and tickers
    """
    number_of_fossil_fuels_needed = top_number
    bloomberg_codes : Set[Tuple[str, str]] = set()
    with open(source_path, mode ='r', newline='')as source_file:
        reader = csv.reader(source_file)
        with open(destination_path, mode= 'w', newline='')as destination_file:
            writer = csv.writer(destination_file)
            writer.writerow(next(reader)) # copy header
            for line in reader:
                ticker = line[0]
                bloomberg_code = filter_method(ticker)
                if bloomberg_code is not None:
                    number_of_fossil_fuels_needed -= 1
                    # include
                    bloomberg_codes.add(bloomberg_code)
                    writer.writerow(line)
                if number_of_fossil_fuels_needed == 0:
                    return bloomberg_codes

    return bloomberg_codes




def reorder_csv(source_path: str, destination_path: str, column_index: int, comparison_function: Callable[[Any, Any], bool] = lambda a,b : float(a) >= float(b) ) -> None:
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


def reorder_bulk_csv(source_root: str, destination_root: str, column_index: int,  comparison_function: Callable = lambda a, b : float(a.replace(',', '')) >= float(b.replace(',', '')), verbose = False) -> None:
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

                print_cond(verbose, f"Sorting {source_path}...")
                reorder_csv(source_path, destination_path, column_index, comparison_function)
                print_cond(verbose, f"Sorted to {destination_path}")




def filter_bulk_csv(source_root: str, destination_root: str, top_number : int = -1, filter_method : Callable[[str], Optional[Tuple[str,str]]] = is_urgewald, verbose = False) -> Dict[str, Set[Tuple[str, str]]]:
    """
    Given a path to a source directory, filter all the csv to only include 
    fossil fuel companies and save the new ones to a new directory.
    
    New CSV names match the old names with '_fossil_fuel' appended at the end.
    For example if a csv is in 'source_root/directory/data.csv' would be saved
    as 'destination_root/directory/data_fossil_fuel.csv'

    return a set containing all fossil fuel companies and bloomberg codes
    """
    bloomberg_codes : Dict[str, Set[Tuple[str, str]]] = {}
    for root, _, files in os.walk(source_root):
        for file in files:
            if file.lower().endswith(".csv"):

                year = contains_which(file, list(map(str, range(2018, 2025))))
                if year is None:
                    raise ValueError(f"Could not find year for: {file} Make sure that each 13F file has the year in it's name")
                if year not in bloomberg_codes:
                    bloomberg_codes[year] = set()
                # Construct source file path
                source_path = os.path.join(root, file)

                # Preserve subdirectory structure under destination_root
                rel_dir = os.path.relpath(root, source_root)
                dest_dir = os.path.join(destination_root, rel_dir)
                os.makedirs(dest_dir, exist_ok=True)

                
                name, ext = os.path.splitext(file)
                dest_file = f"{name}_fossil_fuel{ext}"
                destination_path = os.path.join(dest_dir, dest_file)

                print_cond(verbose, f"Filtering {source_path}...")
                bloomberg_codes[year] |= filter_csv(source_path, destination_path, top_number, filter_method)
                print_cond(verbose, f"Filtered to {destination_path}")
    return bloomberg_codes


if __name__ == "__main__":
    reorder_bulk_csv("./data/13f_data", "./data/sorted_by_value", 4)
    fossil_fuel_country_codes = filter_bulk_csv("./data/sorted_by_value", "./data/filtered_data", top_number = -1, filter_method = is_urgewald, verbose = True)
    print(f"found {len(fossil_fuel_country_codes)} tickers")
    for year in fossil_fuel_country_codes:
        codes = fossil_fuel_country_codes[year]
        print(f"for year: {year} found {len(codes)} tickers, the tickers are {"+".join(company[1].replace(" ", "_") for company in list(codes))}\n")
        generate_tables([company[1] for company in list(codes)], [int(year)])

    