from path_util import data_path
import os
from  zipfile import ZipFile
import pandas as pd

bls_source_path = data_path / "bls" / "source"

#There are many different names for the bls files in the zip archives here is a proper mapping 
bls_reports = {"oesm21nat" : ["oesm21nat/national_M2021_dl.xlsx", "o_group"],
               "oesm03nat" : ["national_may2003_dl.xls", "group"],
               "oesm04nat" : ["national_may2004_dl.xls", "group"],
               "oesm05nat" : ["national_may2005_dl.xls", "group"], 
               "oesm07nat" : ["national_May2007_dl.xls", "group"],
               "oesm08nat" : ["national__M2008_dl.xls", "group"],
               "oesm09nat" : ["national_dl.xls", "group"], 
               "oesm10nat" : ["national_M2010_dl.xls", "group"],
               "oesm11nat" : ["national_M2011_dl.xls", "group"],
               "oesm12nat" : ["oesm12nat/national_M2012_dl.xls", "occ_group"],
               "oesm13nat" : ["oesm13nat/national_M2013_dl.xls", "occ_group"],
               "oesm14nat" : ["oesm14nat/national_M2014_dl.xlsx", "occ_group"],
               "oesm15nat" : ["oesm15nat/national_M2015_dl.xlsx", "occ_group"],
               "oesm16nat" : ["oesm16nat/national_M2016_dl.xlsx", "occ_group"],
               "oesm17nat" : ["oesm17nat/national_M2017_dl.xlsx", "occ_group"],
               "oesm18nat" : ["oesm18nat/national_M2018_dl.xlsx", "occ_group"],
               "oesm19nat" : ["oesm19nat/national_M2019_dl.xlsx", "o_group"],
               "oesm20nat" : ["oesm20nat/national_M2020_dl.xlsx", "o_group"]}



# using the original Zipfiles to guarantee correct data 
# opening all the zipfiles and appending the corresponding dataframes to bls_reports
for zip_name in os.listdir(bls_source_path):
    zip_path = bls_source_path / zip_name
    with ZipFile(zip_path) as zip_file:
        #removing the .zip at the end
        bls_name = zip_name[:-4]
        xls_path = bls_reports[bls_name][0]

        with zip_file.open(xls_path, "r") as xls_file:
            df = pd.read_excel(xls_file)
            bug = hi
            df.convert.column_to_correct_data_formats()
            df.columns = df.columns.str.lower()
            bls_reports[bls_name].append(df)

empty_occ_columns = {"tot_emp": [], "h_mean": [], "a_mean": [], "h_pct10": [], "h_pct25": [],
                     "h_median": [], "h_pct75": [], "h_pct90": [], "a_pct10": [], "a_pct25": [], "a_median": [], "a_pct75": [], "a_pct90": []}
occ_stat_keys = empty_occ_columns.keys()

occupations =  {}

for row in bls_reports["oesm21nat"][-1].itertuples():
    row = row._asdict()
    occupations[row["occ_code"]] = {"tot_emp": [], "h_mean": [], "a_mean": [], "h_pct10": [], "h_pct25": [],
                     "h_median": [], "h_pct75": [], "h_pct90": [], "a_pct10": [], "a_pct25": [], "a_median": [], "a_pct75": [], "a_pct90": []}

    occupations[row["occ_code"]]["group"] = row["o_group"]

occ_21_keys =  list(occupations.keys())
for name, value in bls_reports.items():
    for row in value[-1].itertuples():
        row = row._asdict()

        #skipping occupations that are not in the 2021 occ classification
        if row["occ_code"] not in occ_21_keys:
            continue

        #appending the stats 
        for key in occ_stat_keys:
            occupations[row["occ_code"]][key].append(row[key])

print(occupations["11-0000"])

        
        
            








