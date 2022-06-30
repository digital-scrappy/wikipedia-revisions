import requests
import time


def search_wikipedia(query: str,
                     api_url: str = "https://en.wikipedia.org/w/api.php",
                     srlimit: int = 100,
                     srsort: str = "relevance",
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
    retry_flag = 0
    while retry_flag < 5:
        try:
            response = S.get(api_url, params=search_params)
        except:
            retry_flag += 1
            time.sleep(1)
            print(f"query for {query} failed ")
        else:
            return response.json()
    return None


def extract_articles(response):

    url_pattern = "http://en.wikipedia.org/?curid="
    search_items = response["query"]["search"]
    candidate_articles = [(i["title"], url_pattern + str(i["pageid"]))
                          for i in search_items]

    return candidate_articles
