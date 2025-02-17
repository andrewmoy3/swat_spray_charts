import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_play_by_play(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # may need to change this line to find the correct table in html
    playbyplay = soup.find_all('div', id='inning-all')

    rgx = re.compile(r'[A-Z]{1}\.')

    data = []

    for table in playbyplay:
        for row in table.find_all('td'):
            if rgx.match(row.text):
                data.append([row.text])

    df = pd.DataFrame(data, columns=["Play by Play"])
    df.to_csv("play-by-play.csv", index=False)
