from selenium.webdriver import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
import json

# Function to save updates to the JSON file
def update_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to update the 'Checked' status in the JSON file
def mark_as_checked(file_path, instagram_url):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Update the 'Checked' field for the matching Instagram URL
    for user in data:
        if user.get("Instagram Account") == instagram_url:
            user["Checked"] = True
            break

    # Write the updated data back to the file
    update_json_file(file_path, data)

# Function to open Instagram accounts
def open_instagram_accounts(users, file_path):
    # Configure undetected_chromedriver options
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument("--user-data-dir=/Users/aryanrogye/Library/Application Support/Google/Chrome/Profile 1")
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--profile-directory=Profile 1")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    print("Options Loading")

    try:
        driver.set_window_size(800, 600)
        screen_width = driver.execute_script("return window.screen.availWidth;")
        screen_height = driver.execute_script("return window.screen.availHeight;")

        bottom_right_x = screen_width - 200
        bottom_right_y = screen_height - 200
        driver.set_window_position(bottom_right_x, bottom_right_y)

        for i, user in enumerate(users):
            instagram_url = user.get("Instagram Account")
            if not instagram_url:
                print(f"No Instagram Account found for user: {user}")
                continue

            if i == 0:
                time.sleep(3)
                # Open the first account in the current tab
                driver.get(instagram_url)
            else:
                # Open a new blank tab
                driver.switch_to.new_window('tab')

                # Switch to the newly created tab (last handle)
                driver.switch_to.window(driver.window_handles[-1])

                # Load the Instagram URL in the new tab
                driver.get(instagram_url)

            print(f"Opened Instagram Account: {instagram_url}")
            
            # Mark the account as checked in the file
            mark_as_checked(file_path, instagram_url)

        print("All Instagram accounts opened in separate tabs. Press Ctrl+C to close.")
        while True:
            time.sleep(1)

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    users_json = sys.argv[1]
    file_edit = sys.argv[2]
    if not users_json or not file_edit:
        print("Args Invalid")
        exit(1)
    users = json.loads(users_json)
    open_instagram_accounts(users, file_edit)
