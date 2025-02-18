import pandas as pd  
import string
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
from get_play_by_play import get_play_by_play 
from get_roster import get_roster

hits = {'singled', 'doubled', 'tripled', 'homered'}
outs = {'flied out', 'grounded out', 'lined out', 'fouled out'}
misc = {'error', 'fielder\'s choice'}
positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field',  'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'p', 'pitcher', 'c', 'catcher'}
spray_chart_template = {pos: 0 for pos in positions}

def main():
    roster = 'https://berryvikings.com/sports/baseball/roster/'
    box_score = 'https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/6421'
    # for i in range(6421, 6424):
        # scrape('https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/' + str(i))

    ## writes roster to roster.csv, play by play to play-by-play.csv
    ## uncomment to use, leave commented if data already scraped
    # get_roster(roster)
    # get_play_by_play(box_score)

    ## reads in data from csv files
    roster = pd.read_csv('roster.csv')
    play_by_play = pd.read_csv('play-by-play.csv')
    
    for index, row in roster.iterrows():
        spray_chart = spray_chart_template.copy()
        first_name = row['First Name']
        last_name = row['Last Name']
        # full_name = first_name + " " + last_name
        full_name = first_name[0] + ". " + last_name    
        plays = play_by_play.loc[play_by_play['Name'] == full_name, 'Play']
        if not plays.empty:
            # for pos in positions:
            for play in plays:
                pos = ball_hit_to(play)
                if pos:
                    spray_chart[pos] += 1
            print(f"Plays for {full_name}: \n{plays}")

        # write spray chart to csv
        df = pd.DataFrame.from_dict(spray_chart, orient='index', columns=['#'])
        df.index.name = "Positions"
        df = df.reset_index()
        df.to_csv(f'spray_charts/{last_name}.csv', index=False)


# Find where the ball is hit to by returning first position found in string
def ball_hit_to(play):
    tokens = play.translate(str.maketrans("", "", string.punctuation)).split()
    # play = play.replace(",", "").split(';')[0]
    # tokens = play.split()
    for i in range(2, len(tokens)):
        word = tokens[i]
        two_word = tokens[i-1] + ' ' + tokens[i]
        three_word = tokens[i-2] + ' ' + tokens[i-1] + ' ' + tokens[i]
        for pos in positions:
            if pos == word.lower() or pos == two_word.lower() or pos == three_word.lower():
                return pos


def tokenize(play):
    tokens = play.split()
    return tokens

if __name__ == "__main__":  
    main()