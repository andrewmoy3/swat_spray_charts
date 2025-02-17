import pandas as pd  
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
import csv

def main():
    url = 'https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/6421'
    get_play_by_play(url)
    # for i in range(6421, 6424):
        # scrape('https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/' + str(i))

# filters out each line of play by play from given url
def get_play_by_play(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # may need to change this line to find the correct table in html
    playbyplay = soup.find_all('div', id='inning-all')

    rgx = re.compile(r'[A-Z]{1}\.')

    writer = csv.writer(file)
    with open('output.csv', 'w', newline='') as file:
        for table in playbyplay:
            for row in table.find_all('td'):
                if rgx.match(row.text):
                    writer.writerows([[row.text]])

if __name__ == "__main__":  
    main()