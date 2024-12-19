from selenium.webdriver import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import sys
import json

def open_google():
    # Configure undetected_chromedriver options
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

    # Initialize undetected_chromedriver
    driver = uc.Chrome(options=options)

    try:
        # Open the browser and maximize the window
        driver.set_window_size(800, 600)  # Set an initial window size
        screen_width = driver.execute_script("return window.screen.availWidth;")
        screen_height = driver.execute_script("return window.screen.availHeight;")
        
        # Calculate bottom-right position
        bottom_right_x = screen_width - 200  # Subtract the browser's width
        bottom_right_y = screen_height - 200  # Subtract the browser's height

        driver.set_window_position(bottom_right_x, bottom_right_y)  # Move to bottom-right

        # Open Google
        driver.get("https://www.google.com")
        print("Opened Google successfully!")

        # Wait for a few seconds to see the result
        while (True):
            print()

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    users_json = sys.argv[1]
    users = json.loads(users_json)
    for user in users:
        print(user)
    open_google()
