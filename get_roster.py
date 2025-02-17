import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs

def get_roster(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # may need to change these lines to find the correct table in html
    firstnames = soup.find_all('span', class_='sidearm-roster-player-first-name')
    lastnames = soup.find_all('span', class_='sidearm-roster-player-last-name')

    data = []

    for i in range(len(firstnames)):
        data.append([firstnames[i].text, lastnames[i].text]) 
    
    df = pd.DataFrame(data, columns=["First Name", "Last Name"]) 
    df.to_csv("roster.csv", index=False)
