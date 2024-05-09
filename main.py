import pyautogui
import cv2
import numpy as np
import time
import os
import autoit

debug_mode = False 
threshold = 0.8 # Accuracy-level for images
mouse_move_speed = 0  # Mouse speed movement, I do not reccomend changing this


def find_template(template_path):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
    
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        return center_x, center_y, True
    else:
        return None, None, False


def click_mouse(x, y):
    autoit.mouse_click("left", x, y, 1, mouse_move_speed)


template_paths = ["frisker.png", "fishbone.png", "menos.png", "adjuchas.png", "arrancar.png"]

template_paths = [os.path.abspath('templates/' + template) for template in template_paths]


print("[!] Started")

while True:

    found_any = False
    
    for template_path in template_paths:
        x, y, found = find_template(template_path)
        if found:
            click_mouse(x, y)
            if debug_mode:
                print(f"Found {template_path}")
            found_any = True
            time.sleep(0.2)
    
    if not found_any and debug_mode:
        print("[!] Refreshing search")