import requests
import datetime

#following function taken from https://stackoverflow.com/questions/5417727/get-date-object-for-the-first-last-day-of-the-current-year
def year_range(year, datetime_o = datetime.datetime):
    return (
        datetime_o.min.replace(year = year),
        datetime_o.max.replace(year = year)        
    )



def get_revisions(page_id, year):

    api_url= "https://en.wikipedia.org/w/api.php"

    start, end=year_range(year)

    query_params = {
        'action': "query",
        'format': "json",
        'prop': 'revisions',
        'pageids': page_id,
        'rvprop': "ids|timestamp",
        'rvlimit': "max",
        'rvstart' : start.timestamp(),
        'rvend' : end.timestamp(),
        'rvdir' : "newer",
        'rvcontinue' : None}
    S = requests.Session()
    response = S.get(api_url, params = query_params)
    data = response.json()
    revisions = list(data["query"]["pages"].values())[0]["revisions"]
    return revisions

# query = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&pageids={page_id}&rvslots=*&rvprop=id%timestamp&rvlimit=max&rvstart={start.timestamp()}&rvstop={stop.tim}"


