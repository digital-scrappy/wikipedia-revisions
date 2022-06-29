import requests
from bs4 import BeautifulSoup
from typing import Dict
from time import strptime, struct_time

def get_history_page(page_id: str) -> BeautifulSoup:
    '''Get the history page associated with the page_name.

    Args:
        page_name (str): the name of the page

    Returns:
        BeautifulSoup: the content of the page in a BeautifulSoup object
    '''

    response = requests.get(
        f"http://en.wikipedia.org/?curid={page_id}&offset=&limit=500&action=history")


    return BeautifulSoup(response.text)


def get_versions(page: BeautifulSoup) -> Dict[struct_time, str]:
    '''Get the revision dates and corresponding links from a history page.

    Args:
        page (BeautifulSoup): the name of the page

    Returns:
        Dict: the dates of the versions with the corresponding links
    '''
    date_format = "%H:%M, %d %B %Y"
    date_elem_class = "mw-changeslist-date"
    revision_dates = page.find_all("a", class_ = date_elem_class)
    versions_dictionary = {strptime(version.text, date_format) : version["href"] for version in revision_dates}

        
    return versions_dictionary
