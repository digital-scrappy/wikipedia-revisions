import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import sqlite3
import json
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr
import statsmodels.api as sm
from statsmodels.formula.api import ols

from path_util import data_path
from count_contributions import contributions_by_user, amount_detailed, avg_unique_auth_page_lengths
from sum_stats import sum_up_attributes
from reading_cpsaat import read_education_data, get_major_median, read_m2021, get_major_median_annual, get_detailed_education, get_detailed_median_annual



def dataframe_all():
	bls_gender_race_excel_path = data_path / "bls" / "gender_race_hispanic" / "cpsaat11_gender, races, hispanic.xlsx"
	gender_race_df = pd.read_excel(bls_gender_race_excel_path, skiprows = 6)
	db_path = data_path / "data_bases" / "all_occupations.db"
	con = sqlite3.connect(db_path)

	df_all = pd.read_sql('SELECT occ_code, occ_group, occ_title, lenient_links, lenient_revs, lenient_lengths, women, white, african_american,     asian, hispanic  FROM occupations', con)

	return df_all

def dataframe_standard():
	df_all = dataframe_all()
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
                      
def create_df_major():
	df_all = dataframe_all()
	df = df_all # make a copy

	df = df.loc[df['women'] != "null"] # delete nulls

	# fix parsing as float and rounding
	for col in ["women", "white", "african_american", "asian", "hispanic"]:
		df[col] = df[col].astype(float)
		df[col] = df[col].apply(lambda x: round(x, 3))

	# add a column for non-hispanic white people
	if "non_hispanic_white" not in df:
		df.insert(8, "non_hispanic_white", df["white"].subtract(df["hispanic"]))

	# Naive assumption that 1-women == men
	if "men" not in df:
		df.insert(6, "men", (df["women"] - 1).abs())

	# adding the _summed corresponding values
	for i in ["men", "women", "white", "non_hispanic_white", "african_american", "asian", "hispanic"]:
		new_col_name = i + "_summed"
		sum_up_attributes(i, new_col_name, df)
		df[new_col_name] = df[new_col_name].astype(float)
	df_major = df.loc[df['occ_group'] == "major"] # only majors -> redundant as above code block removes non-major anyways

	articles_per_detailed = amount_detailed(df_all, df_major)
	unique_auths, page_lengths, number_articles = avg_unique_auth_page_lengths(df_major)

	if "art_per_detailed" not in df_major:
		df_major.insert(4, "art_per_detailed", articles_per_detailed)

	if "avg_unique_auths" not in df_major:
		df_major.insert(6, "avg_unique_auths", unique_auths)

	if "avg_art_lengths" not in df_major:
		df_major.insert(8, "avg_art_lengths", page_lengths)

	if "amount_art" not in df_major:
		df_major.insert(4, "amount_art", number_articles)

	# Adding Mean and Median Income
	if "A_MEAN" not in df_major:
		m_df = get_major_median_annual(read_m2021())
		df_major = df_major.set_index('occ_code').join(m_df.set_index('OCC_CODE'))
		df_major.reset_index(inplace=True) # make sure occ_code is a column and not the index

	education_lsts = get_major_median(read_education_data())

	# making a df from the list of lists --> able to see each category individually
	df_education = pd.DataFrame(education_lsts, columns=['o_code', 'no_high_school', 'high_school', 'some_college',
										  'associate_degree', 'bachelors', 'masters', 'phd_professional'])
	if "education_slope" not in df_major:
		slopes = []
		nums = [i for i in range(1, 8)]
		for lst in education_lsts:
			lst.pop(0)
			slope, intercept, r_value, p_value, std_err = stats.linregress(nums, lst)
			slopes.append(slope)
		df_major['education_slope'] = slopes

	df_major["A_MEAN"] = pd.to_numeric(df_major["A_MEAN"])
	df_major["A_MEDIAN"] = pd.to_numeric(df_major["A_MEDIAN"])
	df_major["education_slope"] = pd.to_numeric(df_major["education_slope"])
	return df_major


def create_df_detailed():
	df_all = dataframe_all()
	df = df_all # make a copy

	df = df.loc[df['women'] != "null"] # delete nulls

	# fix parsing as float and rounding
	for col in ["women", "white", "african_american", "asian", "hispanic"]:
		df[col] = df[col].astype(float)
		df[col] = df[col].apply(lambda x: round(x, 3))

	# add a column for non-hispanic white people
	if "non_hispanic_white" not in df:
		df.insert(8, "non_hispanic_white", df["white"].subtract(df["hispanic"]))

	# Naive assumption that 1-women == men
	if "men" not in df:
		df.insert(6, "men", (df["women"] - 1).abs())

	df_detailed = df # make copy
	df_detailed = df_detailed.loc[df['occ_group'] == "detailed"] # has 453 rows (out of 831; so approx 55% of all detailed occs)

	df_detailed = df_detailed.dropna() # after removing NaNs has 285 rows (so approx. 34.3% of all detailed)

	articles_per_detailed = amount_detailed(df_all, df_detailed)
	unique_auths, page_lengths, number_articles = avg_unique_auth_page_lengths(df_detailed)

	if "art_per_detailed" not in df_detailed:
		df_detailed.insert(4, "art_per_detailed", articles_per_detailed)

	if "avg_unique_auths" not in df_detailed:
		df_detailed.insert(6, "avg_unique_auths", unique_auths)

	if "avg_art_lengths" not in df_detailed:
		df_detailed.insert(8, "avg_art_lengths", page_lengths)

	if "amount_art" not in df_detailed:
		df_detailed.insert(4, "amount_art", number_articles)

	df_detailed = df_detailed.loc[df_detailed['lenient_links'] != "[]"] # after this, only about 100 observations

	df_merged = get_detailed_education(read_education_data(), df_detailed)


	df_education = df_merged[['Less than high school diploma', 'High school diploma or equivalent', "Some college, no degree", 
								"Associate's degree", "Bachelor's degree", "Master's degree", "Doctoral or professional degree"]]

	if "education_slope" not in df_detailed:
		slopes = []
		nums = [i for i in range(1, 8)]
		for lst in df_education.values.tolist():
			slope, intercept, r_value, p_value, std_err = stats.linregress(nums, lst)
			slopes.append(slope)
		df_detailed['education_slope'] = slopes


	if "A_MEAN" not in df_detailed:
		m_df = get_detailed_median_annual(read_m2021())
		df_detailed = df_detailed.set_index('occ_code').join(m_df.set_index('OCC_CODE'))
		df_detailed.reset_index(inplace=True) # make sure occ_code is a column and not the index

	df_detailed = df_detailed.loc[df_detailed['A_MEAN'] != "*"] # can also interpolate (one observations)

	df_detailed["A_MEAN"] = pd.to_numeric(df_detailed["A_MEAN"])
	df_detailed["A_MEDIAN"] = pd.to_numeric(df_detailed["A_MEDIAN"])
	df_detailed["education_slope"] = pd.to_numeric(df_detailed["education_slope"])
	return df_detailed