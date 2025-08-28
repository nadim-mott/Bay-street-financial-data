from functools import partial
from extraction_methods.extract_13F_data import get_share_value_from_13F
from extraction_methods.extract_loan_data import get_loan_value
from utilities.urgewald import urgewald_tickers

from extraction_methods.BOCC_IICC import get_IICC_share, get_BOCC_loan

from utilities.sfh import sfh_tickers
from utilities.yahoo import get_yahoo_tickers

FINANCIAL_INSTITUTIONS = [
    # Banks:
    "RBC",
    "BMO", 
    "TD",
    "Scotiabank",
    "CIBC", 
    "National Bank of Canada",
    # Asset Management:
    "Sun Life Financial",
    "Power Corp of Canada",
    "Manulife",
    "Brookfield Asset Management", 
    "Fairfax", 
    "Intact Financial",
    # Pension Funds
    "OMERS",
    "CPPIB",
    "Healthcare of Ontario Pension Plan Trust Fund",
    "OTPP", 
    "OPSEU",
    "Investment Management of Ontario",
]

HOLDINGS_DATA_COLLECTION = lambda ticker, name, fi, year : get_share_value_from_13F(ticker, fi, year, max)
LOAN_DATA_COLLECTION = lambda ticker, name, fi, year : get_loan_value(name, fi, year)

YEARS_OF_INTEREST = [i for i in range(2018,2025)]
FOSSIL_FUEL_TICKERS = urgewald_tickers

# YEARS_OF_INTEREST = [2022]
# FOSSIL_FUEL_TICKERS = sfh_tickers

# HOLDINGS_DATA_COLLECTION = get_IICC_share
# LOAN_DATA_COLLECTION = get_BOCC_loan

# FOSSIL_FUEL_TICKERS = get_yahoo_tickers()