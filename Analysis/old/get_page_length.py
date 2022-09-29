import mwclient
import json
import sqlite3
from tqdm import trange
from pathlib import Path
from Occupation import Occupation
from socket import gethostname

hostname = gethostname()
print(hostname)
if hostname == "yocto":
    base_path = Path("/home/scrappy/Projects/csh")
# insert your hostname here and the path to the repository   
elif hostname == "Maria":
    #just an example below
    base_path = Path("/home/Maria/Projects/csh")
else:
    base_path = Path("/home/scrappy/Projects/csh")
    print("no correct hostname found")
    

credentials_file = "mw_oauth1.json"
db_file = "aggregated_edits.db"


con = sqlite3.connect(base_path / "data" / db_file)
cur = con.cursor()

with open(base_path / "secrets" / credentials_file ) as handle:
    credentials = json.load(handle)


user_agent="csh_wikipedia_edits_and_employment 1.0 (jakob.e.hauser@protonmail.com)"

site = mwclient.Site("en.wikipedia.org",
                     clients_useragent= user_agent,
                     consumer_token=credentials["Consumer token"],
                     consumer_secret=credentials["Consumer secret"],
                     access_token=credentials["Access token"],
                     access_secret=credentials["Access secret"],
                     max_lag=5)

cur.execute("SELECT * FROM occupations")
occupations =  cur.fetchall()

page_lenghts= []
for idx in trange(len(occupations)):
    occ = Occupation(*occupations[idx])
    
    strict_lenght = 0
    for page in occ.strict_links:
        name, link = page
        strict_lenght += len(site.pages[name].text())
    lenient_lenght = 0
    for page in occ.lenient_links:
        name, link = page
        lenient_lenght += len(site.pages[name].text())
    page_lenghts.append([occ.id, strict_lenght, lenient_lenght])

with open("test.json" , "w") as handle:
    json.dump(page_lenghts, handle)

    
    

    
    




