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

    numbers = []
    names = []
    for i in range(len(table)):
        names += (table[i].find_all('a'))
        numbers += (table[i].find_all('td'))
    
    data = []

    rgx = re.compile(r'[A-Za-z]+[ ]+[A-Za-z]+')
    for i in range(len(names)):
        if rgx.match(names[i].text):
            data.append(names[i].text.split(maxsplit=1))
        # else:
        #     print(data)
        # data.append([firstnames[i].text, lastnames[i].text]) 
    
    player = 0
    num = re.compile(r'^\d{1,2}$')
    for i in range(len(numbers)):
        n = numbers[i].text
        if num.match(n):
            data[player].append(n)
            player += 1
            

    df = pd.DataFrame(data, columns=["First Name", "Last Name", "Number"]) 
    df.to_csv(f"rosters/{team}.csv", index=False)
