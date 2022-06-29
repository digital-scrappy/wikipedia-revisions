from wiki_utils import wiki_utils as wiki
from bls_utils import bls_utils as bls
import time


def get_articles_for_occupation(occupation):
    time.sleep(1)
    response = wiki.search_wikipedia(query=occupation, srlimit=5)
    print(f"sucessfully fetched page for id {occupation}")
    return wiki.extract_articles(response)

path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
occupations = bls.get_occupations(path, group="Broad Group")




candidate_pages = [get_articles_for_occupation(occ) for occ in occupations]

print(candidate_pages)
