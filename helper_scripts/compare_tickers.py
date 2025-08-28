from utilities.urgewald import urgewald_tickers
from utilities.sfh import sfh_tickers
ticker1 = urgewald_tickers
ticker2 = sfh_tickers

missing = [ticker for ticker in ticker2 if not any(ticker in t for t in ticker1)]

print(f"The following {len(missing)} tickers are missing from urgewald: {missing}")