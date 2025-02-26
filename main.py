import pandas as pd  
import string
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
from PIL import Image
import os
from io import BytesIO
import tempfile
from fpdf import FPDF
from get_play_by_play import get_play_by_play 
from get_roster import get_roster
from create_chart import create_chart

# 2.5 minutes

hits = {'singled', 'doubled', 'tripled', 'homered'}
outs = {'flied out', 'grounded out', 'lined out', 'fouled out'}
misc = {'error', 'fielder\'s choice'}
positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field', 'left side', 'left center', 'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'right center', 'p', 'pitcher', 'c', 'catcher'}
spray_chart_template = {pos: 0 for pos in positions}

team = 'eastern'

def main():
    roster_url = 'https://goeasterneagles.com/sports/baseball/roster'
    box_scores = []
    
    # baseball schedules
    urls = ['https://goeasterneagles.com/sports/baseball/schedule/2025', \
'https://goeasterneagles.com/sports/baseball/schedule/2024', 'https://goeasterneagles.com/sports/baseball/schedule/2023',\
'https://goeasterneagles.com/sports/baseball/schedule/2022', 'https://goeasterneagles.com/sports/baseball/schedule/2021']

    # get box score links from schedule pages
    for url in urls:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        box_scores += ['https://goeasterneagles.com/' + a['href'] for a in soup.find_all('a', href=True) if 'boxscore' in a['href'] and "target" not in a.attrs]

    ## writes roster to roster.csv, play by play to play-by-play.csv
    ## uncomment to use, leave commented if data already scraped
    get_roster(roster_url, team)
    # get_play_by_play(box_scores, team)

    ## reads in data from csv files
    roster = pd.read_csv(f'rosters/{team}.csv')
    roster = roster.sort_values(by="Last Name", ascending=True) 
    play_by_play = pd.read_csv('play-by-play.csv')
        
    if not os.path.exists(f'spray_charts/{team}'):
        os.mkdir(f'spray_charts/{team}')
    
    # for index, row in roster.iterrows():
    #     spray_chart = spray_chart_template.copy()
    #     first_name = row['First Name'].strip()
    #     last_name = row['Last Name'].strip()
    #     full_name = first_name + ' ' + last_name
    #     plays = play_by_play.loc[play_by_play['Name'] == full_name, 'Play']
    #     if not plays.empty:
    #         plays.to_csv('test.csv')
    #         for play in plays:
    #             pos = ball_hit_to(play)
    #             if pos:
    #                 # print(play, pos)
    #                 spray_chart[pos] += 1
                
    #     # write spray chart to csv
    #     df = pd.DataFrame.from_dict(spray_chart, orient='index', columns=['#'])
    #     df.index.name = "Positions"
    #     df = df.reset_index()
    #     df.to_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv', index=False)
    #     create_chart(team, first_name, last_name)   
    #     if sum(spray_chart.values()) > 50:
    #         print(first_name, last_name)

        
    image_folder = f'spray_chart_pics/{team}'
    PAGE_WIDTH, PAGE_HEIGHT = 2550, 3300
    MARGIN = 10
    # for index, row in roster.iterrows():
    # first_name = row['First Name'].strip()
    # last_name = row['Last Name'].strip()
    # full_name = first_name + ' ' + last_name
    # images = [Image.open(os.path.join(folder, f)) for f in os.listdir(folder) if f.endswith(".jpg")]
    # Resize all images to have a uniform height (preserve aspect ratio)
    # base_height = min(img.height for img in images)
    # images = [img.resize((int(img.width * (base_height / img.height)), base_height), Image.LANCZOS) for img in images]

    # Constants for letter size
    output_pdf = 'output.pdf'
    PAGE_WIDTH = 612  # 8.5 inches * 72 dpi
    PAGE_HEIGHT = 792  # 11 inches * 72 dpi
    MARGIN = 20
    MAX_WIDTH = PAGE_WIDTH - 2 * MARGIN
    MAX_HEIGHT = PAGE_HEIGHT - 2 * MARGIN
    ROW_SPACING = 10
    COL_SPACING = 10

    images = [Image.open(os.path.join(image_folder, img)) for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images = [img.convert("RGB") for img in images]
    pdf = FPDF(unit="pt", format="letter")
    pdf.add_page()
    x, y = MARGIN, MARGIN
    row_height = 0
    for img in images:
        img = img.resize((MAX_WIDTH // 2 - COL_SPACING, MAX_HEIGHT // 3)) 
        print(MAX_WIDTH, MAX_WIDTH //2, img.size, x)
        img_width, img_height = img.size
        if x + img_width > PAGE_WIDTH - MARGIN:
            x = MARGIN
            y += row_height
            row_height = 0
        if y + img_height > PAGE_HEIGHT - MARGIN:
            pdf.add_page()
            x, y = MARGIN, MARGIN
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            img.save(temp_file, format="JPEG")
            temp_file_path = temp_file.name
            pdf.image(temp_file_path, x, y, img_width, img_height)
        x += img_width + COL_SPACING
        row_height = max(row_height, img_height)
    pdf.output(output_pdf)
    print(f"PDF saved as {output_pdf}")




# Find where the ball is hit to by returning first position found in string
def ball_hit_to(play):
    # doubled, RBI (2-0 BB); T. Cate advanced to third; C. Ellis scored, unearned. c
    play = play.replace(",", "").split(';')[0]
    tokens = play.translate(str.maketrans("", "", string.punctuation)).split()
    if tokens[0] == 'to' or tokens[0] == 'advanced' or tokens[0] == 'walked' or tokens[0] == 'stole' or tokens[0] == 'pinch':
        return None
    if len(tokens) > 1:
        two_word = tokens[0] + tokens[1] 
        if two_word == 'struckout' or two_word == 'outat' or two_word == 'caughtstealing':
            return None
    if len(tokens) > 2 and tokens[0] + tokens[1] + tokens[2] == 'hitbypitch':
        return None
    
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
        
        for pos in positions:
            if pos == word or pos == two_word or pos == three_word:
                return pos

    

if __name__ == "__main__":  
    main()