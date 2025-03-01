import sys
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os


# positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field', 'left side', 'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'p', 'pitcher', 'c', 'catcher'}

# gets data from spray_charts/ folder and creates a spray chart image, saves to spray_chart_pics/ folder
def create_chart_image(team, first_name, last_name, number):
    # read in data from csv files
    if not os.path.exists(f'spray_chart_pics/{team}'):
        os.mkdir(f'spray_chart_pics/{team}')

    df = pd.read_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv')
    first = df.loc[df['Positions'] == '1b', '#'].values[0] + df.loc[df['Positions'] == 'first base', '#'].values[0]
    second = df.loc[df['Positions'] == '2b', '#'].values[0] + df.loc[df['Positions'] == 'second base', '#'].values[0]
    third = df.loc[df['Positions'] == '3b', '#'].values[0] + df.loc[df['Positions'] == 'third base', '#'].values[0]
    ss = df.loc[df['Positions'] == 'ss', '#'].values[0] + df.loc[df['Positions'] == 'shortstop', '#'].values[0]
    lf = df.loc[df['Positions'] == 'lf', '#'].values[0] + df.loc[df['Positions'] == 'left field', '#'].values[0] + df.loc[df['Positions'] == 'left side', '#'].values[0] + df.loc[df['Positions'] == 'left center', '#'].values[0]
    cf = df.loc[df['Positions'] == 'cf', '#'].values[0] + df.loc[df['Positions'] == 'center field', '#'].values[0] + df.loc[df['Positions'] == 'up the middle', '#'].values[0]
    rf = df.loc[df['Positions'] == 'rf', '#'].values[0] + df.loc[df['Positions'] == 'right field', '#'].values[0] + df.loc[df['Positions'] == 'right side', '#'].values[0] + df.loc[df['Positions'] == 'right center', '#'].values[0]
    pitcher = df.loc[df['Positions'] == 'p', '#'].values[0] + df.loc[df['Positions'] == 'pitcher', '#'].values[0]
    catcher = df.loc[df['Positions'] == 'c', '#'].values[0] + df.loc[df['Positions'] == 'catcher', '#'].values[0]

    # print(first_name, last_name)
    # print("1B: ", first)
    # print("2B: ", second)
    # print("3B: ", third)
    # print("SS: ", ss)
    # print("LF: ", lf)
    # print("CF: ", cf)
    # print("RF: ", rf)
    # print("P: ", pitcher)
    # print("C: ", catcher)

    sum = first + second + third + ss + lf + cf + rf + pitcher + catcher
    if sum == 0:
        return
    first_ratio = first / sum
    second_ratio = second / sum
    third_ratio = third / sum
    ss_ratio = ss / sum
    lf_ratio = lf / sum
    cf_ratio = cf / sum
    rf_ratio = rf / sum
    pitcher_ratio = pitcher / sum
    catcher_ratio = catcher / sum

    # overlay number of occurrences on spray chart
    img = Image.open("empty_chart.jpg").convert("RGB")  
    font = ImageFont.truetype("arial.ttf", 25) 
    draw = ImageDraw.Draw(img)

    width = img.width
    third_x, third_y = 105, 285
    ss_x, ss_y = 155, 220
    lf_x, lf_y = 65, 150 
    cf_y = 80
    p_y = 290
    c_y = 450


    # Adjust position for text width
    def centered_x(text, x_pos):
        text_width = draw.textbbox((0, 0), str(text), font=font)[2]  # Get text width
        return x_pos - text_width // 2  # Center the text
    
    def blue_value(ratio):
        if ratio == 0:
            return 255
        return round(.5 / ratio)

    # add name to top of photo
    name_text = f"{first_name} {last_name}\n{int(number)}"
    name_x = width // 2  # Center X
    name_y = 20  # Start Y position
    lines = name_text.split("\n")
    line_spacing = 5  # Adjust line spacing if needed
    y_offset = name_y

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)  # Get bounding box (left, top, right, bottom)
        text_width = bbox[2] - bbox[0]  # Calculate text width
        text_height = bbox[3] - bbox[1]  # Calculate text height
        
        draw.text((name_x - text_width // 2, y_offset), line, fill=(0, 0, 0), font=font)
        
        y_offset += text_height + line_spacing  # Move Y position for next line

    draw.text((centered_x(first, width - third_x), third_y), f"{first}", fill=(round(255*first_ratio), 0, blue_value(first_ratio)), font=font)
    draw.text((centered_x(second, width - ss_x), ss_y), f"{second}", fill=(round(255*second_ratio), 0, blue_value(second_ratio)), font=font)
    draw.text((centered_x(third, third_x), third_y), f"{third}", fill=(round(255*third_ratio), 0, blue_value(third_ratio)), font=font)
    draw.text((centered_x(ss, ss_x), ss_y), f"{ss}", fill=(round(255*ss_ratio), 0, blue_value(ss_ratio)), font=font)
    draw.text((centered_x(lf, lf_x), lf_y), f"{lf}", fill=(round(255*lf_ratio), 0, blue_value(lf_ratio)), font=font)
    draw.text((centered_x(cf, width // 2), cf_y), f"{cf}", fill=(round(255*cf_ratio), 0, blue_value(cf_ratio)), font=font)
    draw.text((centered_x(rf, width - lf_x), lf_y), f"{rf}", fill=(round(255*rf_ratio), 0, blue_value(rf_ratio)), font=font)
    draw.text((centered_x(pitcher, width // 2), p_y), f"{pitcher}", fill=(round(255*pitcher_ratio), 0, blue_value(pitcher_ratio)), font=font)
    draw.text((centered_x(catcher, width // 2), c_y), f"{catcher}", fill=(round(255*catcher_ratio), 0, blue_value(catcher_ratio)), font=font)

    img.save(f'spray_chart_pics/{team}/{first_name}_{last_name}.jpg')

