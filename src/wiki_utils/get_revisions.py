import requests
import json
import datetime
import time
from requests.exceptions import ConnectionError

query = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles='Baker'&rvslots=*&rvprop=id%timestamp&rvlimit=max&rvstart={start.timestamp()}&rvstop={stop.tim}"
