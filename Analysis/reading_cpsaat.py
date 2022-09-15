import pandas as pd
from path_util import data_path
from zipfile import ZipFile

## CPSAAT07 excel
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


## EDUCATION excel
def read_education_data():
    soc_education_excel = data_path / "bls" / "gender_race_hispanic" / "education.xlsx"
    df = pd.read_excel(soc_education_excel, sheet_name = "Table 5.3", skiprows = 1)
    df.drop(df.tail(4).index, inplace=True)
    df = df.drop(['2021 National Employment Matrix title'], axis=1)
    df = df.iloc[1:, :]
    df = df.astype(float, errors = "ignore")
    return df


def get_major_median(df):
    total_lst = []
    for code_digits in range(11, 54, 2):
        code_hyphon = str(code_digits) + "-"
        sub_df = df.loc[df['2021 National Employment Matrix code'].str.contains(code_hyphon, case=False)]
        columns = (sub_df.columns.tolist())[1:]
        median_lst = []

        median_lst.append((code_hyphon + "0000"))
        for col in columns:
            median_lst.append(sub_df[col].median())
        total_lst.append(median_lst)

    return total_lst



def get_detailed_education(df_education, df_detailed):
	
	df_education = df_education.rename({'2021 National Employment Matrix code':'occ_code'}, axis='columns')
	
	merged_df = df_detailed.merge(df_education, on='occ_code', how='left')
	
	return merged_df


## M2021 SOC excel
bls_source_path_2021 = data_path / "bls" / "source" / "oesm21nat.zip"

def read_m2021():
    with ZipFile(bls_source_path_2021) as zip_file:
        with zip_file.open("oesm21nat/national_M2021_dl.xlsx", "r") as xls_file:
            df = pd.read_excel(xls_file)
            return df

def get_major_median_annual(df):
    df_majors = df.loc[df['O_GROUP'] == "major"]
    df_majors_trimmed = df_majors[['OCC_CODE', 'A_MEAN', 'A_MEDIAN']]
    return df_majors_trimmed

def get_detailed_median_annual(df):
    df_detaileds = df.loc[df['O_GROUP'] == "detailed"]
    df_detaileds_trimmed = df_detaileds[['OCC_CODE', 'A_MEAN', 'A_MEDIAN']]
    return df_detaileds_trimmed