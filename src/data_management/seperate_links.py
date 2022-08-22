import sqlite3
import json
from path_util import  data_path

db_path = data_path / "aggregated_edits.db"

con = sqlite3.connect(db_path)
cur = con.cursor()
out_json_path = data_path / "links.json"

cur.execute("Select occ_code, lenient_links, strict_links from occupations")
links = cur.fetchall()

out_json = {}
for occ_code, lenient_links, strict_links in links:
    out_json[occ_code] = [json.loads(lenient_links), json.loads(strict_links)]

with open(out_json_path, "w") as handle:
    json.dump(out_json, handle)
    
