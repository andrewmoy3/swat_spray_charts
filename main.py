import pandas as pd  
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
import get_play_by_play 
import get_roster

def main():
    roster = 'https://berryvikings.com/sports/baseball/roster/'
    box_score = 'https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/6421'
    get_roster(roster)
    get_play_by_play(box_score)
    

    # for i in range(6421, 6424):
        # scrape('https://berryvikings.com/sports/baseball/stats/2025/emory-university/boxscore/' + str(i))

# filters out each line of play by play from given url
            

if __name__ == "__main__":  
    main()