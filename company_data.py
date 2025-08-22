from typing import Optional, Dict, Any
import os
import csv
from utilities import safe_to_float
from functools import partial
from extract_13F_data import get_share_value_from_13F

HOLDINGS_DATA_COLLECTION = partial(get_share_value_from_13F, aggregation_method=sum)
FINANCIAL_INSTITUTIONS = [
    "BMO", 
    "Brookfield Asset Management", 
    "CIBC", 
    "Fairfax", 
    "Healthcare of Ontario Pension Plan Trust Fund",
    "Intact Financial",
    "Investment Management of Ontario",
    "Manulife",
    "National Bank of Canada",
    "OMERS",
    "OPSEU",
    "OTPP",
    "Power Corp of Canada",
    "RBC",
    "Scotiabank",
    "TD"
]
class FossilFuelCompanyYear:
    year : int
    ticker : str
    ghg_scope_1 : Optional[float] = None
    ghg_scope_2_location_based : Optional[float] = None
    ghg_scope_3 : Optional[float] = None
    scope_3_purch_goods_srvcs : Optional[float] = None
    scope_3_capital_goods : Optional[float] = None
    scope_3_fuel_enrg_relatd_act : Optional[float] = None
    scope_3_upstream_trans_dist : Optional[float] = None
    scope_3_waste_genrtd_in_op : Optional[float] = None
    scope_3_business_trvl_emissions : Optional[float] = None
    scope_3_employee_commuting : Optional[float] = None
    scope_3_upstream_leased_assets : Optional[float] = None
    scope_3_dwnstrm_trans_dist : Optional[float] = None
    scope_3_prcss_of_sold_prods : Optional[float] = None
    scope_3_use_sold_products : Optional[float] = None
    scope_3_eol_trtmnt_prods : Optional[float] = None
    scope_3_dwnstrm_lease_assts : Optional[float] = None
    scope_3_franchises : Optional[float] = None
    scope_3_investments : Optional[float] = None
    scope_3_emissions_other : Optional[float] = None
    enterprise_value : Optional[float] = None
    is_comp_sales : Optional[float] = None
    historical_market_cap : Optional[float] = None
    name : Optional[str] = None
    is_avg_num_sh_for_eps : Optional[float] = None
    px_last :  Optional[float] = None
    short_and_long_term_debt : Optional[float] = None
    cash_and_marketable_securities : Optional[float] = None
    bs_tot_asset : Optional[float] = None

    investment_data : Dict[str, float] = {}

    
    def _read_from_csv(self, path_to_csv: str, year: int):
        self.year = year
        with open(path_to_csv, mode='r', newline='') as source_file:
            reader = csv.reader(source_file)
            for line in reader:
                if str(year) in line[0]:
                    
                    self.ticker = line[0]
                    fields = [safe_to_float(val) for val in line]
                    self.ghg_scope_1 = fields[1] 
                    self.ghg_scope_2_location_based = fields[2] 
                    self.ghg_scope_3 = fields[3]
                    self.scope_3_purch_goods_srvcs = fields[4]
                    self.scope_3_capital_goods = fields[5]
                    self.scope_3_fuel_enrg_relatd_act = fields[6]
                    self.scope_3_upstream_trans_dist = fields[7]
                    self.scope_3_waste_genrtd_in_op = fields[8]
                    self.scope_3_business_trvl_emissions = fields[9]
                    self.scope_3_employee_commuting = fields[10]
                    self.scope_3_upstream_leased_assets = fields[11]
                    self.scope_3_dwnstrm_trans_dist = fields[12]
                    self.scope_3_prcss_of_sold_prods = fields[13]
                    self.scope_3_use_sold_products = fields[14]
                    self.scope_3_eol_trtmnt_prods = fields[15]
                    self.scope_3_dwnstrm_lease_assts = fields[16]
                    self.scope_3_franchises = fields[17]
                    self.scope_3_investments = fields[18]
                    self.scope_3_emissions_other = fields[19]
                    self.enterprise_value = fields[20]
                    self.is_comp_sales = fields[21]
                    self.historical_market_cap = fields[22]
                    self.name = line[23] if len(line) > 23 else ""
                    self.is_avg_num_sh_for_eps = safe_to_float(line[24]) if len(line) > 24 else None
                    self.px_last = safe_to_float(line[25]) if len(line) > 25 else None
                    self.short_and_long_term_debt = safe_to_float(line[26]) if len(line) > 26 else None
                    self.cash_and_marketable_securities = safe_to_float(line[27]) if len(line) > 27 else None
                    self.bs_tot_asset = safe_to_float(line[28]) if len(line) > 28 else None
                    return
            print(path_to_csv)
            
    def __init__(self, path_to_csv: str, year: int):
        self._read_from_csv(path_to_csv, year)
        for financial_institution in FINANCIAL_INSTITUTIONS:
            if self.ticker is not None:
                self.investment_data[financial_institution] = HOLDINGS_DATA_COLLECTION(self.ticker, financial_institution, year)


            
    def total_scope_3_emissions(self) -> float:
        scope_3_fields = [
            self.scope_3_purch_goods_srvcs,
            self.scope_3_capital_goods,
            self.scope_3_fuel_enrg_relatd_act,
            self.scope_3_upstream_trans_dist,
            self.scope_3_waste_genrtd_in_op,
            self.scope_3_business_trvl_emissions,
            self.scope_3_employee_commuting,
            self.scope_3_upstream_leased_assets,
            self.scope_3_dwnstrm_trans_dist,
            self.scope_3_prcss_of_sold_prods,
            self.scope_3_use_sold_products,
            self.scope_3_eol_trtmnt_prods,
            self.scope_3_dwnstrm_lease_assts,
            self.scope_3_franchises,
            self.scope_3_investments,
            self.scope_3_emissions_other,
        ]
        return sum(v for v in scope_3_fields if v is not None)

    def get_financed_scope_1_emission(self, fi: str) -> Optional[float]:
        share_value = self.investment_data[fi]
        if self.historical_market_cap is None or self.ghg_scope_1 is None :
            return None
        
        return (share_value / (self.historical_market_cap * (10 ** 6))) * self.ghg_scope_1 * 1000
        
    def get_financed_scope_2_emission(self, fi: str) -> Optional[float]:
        share_value = self.investment_data[fi]
        if self.historical_market_cap is None or self.ghg_scope_2_location_based is None :
            return None
        
        return (share_value / (self.historical_market_cap * (10 ** 6))) * self.ghg_scope_2_location_based * 1000

    def get_financed_scope_3_emission(self, fi: str) -> Optional[float]:
        share_value = self.investment_data[fi]
        if self.historical_market_cap is None :
            return None
        
        return (share_value / (self.historical_market_cap * (10 ** 6))) * self.total_scope_3_emissions() * 1000
        
    def get_total_financed_emission(self, fi: str) -> float:
        emissions = [
            self.get_financed_scope_1_emission(fi),
            self.get_financed_scope_2_emission(fi),
            self.get_financed_scope_3_emission(fi) 
            ]
        return sum(v for v in emissions if v is not None)
        

    def export_with_financed_data_to_csv(self, output_path: str):
        with open(output_path, mode='w', newline='') as f:
            writer = csv.writer(f)

            # Write raw data (header and values)
            raw_fields = [
                'year', 'ticker', 'ghg_scope_1', 'ghg_scope_2_location_based', 'ghg_scope_3',
                'scope_3_purch_goods_srvcs', 'scope_3_capital_goods', 'scope_3_fuel_enrg_relatd_act',
                'scope_3_upstream_trans_dist', 'scope_3_waste_genrtd_in_op', 'scope_3_business_trvl_emissions',
                'scope_3_employee_commuting', 'scope_3_upstream_leased_assets', 'scope_3_dwnstrm_trans_dist',
                'scope_3_prcss_of_sold_prods', 'scope_3_use_sold_products', 'scope_3_eol_trtmnt_prods',
                'scope_3_dwnstrm_lease_assts', 'scope_3_franchises', 'scope_3_investments',
                'scope_3_emissions_other', 'enterprise_value', 'is_comp_sales', 'historical_market_cap',
                'name', 'is_avg_num_sh_for_eps', 'px_last', 'short_and_long_term_debt',
                'cash_and_marketable_securities', 'bs_tot_asset'
            ]
            writer.writerow(raw_fields)
            writer.writerow([getattr(self, field) for field in raw_fields])

            # Spacer row
            writer.writerow([])

            # Write financed emissions per institution
            writer.writerow(['Financial Institution', 'Financed Scope 1', 'Financed Scope 2', 'Financed Scope 3', 'Total Financed Emissions'])
            for fi in self.investment_data:
                row = [
                    fi,
                    self.get_financed_scope_1_emission(fi),
                    self.get_financed_scope_2_emission(fi),
                    self.get_financed_scope_3_emission(fi),
                    self.get_total_financed_emission(fi)
                ]
                writer.writerow(row)

