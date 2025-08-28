import csv

with open("data/input_data/tickers/SFH_data.csv", 'r', encoding='iso-8859-1') as file:
    reader = csv.reader(file)
    next(reader)
    sfh_tickers = [row[19] for row in reader]