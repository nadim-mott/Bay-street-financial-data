import xlsxwriter
import os
import traceback
from typing import List
from utilities import print_cond
from string import ascii_lowercase

# Fields to include in columns (column label and Bloomberg field)
fields = [
    ("GHG_SCOPE_1", "B"),
    ("GHG_SCOPE_2_LOCATION_BASED", "C"),
    ("GHG_SCOPE_3", "D"),
    ("SCOPE_3_PURCH_GOODS_SRVCS", "E"),
    ("SCOPE_3_CAPITAL_GOODS", "F"),
    ("SCOPE_3_FUEL_ENRG_RELATD_ACT", "G"),
    ("SCOPE_3_UPSTREAM_TRANS_DIST", "H"),
    ("SCOPE_3_WASTE_GENRTD_IN_OP", "I"),
    ("SCOPE_3_BUSINESS_TRVL_EMISSIONS", "J"),
    ("SCOPE_3_EMPLOYEE_COMMUTING", "K"),
    ("SCOPE_3_UPSTREAM_LEASED_ASSETS", "L"),
    ("SCOPE_3_DWNSTRM_TRANS_DIST", "M"),
    ("SCOPE_3_PRCSS_OF_SOLD_PRODS", "N"),
    ("SCOPE_3_USE_SOLD_PRODUCTS", "O"),
    ("SCOPE_3_EOL_TRTMNT_PRODS", "P"),
    ("SCOPE_3_DWNSTRM_LEASE_ASSTS", "Q"),
    ("SCOPE_3_FRANCHISES", "R"),
    ("SCOPE_3_INVESTMENTS", "S"),
    ("SCOPE_3_EMISSIONS_OTHER", "T"),
    ("ENTERPRISE_VALUE", "U"),
    ("IS_COMP_SALES", "V"),
    ("HISTORICAL_MARKET_CAP", "W"),
    ("NAME", "X", "BDP"),
    ("IS_AVG_NUM_SH_FOR_EPS", "Y"),
    ("PX_LAST", "Z"),
    ("SHORT_AND_LONG_TERM_DEBT", "AA"),
    ("CASH_AND_MARKETABLE_SECURITIES", "AB"),
    ("BS_TOT_ASSET", "AC"),
]

directory = "data/Bloomberg_template"


def col_index_to_excel_col(index: int) -> str:
    """Convert 0-based column index to Excel-style column letters (e.g., 0 -> 'A', 27 -> 'AB')"""
    result = ''
    while index >= 0:
        result = chr(index % 26 + ord('A')) + result
        index = index // 26 - 1
    return result


def generate_tables_alphabetical(tickers: List[str], years: List[int], verbose=False):
    tickers_copy = tickers.copy()
    for char in ascii_lowercase:
        indexes = [i for i in range(len(tickers_copy)) if tickers_copy[i].lower().startswith(char)]
        indexes.sort()
        indexes.reverse()
        # sort and reverse list so that the later indexes are first to avoid issues when popping
        tickers_of_char = [tickers_copy.pop(i) for i in indexes]
        generate_tables_of_size(tickers_of_char, years, 428, verbose, f'GHG_emissions_{char}')
    generate_tables_of_size(tickers_copy, years, 428, verbose, f'GHG_emissions_others')

def generate_tables_of_size(tickers: List[str], years: List[int], max_size: int, verbose=False, name = "GHG_Emission"):
    chunks = [tickers[x:x+max_size] for x in range(0, len(tickers), max_size)]
    for i in range(len(chunks)):
        chunk = chunks[i]
        generate_table(chunk, years, verbose, name=name+"_"+str(i))


def generate_tables(tickers: List[str], years: List[int], verbose=False):
    os.makedirs(directory, exist_ok=True)

    for ticker in tickers:
        try:
            sanitized_ticker = ticker.replace("/", "-")
            workbook = xlsxwriter.Workbook(f'{directory}/GHG_Emissions_{sanitized_ticker}.xlsx')
            worksheet = workbook.add_worksheet()

            for i, year in enumerate(years):
                row = i + 1  # Excel rows are 1-indexed
                worksheet.write(f'A{row}', f'{ticker} {year}')
                
                # Write environmental + financial fields
                for field in fields:
                    field_name = field[0]
                    col = field[1]
                    formula_type = field[2] if len(field) == 3 else "BDH"
                    if formula_type == "BDP":
                        formula = f'=BDP("{ticker}", "{field_name}")'
                    else:
                        formula = f'=BDH("{ticker}", "{field_name}", "FY {year}")'
                    worksheet.write(f'{col}{row}', formula)

                # Offset to place financial institution data after existing fields
                start_col_index = len(fields) + 1

            print_cond(verbose, f'\nA new .xlsx file for {ticker} from {years[0]}–{years[-1]} has been successfully created.')
            workbook.close()
        except Exception as e:
            print(f'\nProcess failed for {ticker}! Error: {e}')
            traceback.print_exc()

