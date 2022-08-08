import mwclient
import json

credentials_loc = "/home/scrappy/Projects/csh/secrets/mw_oauth1.json"

with open(credentials_loc) as handle:
    credentials = json.load(handle)

user_agent="csh_wikipedia_edits_and_employment 1.0 (jakob.e.hauser@protonmail.com)"
site = mwclient.Site("en.wikipedia.org",
                     clients_useragent= user_agent,
                     consumer_token=credentials["Consumer token"],
                     consumer_secret=credentials["Consumer secret"],
                     access_token=credentials["Access token"],
                     access_secret=credentials["Access secret"],
                     max_lag=5)



raw_revisions = site.pages["Baker"].revisions(limit=1, prop = "ids|content|timestamp|flags|user|userid|size|tags", dir="newer")
