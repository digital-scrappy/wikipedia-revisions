from get_pages_for_occupations import get_pages_for_occupations
from sql_utils import init_db
in_path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
db_path = "/home/scrappy/data/csh/bls/processed/soc_2018_Detailed.db"

init_db(db_path)
get_pages_for_occupations(in_path, db_path, group_level="Detailed Occupation", srlimit = 10)
