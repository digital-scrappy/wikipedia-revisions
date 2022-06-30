import wiki_utils as wiki
import bls_utils as bls
import sql_utils as sql

import time
from tqdm import trange
import sqlite3

in_path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

def get_pages_for_occupations(in_path, db_path, group_level= "Detailed Occupation", srlimit = 10):
    '''A function to retrieve the candidate links the top n link returned by wikipedia search for each occupation
    Args:
        in_path (str) : the path to the xlsx file holding the bls soc structure
        db_path (str) : the path to the sqlite db storing the data
        group_level (str): The the level at which to extract occupations can be one of either ["Minor  Group", "Broad Group", "Detailed Occupation"]
        srlimit (int) : the number of top search results to use

    Returns:
        None'''
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    occupations = bls.get_occupations(in_path, group=group_level)

    for i in trange(len(occupations)):
        time.sleep(0.5)
        occupation = occupations[i]
        response = wiki.search_wikipedia(query=occupation, srlimit= srlimit)

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
