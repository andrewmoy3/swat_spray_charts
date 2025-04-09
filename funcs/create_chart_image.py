import sys
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import numpy as np

# gets data from spray_charts/ folder and creates a spray chart image, saves to spray_chart_pics/ folder
def create_chart_image(team, first_name, last_name, number, types):
    # read in data from csv files
    # if not os.path.exists(f'spray_chart_pics/{team}'):
    #     os.mkdir(f'spray_chart_pics/{team}')
    
    if not os.path.exists(f'spray_charts/{team}/{first_name}_{last_name}.csv'):
        return

    df = pd.read_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv')

    def get_text_size(text, font, scale, thickness):
        return cv2.getTextSize(text, font, scale, thickness)[0]

    def draw_centered_text(image, text, x, y, font, scale, color, thickness):
        text_size = get_text_size(text, font, scale, thickness)
        text_x = x - text_size[0] // 2
        text_y = y + text_size[1] // 2  
        cv2.putText(image, text, (text_x, text_y), font, scale, color, thickness)

    img = cv2.imread("empty_chart.jpg")  
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    width = img.shape[1]

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    name_x, y_offset = width // 2, 25
    line_spacing = 10

    lines = [f"{first_name} {last_name}", str(int(number))]
    for line in lines:
        text_size = get_text_size(line, font, font_scale, thickness)
        draw_centered_text(img, line, name_x, y_offset, font, font_scale, (0, 0, 0), thickness)
        y_offset += text_size[1] + line_spacing 

    third_x, third_y = 105, 285
    ss_x, ss_y = 170, 220
    lf_x, lf_y = 65, 150 
    positions = {
        "1b": (width - third_x, third_y),
        "2b": (width - ss_x, ss_y),
        "3b": (third_x, third_y),
        "ss": (ss_x, ss_y),
        "lf": (lf_x, lf_y),
        "cf": ((width // 2)+1, 90),
        "rf": (width - lf_x, lf_y),
        "p": ((width // 2)+1, 300),
        "c": ((width // 2)+1, 420),
    }

    def get_color(ratio):
        blue = int(255 * (1 - ratio) / 2)  
        red = int(min(255 * ratio * 2, 255))  
        return (blue, 0, red)  

    total = df.iloc[:, 1:].sum().sum()
    for pos, (x, y) in positions.items():
        increment = 20
        row = df.loc[df['Category'] == pos]
        singles = row.iloc[:, 1].sum().sum()
        xbh = row.iloc[:, 2].sum().sum()
        outs = row.iloc[:, 3].sum().sum()
        misc = row.iloc[:, 4].sum().sum()
        pos_total = singles + xbh + outs + misc
        pos_color = get_color(pos_total / total) if total > 0 else (255, 0, 0)
        singles_color = get_color(singles / pos_total) if pos_total > 0 else (255, 0, 0)
        xbh_color = get_color(xbh / pos_total) if pos_total > 0 else (255, 0, 0)
        outs_color = get_color(outs / pos_total) if pos_total > 0 else (255, 0, 0)
        misc_color = get_color(misc / pos_total) if pos_total > 0 else (255, 0, 0)

        draw_centered_text(img, str(pos_total), x, y, font, font_scale, pos_color, thickness)
        if pos in ['lf', 'cf', 'rf']:
            draw_centered_text(img, str(singles), x, y+increment, font, font_scale/2, singles_color, thickness)
            draw_centered_text(img, str(xbh), x, y+2*increment, font, font_scale/2, xbh_color, thickness)
        else: 
            draw_centered_text(img, str(singles), x, y+increment, font, font_scale/2, singles_color, thickness)
            draw_centered_text(img, str(outs), x, y+2*increment, font, font_scale/2, outs_color, thickness)
            draw_centered_text(img, str(misc), x, y+3*increment, font, font_scale/2, misc_color, thickness)

    os.makedirs(f'spray_chart_pics/{team}', exist_ok=True)
    cv2.imwrite(f'spray_chart_pics/{team}/{first_name}_{last_name}.jpg', img)

