# Data extractor Read me.

## Overview:
This repository contains code necessary for generating a dataset similar to the one that was used for the Bay Street Report 2024.

## Step by step instructions:

### Step 1: Download the CSV data from 13f.info 

TODO: automate this process using EDGAR

TODO: add support for "investment" pages

TODO: add support for Sedar+ files

On 13f.info, find the company you are interested in, then download the csv for the final quarter of each year you would like to analyze. Put each year's report in a directory for that company. Ensure that the year is in the name of each respective csv file.

Place each company's directory in the directory data/13f_data.

Here are the listings used in the current dataset.

TODO: figure out what should be done with companies with multiple filings.

| financial Institution | Dataset url |
| --- | --- |
| RBC | https://13f.info/manager/0001000275-royal-bank-of-canada |
| BMO | https://13f.info/manager/0000927971-bank-of-montreal-can
| TD | https://13f.info/manager/0000947263-toronto-dominion-bank
|Scotiabank | https://13f.info/manager/0001335644-scotia-capital-inc
| CIBC | https://13f.info/manager/0001421224-cibc-world-market-inc
|National Bank of Canada | https://13f.info/manager/0000926171-national-bank-of-canada-fi
| --- | --- |
| Sun Life | https://13f.info/cusip/86738J106
| Power Corporation of Canada | https://13f.info/manager/0000801166-power-corp-of-canada
| Manulife Financial | https://13f.info/cusip/56501R106 |
| Brookfield Asset Management | https://13f.info/manager/0001001085-brookfield-corp-on
| Fairfax Financial | https://13f.info/manager/0000915191-fairfax-financial-holdings-ltd-can |
| Intact Financial | https://13f.info/manager/0001443077-intact-investment-management-inc |
| --- | --- |
| OMERS |  https://13f.info/manager/0001053321-omers-administration-corp |
| CPPIB | https://13f.info/manager/0001283718-canada-pension-plan-investment-board |
| HOOPP | https://13f.info/manager/0001535845-healthcare-of-ontario-pension-plan-trust-fund
| OTPP | https://13f.info/manager/0000937567-ontario-teachers-pension-plan-board |
| OPSEU | https://13f.info/manager/0001632810-opseu-pension-plan-trust-fund
| IMCO | https://13f.info/manager/0001811568-investment-management-corp-of-ontario |

### Step 2 (Optional):

Request GCEL with financial indicators and GOGEL with financial indicators from Urgewald. These lists are also publicly available but these scripts will require the use of indicators not present in the public files (such as the bloomberg indicators), if these lists cannot be made available, you may also use the provided substitute functions using yahoo finance.

### Step 3: run filter_fossil_fuel.py

Next run the filter_fossil_fuel.py, this will first sort the csvs such that the companies with the highest share values are listed first (by default this is sorted in data/sorted_by_value). Then it will generate a folder containing bloomberg value templates.

TODO: Add a way to specify whether using yahoo or Urgewald to decide which fossil fuels we are interested in.

### Step 4: Collect data from bloomberg Terminal

Find a computer with the bloomberg plugin for Excel, if you use the templates provided, they should populate with the desired data.

### Step 5: run data_processing.py

Place the data generated from the bloomberg Terminal into the directory "data/Bloomberg" and run data_processing.py the complete processed date tables will be in data/processed_fi_info