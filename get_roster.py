import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs

def get_roster(url,team):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # may need to change these lines to find the correct table in html
    # firstnames = soup.find_all('span', class_='sidearm-roster-player-first-name')
    # lastnames = soup.find_all('span', class_='sidearm-roster-player-last-name')
    table = soup.find_all('table', class_='sidearm-table')
    names = []
    for i in range(len(table)):
        names += (table[i].find_all('a'))
    rgx = re.compile(r'[A-Za-z]+[ ]+[A-Za-z]+')
    
    data = []

    for i in range(len(names)):
        if rgx.match(names[i].text):
            data.append(names[i].text.split(maxsplit=1))
        # data.append([firstnames[i].text, lastnames[i].text]) 

    df = pd.DataFrame(data, columns=["First Name", "Last Name"]) 
    df.to_csv(f"rosters/{team}.csv", index=False)
