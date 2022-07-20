import sqlite3
import time
from typing import List
from numpy import int64
import pandas as pd
from collections import OrderedDict
from pathlib import Path 
import json
from tqdm import trange

old_db_path = "/home/scrappy/data/csh/bls/processed/oesm21nat.db"
new_db_path = "/home/scrappy/data/csh/aggregated_edits.db"

bls_base_path= Path("/home/scrappy/data/csh/bls/source/")
bls_reports = [("oesm13nat", "national_M2013_dl.xls"),
               ("oesm14nat", "national_M2014_dl.xlsx"),
               ("oesm15nat", "national_M2015_dl.xlsx"),
               ("oesm16nat", "national_M2016_dl.xlsx"),
               ("oesm17nat", "national_M2017_dl.xlsx"),
               ("oesm18nat", "national_M2018_dl.xlsx"),
               ("oesm19nat", "national_M2019_dl.xlsx"),
               ("oesm20nat", "national_M2020_dl.xlsx"),
               ("oesm21nat", "national_M2021_dl.xlsx")]

years = [2013+i for i in range(9)]

old_con = sqlite3.connect(old_db_path)
old_cur = old_con.cursor()
new_con = sqlite3.connect(new_db_path)
new_cur = new_con.cursor()

# empty_occ_columns = {"OCC_CODE": [], "OCC_TITLE": [], "TOT_EMP": [], "H_MEAN": [], "A_MEAN": [], "H_PCT10": [], "H_PCT25": [],
#                    "H_MEDIAN": [], "H_PCT75": [], "H_PCT90": [], "A_PCT10": [], "A_PCT25": [], "A_MEDIAN": [], "A_PCT75": [], "A_PCT90": []}
empty_occ_columns = { "TOT_EMP": [], "H_MEAN": [], "A_MEAN": [], "H_PCT10": [], "H_PCT25": [],
                   "H_MEDIAN": [], "H_PCT75": [], "H_PCT90": [], "A_PCT10": [], "A_PCT25": [], "A_MEDIAN": [], "A_PCT75": [], "A_PCT90": []}
my_columns = ["lenient_links", "strict_links"]


bls_dfs = OrderedDict()
for i in bls_reports:
    if i[0] == "oesm19nat":
        group_name = "o_group"
    elif i[0] in ["oesm20nat", "oesm21nat"]:
        group_name = "O_GROUP"
    else:
        group_name = "OCC_GROUP"
    df = pd.read_excel( (bls_base_path / i[0] / i[1]) )
    df.drop(df.index[df[group_name] != "detailed"], inplace=True)
    df.columns = map(str.upper, df.columns)
    bls_dfs[i[0]] = df

old_cur.execute(
    f"SELECT occ_code, occ_title, lenient_links, strict_links FROM occupations WHERE length(strict_links) > 3")
data = old_cur.fetchall()

columns = ["id integer primary key"] + ["occ_code", "occ_title"] + my_columns +  list(empty_occ_columns.keys())
new_cur.execute(f"CREATE TABLE occupations({' ,'.join(columns)})")

# for occ in data:
for idx in trange(len(data)):
    occ = data[idx]
    occ_code, occ_title, lenient_links_json, strict_links_json = occ
    
    occ_columns = { "TOT_EMP": [], "H_MEAN": [], "A_MEAN": [], "H_PCT10": [], "H_PCT25": [], "H_MEDIAN": [], "H_PCT75": [], "H_PCT90": [], "A_PCT10": [], "A_PCT25": [], "A_MEDIAN": [], "A_PCT75": [], "A_PCT90": []}

    lenient_links = json.loads(lenient_links_json)
    strict_links = json.loads(strict_links_json)

    for bls_df in bls_dfs.values():
        row = bls_df[bls_df["OCC_CODE"] == occ_code]
        if row.empty:
            continue
        for key in occ_columns.keys():
            value = row[key].values[0]
            if type(value) == int64:
                occ_columns[key].append(int(value))
            else:
                occ_columns[key].append(value)

    occ_values = [occ_code,
                  occ_title,
                  lenient_links_json,
                  strict_links_json]

    for stat in occ_columns.values():
        occ_values.append(json.dumps(stat))
    new_cur.execute(f"INSERT INTO occupations Values (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(occ_values))
    new_con.commit()

        
    
    

    
    
