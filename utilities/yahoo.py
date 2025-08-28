import yfinance as yf
import pycountry
from typing import Tuple, Optional, List
import time

# Global caches
fossil_fuel_symbols = set()
non_fossil_fossil_symbols = set()

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

def is_fossil_fuel_company(symbol: str) -> Optional[Tuple[str,str]]:
    """
    Check if a company is a fossil fuel company by querying Yahoo Finance,
    and store its Bloomberg-style exchange code in `fossil_fuel_country_codes`.
    return the bloomberg ticker and country code if true, return None if not
    fossil fuel.
    """
    symbol = symbol.split("/")[0]
    if symbol in non_fossil_fossil_symbols:
        return None

    if not isinstance(symbol, str) or not symbol.strip():
        return None

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
                
                return (symbol, bloomberg_code)

            non_fossil_fossil_symbols.add(symbol)
            return None

        except Exception as error:
            print(f"{error}: {symbol}")
            print("pausing for request limit")
            time.sleep(5 * 60)
            print("Resuming.")

    non_fossil_fossil_symbols.add(symbol)
    return None

def get_yahoo_tickers() -> List[str]:
    with open("./data/tickers/yahoo_tickers.txt") as f:
        return f.read().split("\n")