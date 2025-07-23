import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

def run_scraper():
    url = 'https://www.mtgo.com/decklist/pauper-challenge-32-2025-06-2912800016'
    path = 'scraper/response.txt'
    # resp = get_challenge_links(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_pretty_string = soup.prettify()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(soup_pretty_string)

def save_soup(url, path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(response.text)

# temp func to read from local response
def parse_local():
    path = 'scraper/response.txt'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    row_list = []

    # Decklist processing
    for decklist in soup.find_all("section", class_="decklist"):
        row_entry = {}
        for player in decklist.select("p.decklist-player"):
            s = player.get_text().partition(" ")
            user = s[0]
            placeMatch = re.search("(?:\()([0-9]+)", s[2])
            print(user + " | " + placeMatch.group(1))
            row_entry["username"] = user
            row_entry["placement"] = placeMatch.group(1)
        list = decklist.find("div", class_="decklist-category-columns")
        cardTuples = []
        for entry in list.find_all("a"):
            card = entry.get_text().partition(" ")
            myTuple = (card[0], card[2])
            cardTuples.append(myTuple)
        row_entry["cards"] = cardTuples
        row_list.append(row_entry)
    
    df = pd.DataFrame(row_list)
    print(df.loc[:, ["username", "placement"]])

    return

def parse_event(soup):

    return

def parse_decklist():

    return


if __name__ == "__main__":
    parse_local()