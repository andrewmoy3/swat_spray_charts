import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_play_by_play(urls):
    data = []
    for url in urls:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        # may need to change this line to find the correct table in html
        playbyplay = soup.find_all('div', id='inning-all')

        rgx = re.compile(r'[A-Z]{1}\.')

        for table in playbyplay:
            for row in table.find_all('td'):
                if rgx.match(row.text):
                    txt = row.text.strip().split()
                    name = " ".join(txt[:2])
                    play = " ".join(txt[2:])
                    data.append([name, play])

    df = pd.DataFrame(data, columns=["Name", "Play"])
    df.to_csv("play-by-play.csv", index=False)
