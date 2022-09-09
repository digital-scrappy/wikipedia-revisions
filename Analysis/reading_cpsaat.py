import pandas as pd
from path_util import data_path

def read_cpsaat07():
    bls_gender_race_excel = data_path / "bls" / "gender_race_hispanic" / "cpsaat07.xlsx"
    df = pd.read_excel(bls_gender_race_excel, skiprows = 7)
    df = df.loc[df['TOTAL'] == "Employed"]
    df = df[['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 8']]
    df = df.iloc[1: , :]
    df.rename(columns = {'Unnamed: 1':'no high school', 'Unnamed: 2':'high school', 'Unnamed: 4':'some college',
                         'Unnamed: 5':'associate degree', 'Unnamed: 7':'bachelors degree', 'Unnamed: 8':'advanced degree'},
              inplace = True)
    df.loc[27] = df.loc[27] - df.loc[51] # account only for non hispanic whites
    return df

def read_education_data():
    soc_education_excel = data_path / "bls" / "gender_race_hispanic" / "education.xlsx"
    df = pd.read_excel(soc_education_excel, sheet_name = "Table 5.3", skiprows = 1)
    df.drop(df.tail(4).index, inplace=True)
    df = df.drop(['2021 National Employment Matrix title'], axis=1)
    df = df.iloc[1:, :]
    df = df.astype(float, errors = "ignore")
    return df

def get_major_median(df):
    education_median_dict = {}

    for code_digits in range(11, 54, 2):
        code_hyphon = str(code_digits) + "-"
        sub_df = df.loc[df['2021 National Employment Matrix code'].str.contains(code_hyphon, case=False)]

        columns = (sub_df.columns.tolist())[1:]
        median_lst = []
        for col in columns:
            median_lst.append(sub_df[col].median())
        education_median_dict[code_hyphon + "0000"] = median_lst  # create a list for each dict

    return education_median_dict

# get_major_median(read_education_data()) # code for extracting the education data as a dict