def generate_table(tickers: List[str], years: List[int], verbose=False, name='GHG_Emission'):
    os.makedirs(directory, exist_ok=True)
    workbook = xlsxwriter.Workbook(f'{directory}/{name}.xlsx')
    worksheet = workbook.add_worksheet()
    row = 1 # Excel rows are 1-indexed
    for ticker in tickers:
        try:
            for i, year in enumerate(years):
                worksheet.write(f'A{row}', f'{ticker} {year}')
                # Write environmental + financial fields
                for field in fields:
                    field_name = field[0]
                    col = field[1]
                    formula_type = field[2] if len(field) == 3 else "BDH"
                    if formula_type == "BDP":
                        formula = f'=BDP("{ticker}", "{field_name}")'
                    else:
                        formula = f'=BDH("{ticker}", "{field_name}", "FY {year}")'
                    worksheet.write(f'{col}{row}', formula)

                # Offset to place financial institution data after existing fields
                start_col_index = len(fields) + 1
                row += 1
        except Exception as e:
            print(f'\nProcess failed for {ticker}! Error: {e}')
            traceback.print_exc()
    workbook.close()
        

def generate_tables_with_fi(tickers: List[str], years: List[int], banks: List[str], financial_institutions: List[str], verbose=False):
    os.makedirs(directory, exist_ok=True)

    for ticker in tickers:
        try:
            sanitized_ticker = ticker.replace("/", "-")
            workbook = xlsxwriter.Workbook(f'{directory}/GHG_Emissions_{sanitized_ticker}.xlsx')
            worksheet = workbook.add_worksheet()

            for i, year in enumerate(years):
                row = i + 1  # Excel rows are 1-indexed
                worksheet.write(f'A{row}', f'{ticker} {year}')
                
                # Write environmental + financial fields
                for field in fields:
                    field_name = field[0]
                    col = field[1]
                    formula_type = field[2] if len(field) == 3 else "BDH"
                    if formula_type == "BDP":
                        formula = f'=BDP("{ticker}", "{field_name}")'
                    else:
                        formula = f'=BDH("{ticker}", "{field_name}", "FY {year}")'
                    worksheet.write(f'{col}{row}', formula)

                # Offset to place financial institution data after existing fields
                start_col_index = len(fields) + 1

                # Add Bank Loan/Bond exposure
                for j, bank_ticker in enumerate(banks):
                    col_letter = col_index_to_excel_col(start_col_index + j)
                    formula = f'=BDP("{bank_ticker} Equity", "BANK_LOAN_TO_{ticker}")'
                    worksheet.write(f'{col_letter}{row}', formula)

                # Add Financial Institution Shareholding
                fi_offset = start_col_index + len(banks)
                for k, fi_ticker in enumerate(financial_institutions):
                    col_letter = col_index_to_excel_col(fi_offset + k)
                    formula = f'=BDP("{fi_ticker} Equity", "HOLDINGS_VALUE_IN_{ticker}")'
                    worksheet.write(f'{col_letter}{row}', formula)

            print_cond(verbose, f'\nA new .xlsx file for {ticker} from {years[0]}–{years[-1]} has been successfully created.')
            workbook.close()
        except Exception as e:
            print(f'\nProcess failed for {ticker}! Error: {e}')
            traceback.print_exc()






# if __name__ == "__main__":
#     print("\nWelcome to the GHG Emissions DataGen Tool!\nThis can be used to generate .xlsx files that when accessed through a Microsoft Excel session with a Bloomberg Terminal plugin, will output the company's most recent GHG emissions data.\n")

#     tickers_input = input(
#         "Enter the ticker, then an underscore, then the Bloomberg exchange country code for your desired company. "
#         "For example for Microsoft you would enter MSFT_US. "
#         "If you want to generate the template sheets for multiple companies use a '+' to separate them like this: XOM_US+CNQ_CN+SU_CN.\n\n"
#     )
#     tickers = tickers_input.upper().replace("_", " ").split("+")
#     years = list(range(2023, 2017, -1))
#     generate_tables(tickers, years, True)
#     print("\nTask fully completed!!\n")