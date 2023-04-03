# Implements the web_scrape() function to look up information and return the top articles based on the given query.

from typing import Optional

import requests
from bs4 import BeautifulSoup


def get_page_content(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        else:
            print(f"Error: Unable to fetch content from {url} (status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error: Unable to fetch content from {url} due to: {e}")
        return None

# Example usage
# url = "https://example.com/article1"
# print(get_page_content(url))
