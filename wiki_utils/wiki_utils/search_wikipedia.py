import requests


def search_wikipedia(query: str,
                     api_url: str = "https://en.wikipedia.org/w/api.php",
                     srlimit: int = 100,
                     srsort: str = "relevance"
                     ):

    search_params = {
        'action': "query",
        'format': "json",
        'list': 'search',
        'srprop': '',
        'srlimit': srlimit,
        'srsort': srsort,
        'srsearch': query
    }

    S = requests.Session()
    response = S.get(api_url, params=search_params)

    return response.json()


def extract_articles(response):
    url_pattern = "http://en.wikipedia.org/?curid="
    search_items = response["query"]["search"]
    candidate_articles = [ (i["title"], url_pattern + str(i["pageid"])) for i in search_items]

    return candidate_articles





