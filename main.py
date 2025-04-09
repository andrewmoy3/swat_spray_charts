import pandas as pd  
import os
from funcs.get_play_by_play import get_play_by_play 
from funcs.get_roster import get_roster
from funcs.create_chart_image import create_chart_image
from funcs.create_chart_data import create_chart_data
from funcs.get_boxscore_links import get_boxscore_links
from funcs.stitch_to_pdf import stitch_to_pdf
import time

##########
# CHANGE THESE FOR EACH TEAM
team = 'gettysburg'
url_team_name = 'gettysburgsports'
roster_url = f'https://{url_team_name}.com/sports/baseball/roster'
schedule_url = f'https://{url_team_name}.com/sports/baseball/schedule/'
##########

hits = ['singled']
xbh = ['doubled', 'tripled', 'homered']
outs = ['flied', 'grounded', 'lined', 'fouled', 'popped', ]
misc = ['error', 'fielder\'s']
types = {'hits': hits, 'xbh': xbh, 'outs': outs, 'misc': misc}

def main():
    if not os.path.exists(f'spray_charts/{team}'):
        os.mkdir(f'spray_charts/{team}')

    ## get boxscore links from schedule pages
    ## about 1.5 - 2 seconds
    start = time.time()
    boxscores = get_boxscore_links(schedule_url, url_team_name, 2021, 2025)
    print(len(boxscores))
    end = time.time()
    print("Box Scores scraped: ", end - start)

    ## writes roster to roster.csv, play by play to play-by-play.csv
    ## uncomment to use, leave commented if data already scraped
    ## < 1 second
    get_roster(roster_url, team)

    ## writes play by play data to play-by-play.csv
    ## uncomment to use, leave commented if data already scraped
    ## 2 seconds per season
    start = time.time()
    # get_play_by_play(boxscores, team)
    end = time.time()
    print("Play by Plays scraped: ", end - start)

    ## reads in roster, play by play from csv files
    ## < 1 second
    roster = pd.read_csv(f'rosters/{team}.csv').sort_values(by="Number", ascending=True) 
    play_by_play = pd.read_csv('play-by-play.csv')
        
    ## create spray charts for each player
    ## iterate through all players
    ## < 1 second 
    start = time.time()
    for index, row in roster.iterrows():
        first_name = row['First Name'].strip()
        last_name = row['Last Name'].strip()
        number = row['Number']
        full_name = first_name + ' ' + last_name
        # get plays where name == current player
        plays = play_by_play.loc[play_by_play['Name'] == full_name, 'Play']

        ## create spray chart data from play by play data
        create_chart_data(plays, team, first_name, last_name, types)
        ## create spray chart image from csv data
        create_chart_image(team, first_name, last_name, number, types)   
        
    ## stitch all spray chart images into a pdf
    stitch_to_pdf(team)
    end = time.time()
    print("Spray Charts Created: ", end - start)

if __name__ == "__main__":  
    main()