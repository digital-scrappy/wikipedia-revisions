import json
from path_util import base_path, data_path, secrets_path, revisions_path
import os
import mwclient
from datetime import datetime
from time import mktime
import time
import requests.exceptions
from fastprogress.fastprogress import progress_bar

def transfrom_revision(rev):
    rev["timestamp"] = datetime.fromtimestamp(mktime(rev["timestamp"])).isoformat()
    return rev


credentials_loc = "/home/scrappy/Projects/csh/secrets/mw_oauth1.json"
user_agent="csh_wikipedia_edits_and_employment 1.0 (jakob.e.hauser@protonmail.com)"

with open(credentials_loc) as handle:
    credentials = json.load(handle)

site = mwclient.Site("en.wikipedia.org",
                     clients_useragent= user_agent,
                     consumer_token=credentials["Consumer token"],
                     consumer_secret=credentials["Consumer secret"],
                     access_token=credentials["Access token"],
                     access_secret=credentials["Access secret"],
                     max_lag=5)


with open((data_path / "links.json"), "r") as handle:
    links = json.load(handle)

flag = True    
for key, value in progress_bar(links.items()):
    occ_path = revisions_path / key
    if not os.path.exists(occ_path):
        os.mkdir(occ_path)

    dir_list = os.listdir(occ_path)
    for page_name, link in value[0]:
        page_path = occ_path / page_name
        if page_name in dir_list:
            continue

        if not os.path.exists(page_path):
            os.mkdir(page_path)
        try:
            raw_revisions = site.pages[page_name].revisions(limit=500,
                                                            prop = "ids|content|timestamp|flags|user|userid|size|tags",
                                                            dir="newer")
        except requests.exceptions.ReadTimeout:
            time.sleep(60)
            raw_revisions = site.pages[page_name].revisions(limit=500,
                                                            prop = "ids|content|timestamp|flags|user|userid|size|tags",
                                                            dir="newer")
        
            
            
            
        revisions = (transfrom_revision(rev) for rev in raw_revisions)
        for rev in revisions:
            rev_file_path = page_path / (rev["timestamp"] + ".json")
            with open(rev_file_path, "w") as handle:
                json.dump(rev, handle)
            
