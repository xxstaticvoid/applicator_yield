from PIL import ImageGrab, ImageShow, Image
import time, os, os.path
import re

import numpy as np
import pytesseract


minute_yields = [0]
cwd = os.getcwd()
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\aurjeber\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'



def delete_file(file_path) -> bool:
    if os.path.exists(file_path):
        time.sleep(1)
        os.remove(file_path)

def capture_screen():
    try:
        kpi_screen_shot = ImageGrab.grab()
        filename = f"APP_KPI.png"
        kpi_screen_shot.save(filename)
    except:
        print("Error in screenshot")
        exit(1)
    else:
        #print(f"{filename} saved in {cwd}")
        #^^^ UNCOMMENT TO SHOW WHERE FILE WAS STORED
        #ONLY USEFUL FOR TROUBLESHOOTING
        kpi_file_path = os.path.join(cwd, filename)

        total_and_reject_bbox = (214, 176, 288, 331)
        try:
            cropped_image = kpi_screen_shot.crop(total_and_reject_bbox)
        except:
            print("Invalid crop cordinates")
            exit(1)
        else:
            cropped_image = cropped_image.resize( (100, 200) )
            crop_filename = f"APP_Parts.png"
            cropped_image.save(crop_filename)
            cropped_file_path = os.path.join(cwd, crop_filename)
            #ImageShow.show(cropped_image)
            #^^^ UNCOMMENT TO VIEW IMAGE AFTER EACH CAPTURE
            #ONLY USEFUL FOR TROUBLESHOOTING
        
        delete_file(kpi_file_path)

        return crop_filename

        

def extract_nums_from_png(image):
    find_attempts = 0
    text = pytesseract.image_to_string(image)
    #print(f"Found: {text} in image")
    #^^^ UNCOMMENT IF YOU WANT TO PRINT TEXT FOUND IN IMAGE
    #ONLY USEFUL FOR TROUBLESHOOTING
    text.strip()
    text = re.sub(',', '', text)
    numbers = re.findall(r"\d+", text)
    
    nums = [int(x) for x in numbers]
    if len(nums) == 2:
        #delete_file(os.path.join(cwd, "APP_Parts.png"))
        #^^^ COMMENT OUT IF YOU WANT TO KEEP IMAGE
        return nums
    elif find_attempts < 5:
        extract_nums_from_png(image)
    else:
        print("Couldn't find numbers in image")
        exit(1)

def get_data(minute_data, last_hour_good: int, last_hour_total: int, last_hour_rejects: int) -> float:

    good_parts_this_hour = minute_data[0] - last_hour_good
    rejected_parts_this_hour = minute_data[1] - last_hour_rejects
    total_this_hour = good_parts_this_hour + rejected_parts_this_hour
    print(total_this_hour, good_parts_this_hour)
    current_yield = good_parts_this_hour / total_this_hour
    return round(current_yield, 6)


def main() -> None:


    time.sleep(10)
    minute_counter = 0

    try:
        f = open("data.txt", "x")
    except:
        open("data.txt", "w").close()
    else:
        f.close()


    while True:
        cropped_image_file = capture_screen()
        image = Image.open(os.path.join(cwd, cropped_image_file))
        curr_numbers = extract_nums_from_png(image)

        current_time_struct = time.localtime()
        current_time = time.strftime("%H:%M:%S", current_time_struct)
        if(minute_counter == 0 or minute_counter % 60 == 0):
            last_hour_rejects = curr_numbers[1]
            last_hour_good_parts = curr_numbers[0]
            last_hour_total = last_hour_rejects + last_hour_good_parts
            print(f"Start of hour... Target Data: {last_hour_good_parts}, {last_hour_total}  -> {last_hour_good_parts / last_hour_total}")
        else:
            current_yield = get_data(curr_numbers, last_hour_good_parts, last_hour_total, last_hour_rejects)
            minute_yields.append(current_yield) #Add current minute yield to list
            with open("data.txt", "a") as f:
                f.write(str(minute_yields[-1]) + "\n")
            print(f"{current_time} - {current_yield}")
        time.sleep(55)
        minute_counter += 1
    
#RUN APPLICATION
main()
