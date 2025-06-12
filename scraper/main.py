import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

def run_scraper():
    url = 'https://www.mtgo.com/decklists/2025/06'
    print(get_challenge_links(url))

def get_challenge_links(url):
    res = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if 'challenge' in href:
            res.append(href)
    return res


if __name__ == "__main__":
    run_scraper()