from path_util import data_path, revisions_path
import os
from zipfile import ZipFile
import pandas as pd
from datetime import datetime
import json
from json import JSONDecodeError
import sqlite3
from Occupation import Occupation
from tqdm import tqdm


def open_revision(path):
    with open(path) as rev_file:
        try:
            revision = json.load(rev_file)
        except JSONDecodeError:
            sub_set_revison = None
        else:
            try:
                sub_set_revison = {"revid" : revision["revid"],
                                   "user" : revision["user"],
                                   "userid" : revision["userid"],
                                   "timestamp" : revision["timestamp"],
                                   "tags" : revision["tags"],
                                   "lenght": len(revision["*"])}

            except KeyError:
                sub_set_revison = None
        return sub_set_revison
                

    
bls_source_path = data_path / "bls" / "source"
bls_gender_race_excel = data_path / "bls" / "gender_race_hispanic" / "cpsaat11_gender, races, hispanic.xlsx"

db_path = data_path / "data_bases" / "all_occupations.db"

if os.path.exists(db_path):
    os.remove(db_path)

#There are many different names for the bls files in the zip archives here is a proper mapping 
bls_reports = {"oesm03nat" : ["national_may2003_dl.xls", "group"],
               "oesm04nat" : ["national_may2004_dl.xls", "group"],
               "oesm05nat" : ["national_may2005_dl.xls", "group"], # add 2006 here
               "oesm06nat" : ["national_may2006_dl.xls", "group"],
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
               "oesm20nat" : ["oesm20nat/national_M2020_dl.xlsx", "o_group"],
               "oesm21nat" : ["oesm21nat/national_M2021_dl.xlsx", "o_group"]}

numeric_col_names = ["tot_emp", "h_mean", "a_mean", "h_pct10", "h_pct25", "h_median", "h_pct75",
                     "h_pct90", "a_pct10", "a_pct25", "a_median", "a_pct75", "a_pct90"]

empty_occ_columns = {"tot_emp": [], "h_mean": [], "a_mean": [], "h_pct10": [], "h_pct25": [], "h_median": [], "h_pct75": [],
                     "h_pct90": [], "a_pct10": [], "a_pct25": [], "a_median": [], "a_pct75": [], "a_pct90": []}

occ_stat_keys = empty_occ_columns.keys()

links_path = data_path / "links.json"

revision_dirs = os.listdir(revisions_path)

con = sqlite3.connect(db_path)
cur = con.cursor()




###########
#Loading Data
###########
with open(links_path) as links_file:
    links_dict = json.load(links_file)

# using the original zip archives to guarantee correct data 
# opening all the zip archives and appending the corresponding dataframes to bls_reports
print("extracting data from BLS zip archives")
for zip_name in tqdm(os.listdir(bls_source_path)):
    zip_path = bls_source_path / zip_name

    with ZipFile(zip_path) as zip_file:
        
        #removing the .zip at the end of the file name to get the name of the data 
        bls_name = zip_name[:-4]
        xls_path = bls_reports[bls_name][0]

        with zip_file.open(xls_path, "r") as xls_file:
            df = pd.read_excel(xls_file)
            
            df.columns = df.columns.str.lower()

            # converting all numeric columns to numbers and if not possible to nan 
            df[numeric_col_names] = df[numeric_col_names].apply(lambda x: pd.to_numeric(x, errors="coerce"))

            bls_reports[bls_name].append(df)

# gender race information - parsing the excel
gender_race_df = pd.read_excel(bls_gender_race_excel, skiprows = 5)
gender_race_df = gender_race_df.iloc[3: , :] # delete first 3 rows
gender_race_df = gender_race_df.iloc[:-2 , :] # delete last 2 rows

gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[0]: 'occ_name'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[1]: 'total_emp'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[2]: 'women'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[3]: 'white'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[4]: 'african_american'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[5]: 'asian'})
gender_race_df = gender_race_df.rename(columns={gender_race_df.columns[6]: 'hispanic'})

# declare missings, make occ_name lowercase to allow matching with SOC data
gender_race_df = gender_race_df.replace('–', None)
gender_race_df['occ_name'] = gender_race_df['occ_name'].str.lower()

gender_race_df["women"] = (gender_race_df["women"].astype(float) / 100)
gender_race_df["white"] = (gender_race_df["white"].astype(float) / 100)
gender_race_df["african_american"] = (gender_race_df["african_american"].astype(float) / 100)
gender_race_df["asian"] = (gender_race_df["asian"].astype(float) / 100)
gender_race_df["hispanic"] = (gender_race_df["hispanic"].astype(float) / 100)

