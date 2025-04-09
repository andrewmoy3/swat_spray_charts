import os 
import numpy as np  
import pandas as pd
from PIL import Image
import tempfile
import cv2
from fpdf import FPDF

def stitch_to_pdf(team):   
    output_pdf = f'pdfs/{team}.pdf'
    PAGE_WIDTH = 612  # 8.5 inches * 72 dpi
    PAGE_HEIGHT = 792  # 11 inches * 72 dpi
    MARGIN = 20
    MAX_WIDTH = PAGE_WIDTH - 2 * MARGIN
    MAX_HEIGHT = PAGE_HEIGHT - 2 * MARGIN
    COL_SPACING = 10

    images = [] 
    tutorial = Image.open("tutorial.png")
    images.append(tutorial)

    roster = pd.read_csv(f'rosters/{team}.csv').sort_values(by="Number", ascending=True) 
    for index, row in roster.iterrows():
        first_name = row['First Name'].strip()
        last_name = row['Last Name'].strip()
        image_path = f'spray_chart_pics/{team}/{first_name}_{last_name}.jpg'
        if os.path.exists(image_path):
            images.append(Image.open(image_path))
            
    # images = [Image.open(os.path.join(image_folder, img)) for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images = [img.convert("RGB") for img in images]
    pdf = FPDF(unit="pt", format="letter")
    pdf.add_page()
    x, y = MARGIN, MARGIN
    row_height = 0
    for img in images:
        img = img.resize((MAX_WIDTH // 2 - COL_SPACING, MAX_HEIGHT // 3)) 
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
