
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sqlite3
import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

from path_util import data_path
from count_contributions import contributions_by_user, amount_detailed, avg_unique_auth_page_lengths
from sum_stats import sum_up_attributes

def create_dataframe():
    bls_gender_race_excel_path = data_path / "bls" / "gender_race_hispanic" / "cpsaat11_gender, races, hispanic.xlsx"

    gender_race_df = pd.read_excel(bls_gender_race_excel_path, skiprows = 6)

    # overall labor market participation
    women = gender_race_df["Unnamed: 2"][0]/100
    white = gender_race_df["Unnamed: 3"][0]/100
    african_american = round(gender_race_df["Unnamed: 4"][0]/100, 3)
    asian = gender_race_df["Unnamed: 5"][0]/100
    hispanic = gender_race_df["Unnamed: 6"][0]/100

    mapping_dict = {"women": women, "white": white, "non_hispanic_white": white - hispanic,
                    "african_american": african_american, "asian": asian, "hispanic": hispanic}

    db_path = data_path / "data_bases" / "all_occupations.db"
    con = sqlite3.connect(db_path)

    df_all = pd.read_sql('SELECT occ_code, occ_group, occ_title, lenient_links, lenient_revs, lenient_lengths, women, white, african_american, asian, hispanic  FROM occupations', con)
    df = df_all # make a copy

    df = df.loc[df['women'] != "null"] # delete nulls

    # fix parsing as float and rounding
    for col in ["women", "white", "african_american", "asian", "hispanic"]:
        df[col] = df[col].astype(float)
        df[col] = df[col].apply(lambda x: round(x, 3))

    # add a column for non-hispanic white people
    if "non_hispanic_white" not in df:
        df.insert(8, "non_hispanic_white", df["white"].subtract(df["hispanic"]))

    print("The number of entries in df:", len(df))

    # adding the _summed corresponding values
    for i in ["women", "white", "non_hispanic_white", "african_american", "asian", "hispanic"]:
        new_col_name = i + "_summed"
        sum_up_attributes(i, new_col_name, df)

    df.dropna(inplace = True) # drop NaNs
    df_major = df.loc[df['occ_group'] == "major"]

    articles_per_detailed = amount_detailed(df_all, df_major)
    unique_auths, page_lengths = avg_unique_auth_page_lengths(df_major)

    if "art_per_detailed" not in df_major:
        df_major.insert(4, "art_per_detailed", articles_per_detailed)

    if "avg_unique_auths" not in df_major:
        df_major.insert(6, "avg_unique_auths", unique_auths)

    if "avg_page_lengths" not in df_major:
        df_major.insert(8, "avg_page_lengths", page_lengths)

    return df_major
                      
