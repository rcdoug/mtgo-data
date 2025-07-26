from datetime import datetime

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

import dbops

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
    url = 'https://www.mtgo.com/decklist/pauper-challenge-32-2025-06-2912800016'
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    row_list = []

    # Event Details Processing
    print(parse_event_details(soup, url))

    # Decklist processing

    # soup.find_all returns bs4.element.ResultSet
    for decklist in soup.find_all("section", class_="decklist"):
        # decklist is of type bs4.element.Tag

        row_entry = {}
        playerStringPartition = decklist.find("p", class_="decklist-player").get_text().partition(" ")

        user = playerStringPartition[0]
        placeMatch = re.search("(?:\()([0-9]+)", playerStringPartition[2])

        row_entry["username"] = user
        row_entry["placement"] = placeMatch.group(1)

        cardDict = get_cardDict(decklist.find("div", class_="decklist-category-columns"), decklist.find("ul", class_="decklist-sideboard"))

        row_entry["cards"] = cardDict
        row_list.append(row_entry)
    
    df = pd.DataFrame(row_list)
    player_list = df['username'].tolist()
    player_map = dbops.get_player_ids(player_list)
    df['player_id'] = player_map[df['username']]
    print(df)

    return

def parse_event_details(soup, url: str):

    playerCount = int(soup.find("h2", class_="decklist-player-count").get_text().partition(" ")[0])
    datePosted = soup.find("p", class_="decklist-posted-on").get_text().partition(" ")[2].partition(" ")[2]
    date_obj = datetime.strptime(datePosted, "%B %d, %Y")
    date = date_obj.date().isoformat()
    mtgo_event_id = url[-8:]
    title = soup.title.get_text().partition("|")[0].partition(" ")
    formatName = title[0]
    eventType = title[2].rstrip()
    return (formatName, eventType, date, playerCount, mtgo_event_id)
    # (event_id, format_id, event_type_id, date, entries, mtgo_event_id)

def get_cardDict(mainList, sideList):
    cardDict = {}
    
    for entry in mainList.find_all("a"):
        cardName, cardNum = get_name_and_num(entry)
        cardDict[cardName] = (cardNum, 0)
    for entry in sideList.find_all("a"):
        cardName, cardNum = get_name_and_num(entry)
        if cardName in cardDict:
            (numMainBoard, numSideBoard) = cardDict[cardName]
            cardDict[cardName] = (numMainBoard, numSideBoard + cardNum)
        else:
            cardDict[cardName] = (0, cardNum)

    return cardDict

def get_name_and_num(entry):
    card = entry.get_text().partition(" ")
    cardNum = int(card[0])
    cardName = card[2]
    return (cardName, cardNum)

if __name__ == "__main__":
    parse_local()