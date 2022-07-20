import mwclient
import json
import sqlite3
from datetime import datetime
from time import mktime
from tqdm import trange

def transfrom_revision(rev):
    rev["timestamp"] = datetime.fromtimestamp(mktime(rev["timestamp"])).isoformat()
    return rev

db_path = "/home/scrappy/data/csh/aggregated_edits.db"
credentials_loc = "/home/scrappy/Projects/csh/secrets/mw_oauth1.json"

con = sqlite3.connect(db_path)
cur = con.cursor()

with open(credentials_loc) as handle:
    credentials = json.load(handle)


data_location = "/home/scrappy/Data/csh/wikipedia/test/"
user_agent="csh_wikipedia_edits_and_employment 1.0 (jakob.e.hauser@protonmail.com)"

site = mwclient.Site("en.wikipedia.org",
                     clients_useragent= user_agent,
                     consumer_token=credentials["Consumer token"],
                     consumer_secret=credentials["Consumer secret"],
                     access_token=credentials["Access token"],
                     access_secret=credentials["Access secret"],
                     max_lag=5)
cur.execute("ALTER TABLE occupations ADD strict_revisions MEDIUMTEXT")
cur.execute("ALTER TABLE occupations ADD lenient_revisions MEDIUMTEXT")

cur.execute("SELECT id, lenient_links, strict_links FROM occupations")
occupations =  cur.fetchall()

for idx in trange(len(occupations)):
    occ = occupations[idx]
    tbl_id, lenient_links_json, strict_links_json = occ
    
    lenient_links = json.loads(lenient_links_json)
    strict_links = json.loads(strict_links_json)

    strict_revision_hist = {}

    for page in strict_links:
        name, link = page
        raw_revisions = site.pages[name].revisions(limit=500, prop = "ids|timestamp|flags|user|userid|size|tags", dir="newer")
        revisions = [transfrom_revision(rev) for rev in raw_revisions]
        strict_revision_hist[name] = revisions
    cur.execute("UPDATE occupations SET strict_revisions = ? WHERE id = ?",
                (json.dumps(strict_revision_hist), tbl_id))
        
    lenient_revision_hist = strict_revision_hist.copy()
    for page in lenient_links:
        name, link = page
        if name in lenient_revision_hist.keys():
            continue
        raw_revisions = site.pages[name].revisions(limit=500, prop = "ids|timestamp|flags|user|userid|size|tags", dir="newer")
        revisions = [transfrom_revision(rev) for rev in raw_revisions]
        lenient_revision_hist[name] = revisions
    
    cur.execute("UPDATE occupations SET lenient_revisions = ? WHERE id = ?",
                (json.dumps(lenient_revision_hist), tbl_id))

    con.commit()




