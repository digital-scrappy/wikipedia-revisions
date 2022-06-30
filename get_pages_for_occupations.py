import wiki_utils as wiki
import bls_utils as bls
import sql_utils as sql

import sys
sys.path.append(".")
import time
from tqdm import trange
import sqlite3

in_path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

def get_pages_for_occupations(in_path, db_path, group_level= "Detailed Occupation"):

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    occupations = bls.get_occupations(in_path, group=group_level)

    for i in trange(len(occupations)):
        time.sleep(0.5)
        occupation = occupations[i]
        response = wiki.search_wikipedia(query=occupation, srlimit=10)

        if response:
            content = wiki.extract_articles(response)
            sucess = 1

        else:
            content = None
            sucess = 0

        sql.write_occupation_to_db(occupation,
                                content,
                                sucess,
                                cur,
                                con,
                                table = "occupations")

    con.close()
