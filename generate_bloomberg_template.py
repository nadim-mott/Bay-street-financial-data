import csv
from datagen import generate_table, generate_tables_with_fi, generate_tables_alphabetical
from typing import List

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

banks = ["RY", "BMO","TD", "BNS", "CM", "NA", "SLF", "POW", "MFC", "BN", "FFH", "IFC"]
pensions = ["OMERS", "CPPIB", "HLTHON"]
asset_managements = ["SLF", "POW", "MFC", "BN", "FFH", "IFC"]
bank_tickers = [ticker + "CN Equity" for ticker in banks]
pension_tickers = [ticker + "CN Equity" for ticker in pensions]
asset_management_tickers = [ticker + "CN Equity" for ticker in asset_managements]

all_fi_tickers = []
all_fi_tickers.extend(bank_tickers)
all_fi_tickers.extend(asset_managements)
all_fi_tickers.extend(pension_tickers)

all_tickers : List[str] = []
generate_tables_alphabetical(urgewald_tickers, list(range(2018, 2025)), True)