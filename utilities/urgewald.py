import csv

urgewald_tickers_set = set()
with open("data/input_data/tickers/urgewald GOGEL 2024.csv", 'r', encoding='iso-8859-1') as file:
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
    tickers = {line[bb_ticker_index] for line in reader if  line[bb_ticker_index] != "ticker" and line[bb_ticker_index] != "! - n.a." and line[bb_ticker_index] != "" and line[bb_ticker_index] != " " and "Oil & Gas" in line[business_sector_index]}
    urgewald_tickers_set |= tickers

with open("data/input_data/tickers/urgewald GCEL 2024 for FI.csv", encoding='iso-8859-1') as file:
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
    tickers = {line[bb_ticker_index] for line in reader if line[bb_ticker_index] != "! - n.a." and line[bb_ticker_index] != "" and line[bb_ticker_index] != " "}
    urgewald_tickers_set |= tickers

urgewald_tickers = list(urgewald_tickers_set)