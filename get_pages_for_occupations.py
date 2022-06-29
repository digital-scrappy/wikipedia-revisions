from wiki_utils import wiki_utils as wiki
from bls_utils import bls_utils as bls
import time
from tqdm import trange 
import json
import sqlite3

def get_articles_for_occupation(occupation: str, cursor: sqlite3.Cursor):
    response = wiki.search_wikipedia(query=occupation, srlimit=10)

    if response:
        content = wiki.extract_articles(response)
        value = (occupation, json.dumps(content), '', 1, 0)
        cursor.execute("INSERT INTO occupations Values (NULL, ?,?,?,?,?)", value)
    
    else:
        value = (occupation, '', '', 0, 0)
        cursor.execute("INSERT INTO occupations Values (NULL, ?,?,?,?,?)", value)

in_path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"


con = sqlite3.connect(db_path)
cur = con.cursor()


occupations = bls.get_occupations(in_path, group= "Detailed Occupation")
for i in trange(len(occupations)):
    time.sleep(0.5)
    occupation = occupations[i]
    get_articles_for_occupation(occupation, cur)
    con.commit()

con.close()
