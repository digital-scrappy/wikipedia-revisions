import requests
import datetime
import time
from requests.exceptions import ConnectionError


def get_revisions(page_id, start, end):

    api_url= "https://en.wikipedia.org/w/api.php"
    query_params = {
        'action': "query",
        'format': "json",
        'prop': 'revisions',
        'titles': page_id,
        'rvprop': "ids|timestamp",
        'rvlimit': "max",
        'rvstart' : start.timestamp(),
        'rvend' : end.timestamp(),
        'rvdir' : "newer",
        'rvcontinue' : None}
    S = requests.Session()
    revisions = []
    i=0
    not_found=True
    while i <30 and not_found:
        try:
            response = S.get(api_url, params = query_params)
            not_found=False
        except ConnectionError:
            print("Connection Error")
            time.sleep(1)
            i += 1
        else:


            data = response.json()

            try:
                revisions = list(data["query"]["pages"].values())[0]["revisions"]
            except KeyError:
                print(data)
                print("KeyError")

    return revisions

# query = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&pageids={page_id}&rvslots=*&rvprop=id%timestamp&rvlimit=max&rvstart={start.timestamp()}&rvstop={stop.tim}"


