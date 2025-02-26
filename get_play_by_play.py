import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

def get_play_by_play(urls, team):
    roster = pd.read_csv(f'rosters/{team}.csv')

    # get full name from a play string
    def getFullName(name):
        for index, row in roster.iterrows():
            first_name = row['First Name'].strip()
            last_name = row['Last Name'].strip()
            full_name = f"{first_name} {last_name}"
            # Match "F. Last"
            if re.fullmatch(r"[A-Z]\. [A-Z][a-z]*[A-Za-z'-]*", name):
                if name.lower() == f"{first_name[0].lower()}. {last_name.lower()}":
                    return full_name, 1
            # Match "First Last"
            elif re.fullmatch(r"[A-Z][a-z]*[A-Za-z'-]* [A-Z][a-z]*[A-Za-z'-]*", name):
                if name.lower() == full_name.lower():
                    return full_name, 1
            # Match "Last, First"
            elif re.fullmatch(r"[A-Z][A-Za-z'-]*, [A-Z][A-Za-z'-]*", name):
                if name.lower() == f"{last_name.lower()}, {first_name.lower()}":
                    return full_name, 1
            # Match "Last,F"
            elif re.fullmatch(r"[A-Z][A-Za-z'-]*,[A-Z]", name):
                if name.lower() == f"{last_name.lower()},{first_name[0].lower()}":
                    return full_name, 1
            # Match "Last"
            else:
                name_lst = name.split()
                if name_lst and name_lst[0].lower() == last_name.lower():
                    return full_name, 0

            # need to do AJ Last, hypens

        # if re.fullmatch(r"[A-Z]\. [A-Z][a-z]*[A-Za-z'-]*", name)\
        #     or re.fullmatch(r"[A-Z][a-z]*[A-Za-z'-]* [A-Z][a-z]*[A-Za-z'-]*", name)\
        #     or re.fullmatch(r"[A-Z][a-z]*[A-Za-z'-]*, [A-Z][a-z]*[A-Za-z'-]*", name)\
        #     or re.fullmatch(r"[A-Z][A-Za-z'-]*,[A-Z]", name):
        #         return "", 0
        # else:
        #     print(name)

        return "", 0

    data = []
    for url in tqdm(urls):
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        # may need to change this line to find the correct table in html
        playbyplay = soup.find_all('div', id='inning-all')

        num = re.compile(r'^\d+$')

        for table in playbyplay:
            for row in table.find_all('td'):
                if not num.match(row.text):
                    txt = row.text.strip().split()
                    # assume first two words are name for now
                    if len(txt) < 2:
                        continue
                    name = txt[0].strip() + " " + txt[1].strip()
                    full_name, add = getFullName(name)
                    play = " ".join(txt[1+add:])
                    if full_name:
                        data.append([full_name, play])

    df = pd.DataFrame(data, columns=["Name", "Play"])
    df.to_csv("play-by-play.csv", index=False)


