from pathlib import Path
from typing import List, Tuple
from test_data import doc_1, doc_2
from bertopic import BERTopic
from path_util import revisions_path, data_path
from split_page_into_paragraphs import split_page_into_paragraphs
import numpy as np
import os
import json
from datetime import datetime
import sqlite3
db_path = (data_path / "data_bases" / "all_occupations.db")
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute(
    "SELECT occ_code, occ_title, strict_links, rev_dirs FROM occupations WHERE occ_group = 'detailed'")

query_result = cur.fetchall()
occupations = {}


def get_latest_page(page_dir: Path) -> Path:

    rev_names = os.listdir(page_dir)


    for revision_name in rev_names:
        rev_path = page_dir / revision_name
        oldest_path = rev_path
        oldest = datetime(year=2000, month=1, day=1)
        
        oldest_path = rev_path
        with open(rev_path) as rev_file:
            try: 
                rev_date = datetime.fromisoformat(json.load(rev_file)["timestamp"])
            except json.JSONDecodeError:
                continue
            if rev_date > oldest:
                oldest = rev_date
                oldest_path = rev_path

    return oldest_path
                



all_paragraphs = []
all_pages = []
for occ_str in query_result:
    occ = (occ_str[0], occ_str[1], json.loads(occ_str[2]), json.loads(occ_str[3]))
    occ_code = occ[0]
    occupations[occ_code] = {"pages" :[], "paragraphs" : []}
    link_names = map(lambda x: x[0], occ[2])
    

    
    for dir_name in occ[3]:
        rev_dir_path = revisions_path / dir_name
        page_dirs = os.listdir(rev_dir_path)

        for page_dir in page_dirs:
            page_dir_path = rev_dir_path / page_dir

            if page_dir in link_names:
                latest_page = get_latest_page(page_dir_path)
                with open(latest_page, "r") as page_file:
                    page_dict = json.load(page_file)
                    
                    try:
                        page_text = page_dict["*"]
                    except:
                        break

                occupations[occ_code]["pages"].append(page_text)
                all_pages.append(page_text)
                paragraphs = split_page_into_paragraphs(page_text)
                [occupations[occ_code]["paragraphs"].append(p) for p in paragraphs]
                [all_paragraphs.append(p) for p in paragraphs]


topic_model = BERTopic(language="english",calculate_probabilities=True, verbose=True)
topic_model.fit(all_paragraphs)



