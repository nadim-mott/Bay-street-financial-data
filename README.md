# Data extractor Read me.

## Overview:
This repository contains code necessary for generating a dataset similar to the one that was used for the Bay Street Report 2024.

## Step by step instructions:

### Step 1: Download the CSV data from 13f.info 


On 13f.info, find the company you are interested in, then download the csv for the final quarter of each year you would like to analyze. Put each year's report in a directory for that company. Ensure that the year is in the name of each respective csv file. You may feel free to use subdirectories as you please, so long as the name of the parent directory matches the name of the company you are interested in

Place each company's directory in the directory data/13f_data.

### Step 2 (Optional):

Request GCEL with financial indicators and GOGEL with financial indicators from Urgewald. These lists are also publicly available but these scripts will require the use of indicators not present in the public files (such as the bloomberg indicators), if these lists cannot be made available, you may also use the provided substitute functions using yahoo finance or using the company set from the Bay Street Report 2024.

To use the company set from Bay Street Report 2024, go to global_values.py and make the following changes:

```python
# 1: comment out the urgwald tickers
# FOSSIL_FUEL_TICKERS = urgewald_tickers

# 2: uncomment the sfh tickers
FOSSIL_FUEL_TICKERS = sfh_tickers
```


### Step 3: run datagen.py

run:
```bash
python -m datagen
```

This will generate bloomberg templates in data/Bloomberg_template

If you wish to use companies from yahoo finance, you should instead run the helper script "filter_fossil_fuel"

```bash
python -m filter_fossil_fuel
```

Optionally, you may pass in as an argument the number of fossil fuel companies you wish to find per 13F file if you wish to replicate the methods of the Bay Street Report 2024 where we focused on the top 20 fossil fuel companies for each financial institution. Then make sure to update global_values.py:
```python
# 1: comment out the urgwald tickers
# FOSSIL_FUEL_TICKERS = urgewald_tickers

# 2: uncomment the yahoo tickers
FOSSIL_FUEL_TICKERS = get_yahoo_tickers()
```



### Step 4: Collect data from bloomberg Terminal

Find a computer with the bloomberg plugin for Excel, if you use the templates provided, they should populate with the desired data.

### Step 5: run data_processing.py

Place the data generated from the bloomberg Terminal into the directory "data/Bloomberg" and run data_processing.py.

```bash
python -m data_processing
```


Your data should be processed to data/processed_fi_info and data/seritalized_fi_data