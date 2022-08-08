import wiki_utils as wiki
import bls_utils as bls
import sql_utils as sql

import time
from tqdm import trange
import sqlite3


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
    print(occupations)

    for i in trange(len(occupations)):
        time.sleep(0.5)
        occupation = occupations[i]
        responses = wiki.dynamic_search_wikipedia(query=occupation, srlimit= srlimit)
        # response = wiki.search_wikipedia(query=occupation, srlimit= srlimit)

        content = []
        for response in responses:
            if response:
                try:
                    content += wiki.extract_articles(response)
                    sucess = 1
                except KeyError:
                    print("some key error in wiki.extract_articles")

            else:
                continue

        if len(content) == 0:
            sucess = 0

        sql.write_occupation_to_db(occupation,
                                content,
                                sucess,
                                cur,
                                con,
                                table = "occupations")




    con.close()