# renaming several occ_names from the excel to fit the official SOC titles
gender_race_df['occ_name'] = gender_race_df['occ_name'].replace({
    'education, training, and library occupations': 'educational instruction and library occupations',
    'purchasing agents, except wholesale, retail, and farm products': 'buyers and purchasing agents',
    'other financial specialists': 'financial specialists, all other',
    'database administrators and architects': 'database administrators',
    'other mathematical science occupations': 'mathematical science occupations, all other',
    'other drafters': 'drafters, all other',
    'other engineering technologists and technicians, except drafters': 'engineering technologists and technicians, except drafters, all other',
    'other psychologists': 'psychologists, all other',
    'other life, physical, and social science technicians': 'life, physical, and social science technicians, all other',
    'mental health counselors': 'substance abuse, behavioral disorder, and mental health counselors',
    'other community and social service specialists': 'community and social service specialists, all other',
    'other educational instruction and library workers': 'educational instruction and library workers, all other',
    'other designers': 'designers, all other',
    'other physicians': 'physicians, all other',
    'dietetic technicians and ophthalmic medical technicians': 'ophthalmic medical technicians',
    'home health aides': 'home health and personal care aides',
    'orderlies and psychiatric aides': 'orderlies',
    'other healthcare support workers': 'healthcare support workers, all other',
    'janitors and building cleaners': 'janitors and cleaners, except maids and housekeeping cleaners',
    'other entertainment attendants and related workers': 'entertainment attendants and related workers, all other',
    'other extraction workers': 'extraction workers, all other',
    'industrial and refractory machinery mechanics': 'industrial machinery mechanics',
    'other installation, maintenance, and repair workers': 'installation, maintenance, and repair workers, all other',
    'other assemblers and fabricators': 'miscellaneous assemblers and fabricators',
    'other metal workers and plastic workers': 'metal workers and plastic workers, all other',
    'other production workers': 'production workers, all other',
    'other material moving workers': 'material moving workers, all other'})



#ram unfriendly runtime friendly code below
print("retrieving all revisions")
revs_by_pages = {}
for dir_number in tqdm(os.listdir(revisions_path)):
    pages_path = (revisions_path / dir_number)
    
    for page_name in os.listdir(pages_path):
        revs_by_pages[page_name] = []
        page_path = (pages_path / page_name)
        for revision in os.listdir(page_path):
            rev_path = (page_path / revision)
            rev_content = open_revision(rev_path)

            if rev_content:
                revs_by_pages[page_name].append(rev_content)


occupations = {}

# initialization of every occupation in the occupations dictionary
print("building the dictionary")
for row in bls_reports["oesm21nat"][-1].itertuples():
    row = row._asdict()
    detail_level  = row["o_group"]
    if detail_level == "total":
        continue
    occ_code = row["occ_code"]
    occupations[occ_code] = {"tot_emp": {}, "h_mean": {}, "a_mean": {}, "h_pct10": {}, "h_pct25": {},
                     "h_median": {}, "h_pct75": {}, "h_pct90": {}, "a_pct10": {}, "a_pct25": {}, "a_median": {}, "a_pct75": {}, "a_pct90": {}}

    occupations[occ_code]["occ_group"] = detail_level
    occupations[occ_code]["occ_title"] = row["occ_title"]
    occupations[occ_code]["occ_code"] = occ_code

    if detail_level == "major":
        code_slice = occ_code[:2]
    elif detail_level == "minor":
        code_slice = occ_code[:5]
    elif detail_level == "broad":
        code_slice = occ_code[:6]
    elif detail_level == "detailed":
        code_slice = occ_code
    else:
        continue

    #getting all the keys of the links_dict that correspond to the occupation code
    relevant_link_keys = filter(lambda x: x.startswith(code_slice), links_dict.keys())
    relevant_links_nested_2 = [links_dict[occ_code] for occ_code in relevant_link_keys]

    #sorry ...  just flattening lists and converting the inner lists to tuples 
    lenient_nested =  [ page for page_lists in relevant_links_nested_2 for page in page_lists[0]]
    strict_nested =  [ page for page_lists in relevant_links_nested_2 for page in page_lists[1]]

    # sorry ... I don't know of a better way 
    lenient_tuple_list = list(set([tuple(page) for page in lenient_nested]))
    strict_tuple_list = list(set([tuple(page) for page in strict_nested]))

    # converting every [page_name, link] sublist to tuples and then converting the outer list to a set
    relevant_revision_dirs = list(filter(lambda x: x.startswith(code_slice), revision_dirs))
    
    occupations[occ_code]["strict_links"] = strict_tuple_list
    occupations[occ_code]["lenient_links"] = lenient_tuple_list
    occupations[occ_code]["rev_dirs"] = relevant_revision_dirs
    occupations[occ_code]["strict_revs"] = {}
    occupations[occ_code]["lenient_revs"] = {}
    occupations[occ_code]["strict_lengths"] = {}
    occupations[occ_code]["lenient_lengths"] = {}

    #slowing down this script by 2 minutes :)
    page_names =  list(set(map(lambda x: x[0], strict_tuple_list + lenient_tuple_list)))
    strict_names = map(lambda x: x[0], strict_tuple_list)
    lenient_names = map(lambda x: x[0], lenient_tuple_list)

    for page_name in strict_names:

        page_revs = revs_by_pages[page_name]
        datetimes = [(datetime.fromisoformat(page_rev["timestamp"]), page_rev["lenght"]) for page_rev in page_revs]
        lenght = max(datetimes, key = lambda x: x[0])[1]

        occupations[occ_code]["strict_revs"][page_name] = page_revs
        occupations[occ_code]["strict_lengths"][page_name] = lenght

    for page_name in lenient_names:
        
        page_revs = revs_by_pages[page_name]
        datetimes = [(datetime.fromisoformat(page_rev["timestamp"]), page_rev["lenght"]) for page_rev in page_revs]
        lenght = max(datetimes, key = lambda x: x[0])[1]
        
        occupations[occ_code]["lenient_revs"][page_name] = page_revs
        occupations[occ_code]["lenient_lengths"][page_name] = lenght
                    
    
    
    

    



    

