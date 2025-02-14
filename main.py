import pandas as pd  
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re

def main():
    url = 'https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/6421'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    rgx = re.compile(r'[A-Z]{1}\.')

    for row in soup.find_all('td'):
        if rgx.match(row.text):
            print(row.text)
    # print(soup.prettify())

if __name__ == "__main__":  
    main()