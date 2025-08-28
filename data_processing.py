import sys

import csv
from utilities.company_data import FossilFuelCompanyYear

from global_values import FINANCIAL_INSTITUTIONS, YEARS_OF_INTEREST, FOSSIL_FUEL_TICKERS

import os
from typing import List
import matplotlib.pyplot as plt
from string import ascii_lowercase
from alive_progress import alive_bar




def main(fossil_csv_dir: str, years: List[int], output_dir: str, graph_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the fi dicts:
    fi_serialized_data = {}
    for fi in FINANCIAL_INSTITUTIONS:
        fi_serialized_data[fi] = [0] * len(years)

    for i in range(len(years)):
        
        year = years[i]
        print(f"Analyzing fossil fuel companies for year {year}")
        year_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_dir, exist_ok=True)

        with alive_bar(len(FOSSIL_FUEL_TICKERS)) as bar:
            for urgewald_ticker in FOSSIL_FUEL_TICKERS:
                bar()
                # Find relevant file:
                first_character = urgewald_ticker[0].lower()
                if first_character not in ascii_lowercase:
                    possible_files = [os.path.join(fossil_csv_dir, filename) for filename in os.listdir(fossil_csv_dir) if filename.startswith(f"GHG_emissions_others_") and filename.endswith(".csv")]
                else:
                    possible_files = [os.path.join(fossil_csv_dir, filename) for filename in os.listdir(fossil_csv_dir) if filename.startswith(f"GHG_emissions_{first_character}") and filename.endswith(".csv") and not filename.startswith(f"GHG_emissions_others_")]
                
                for file in possible_files:
                    try:
                        company = FossilFuelCompanyYear(file, year, urgewald_ticker)
                        for fi in FINANCIAL_INSTITUTIONS:
                            fi_serialized_data[fi][i] += company.get_total_financed_emission(fi)
                        output_path = os.path.join(year_dir, f"{company.ticker.replace("/", " - ")}_{year}.csv")
                        company.export_with_financed_data_to_csv(output_path)
                        
                        break
                    except StopIteration:
                        continue
                    except Exception as e:
                        print(f"[ERROR] Failed processing {file} for year {year}: {e}")
                
        
    for fi in FINANCIAL_INSTITUTIONS:
        plt.bar(years, fi_serialized_data[fi])
        plt.title(f"{fi} Emissions data")
        plt.xlabel("Year")
        plt.ylabel("Financed CO2 Emission")
        plt.savefig(f"{graph_dir}/{fi}_plot.png")
        plt.clf()
    with open(f"{graph_dir}/data.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Financial Institution"] + years)
        writer.writerows([[fi] +  fi_serialized_data[fi] for fi in FINANCIAL_INSTITUTIONS])
        
    


if __name__ == "__main__":
    if len(sys.argv) < 4:
        fossil_csv_dir = "data/Bloomberg"
        output_dir = "data/processed_info"
        graph_dir = "./data/serialized_fi_data"

    else:
        fossil_csv_dir = sys.argv[1]
        output_dir = sys.argv[2]
    years = [int(year) for year in YEARS_OF_INTEREST]


    main(fossil_csv_dir, years, output_dir, graph_dir)