# adding all the older reports to the occupations dictionary
occ_21_keys = list(occupations.keys())
print("adding older bls stats")
for name, value in tqdm(bls_reports.items()):
    timestamp = datetime(int("20" + name[4:6]), 5, 1).isoformat()

    for row in value[-1].itertuples():
        row = row._asdict()

        #skipping occupations that are not in the 2021 occ classification
        if row["occ_code"] not in occ_21_keys:
            continue

        #appending the stats 
        for key in occ_stat_keys:
            occupations[row["occ_code"]][key][timestamp] = row[key]

print("adding gender information")
for occ_code, contents in tqdm(occupations.items()):
    if contents["occ_title"].lower() in gender_race_df["occ_name"].tolist():
        occupations[occ_code]["women"] = round(gender_race_df[gender_race_df['occ_name'] == contents["occ_title"].lower()]['women'].item(), 3)
        occupations[occ_code]["white"] = round(gender_race_df[gender_race_df['occ_name'] == contents["occ_title"].lower()]['white'].item(), 3)
        occupations[occ_code]["african_american"] = round(gender_race_df[gender_race_df['occ_name'] == contents["occ_title"].lower()]['african_american'].item(), 3)
        occupations[occ_code]["asian"] = round(gender_race_df[gender_race_df['occ_name'] == contents["occ_title"].lower()]['asian'].item(), 3)
        occupations[occ_code]["hispanic"] = round(gender_race_df[gender_race_df['occ_name'] == contents["occ_title"].lower()]['hispanic'].item(), 3)
    else:
        occupations[occ_code]["women"] = None
        occupations[occ_code]["white"] = None
        occupations[occ_code]["african_american"] = None
        occupations[occ_code]["asian"] = None
        occupations[occ_code]["hispanic"] = None

# adding to the database
table_creation = '''CREATE TABLE occupations(
idx integer primary key,
occ_code text,
occ_group text,
occ_title text,
strict_links text,
lenient_links text,
strict_revs text,
lenient_revs text,
strict_lengths text,
lenient_lengths text,
rev_dirs text,
tot_emp text,
women text,
white text,
african_american text,
asian text,
hispanic text,
h_mean text,
a_mean text,
h_pct10 text,
h_pct25 text,
h_median text,
h_pct75 text,
h_pct90 text,
a_pct10 text,
a_pct25 text,
a_median text,
a_pct75 text,
a_pct90 text,
missing_bls_values bool)
'''
cur.execute(table_creation)


error_count = 0
print("writing to database")
for occupation_dict in tqdm(occupations.values()):
    occupation = Occupation(expected_lenght = 23, **occupation_dict)
        
    cur.execute(f"INSERT INTO occupations VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", occupation.to_db())
    con.commit()

print(error_count)
    

    
