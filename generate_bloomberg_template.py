from datagen import generate_tables_alphabetical
from typing import List
from urgewald import urgewald_tickers

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