import pandas as pd  
import string
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
import os
from get_play_by_play import get_play_by_play 
from get_roster import get_roster

hits = {'singled', 'doubled', 'tripled', 'homered'}
outs = {'flied out', 'grounded out', 'lined out', 'fouled out'}
misc = {'error', 'fielder\'s choice'}
positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field', 'left side', 'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'p', 'pitcher', 'c', 'catcher'}
spray_chart_template = {pos: 0 for pos in positions}

team = 'berry'

def main():
    roster_url = 'https://berryvikings.com/sports/baseball/roster/'
    box_scores = []
    
    # baseball schedules
    # urls = ['https://berryvikings.com/sports/baseball/schedule/2025']
    urls = ['https://berryvikings.com/sports/baseball/schedule/2025', 'https://berryvikings.com/sports/baseball/schedule/2024', 'https://berryvikings.com/sports/baseball/schedule/2023', 'https://berryvikings.com/sports/baseball/schedule/2022']

    # get box score links from schedule pages
    for url in urls:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        box_scores += ['https://berryvikings.com/' + a['href'] for a in soup.find_all('a', href=True) if 'boxscore' in a['href'] and "target" not in a.attrs]

    ## writes roster to roster.csv, play by play to play-by-play.csv
    ## uncomment to use, leave commented if data already scraped
    # get_roster(roster_url, team)
    # get_play_by_play(box_scores)

    ## reads in data from csv files
    roster = pd.read_csv(f'rosters/{team}.csv')
    play_by_play = pd.read_csv('play-by-play.csv')
        
    if not os.path.exists(f'spray_charts/{team}'):
        os.mkdir(f'spray_charts/{team}')
    
    for index, row in roster.iterrows():
        spray_chart = spray_chart_template.copy()
        first_name = row['First Name']
        last_name = row['Last Name']
        # full_name = first_name + " " + last_name
        full_name = first_name[0] + ". " + last_name    
        plays = play_by_play.loc[play_by_play['Name'] == full_name, 'Play']
        if not plays.empty:
            for play in plays:
                print(play)
                pos = ball_hit_to(play)
                if pos:
                    spray_chart[pos] += 1
            # print(f"Plays for {full_name}: \n{plays}")

        # write spray chart to csv
        df = pd.DataFrame.from_dict(spray_chart, orient='index', columns=['#'])
        df.index.name = "Positions"
        df = df.reset_index()
        df.to_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv', index=False)


# Find where the ball is hit to by returning first position found in string
def ball_hit_to(play):
    tokens = play.translate(str.maketrans("", "", string.punctuation)).split()
    # play = play.replace(",", "").split(';')[0]
    # tokens = play.split()
    for i in range(len(tokens)):
        word = tokens[i].lower()
        if i > 0:
            two_word = (tokens[i-1] + ' ' + tokens[i]).lower()
        else:
            two_word = None  
        if i > 1:
            three_word = (tokens[i-2] + ' ' + tokens[i-1] + ' ' + tokens[i]).lower()
        else:
            three_word = None  
        
        if word == 'stole' or word == 'advanced' or word == 'walked' or two_word == 'struck out' or three_word == 'hit by pitch':
            return None
        for pos in positions:
            if pos == word or pos == two_word or pos == three_word:
                return pos

    

if __name__ == "__main__":  
    main()