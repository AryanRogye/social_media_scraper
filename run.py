from selenium.webdriver.chrome.webdriver import WebDriver
import undetected_chromedriver as uc  # For bypassing bot detection
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.common.keys import Keys  # For keyboard actions
from selenium.webdriver.support.ui import WebDriverWait  # For explicit waits
from selenium.webdriver.support import expected_conditions as EC  # For conditions in waits
import time  # For basic sleep delays
from selenium.webdriver.chrome.options import Options

# from fastapi import FastAPI from fastapi.websockets import WebSocket
# import asyncio

# Open Interface
# read inputfile - contains url of direct message link for people
# code opens sum amount of pages
# Wait There
# Next will be sum of amount

def printGreen(text):
    print(f"\033[92m{text}\033[0m")  # Green
def printRed(text):
    print(f"\033[91m{text}\033[0m")    # Red

class InstagramBot:
    def __init__(self, username, password, user_to_scan, headless):
        self.username = username
        self.password = password
        self.user_to_scan = user_to_scan
        self.base_url = 'https://www.instagram.com/'
        self.headless = headless
        self.driver = self.initDriver()

        print("Starting Script")
        self.startScript()
        self.driver.quit()

    def initDriver(self):
        options = Options() # Specify user data directory for Arc browser
        options.add_argument("--user-data-dir=/Users/aryanrogye/Library/Application Support/Google/Chrome/Profile 1")
        options.add_argument("--profile-directory=Default")  # Use the default profile

        # Specify the Arc executable binary
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        if self.headless:
            options.add_argument("--headless")



        # Add other Chrome options for stability
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--profile-directory=Profile 1")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize undetected_chromedriver with the updated options
        driver = uc.Chrome(options=options, use_subprocess=True)
        print("Driver initialized")
        return driver

    def startScript(self) :
        try:
            self.driver.get(self.base_url)
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Phone number, username, or email')]"))
            # )
            # username_input = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Phone number, username, or email')]")
            # username_input.send_keys(self.username)

            # password_input = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Password')]")
            # password_input.send_keys(self.password)

            # login_button = self.driver.find_element(By.XPATH, "//*[contains(@class, 'acan _acap _acas _aj1- _ap30')]")
            # login_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Search')]"))
            )
            search_button = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Search')]")
            search_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Search input')]"))
            )

            search_input = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Search input')]")
            search_input.send_keys(self.user_to_scan)
            search_input.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '" + self.user_to_scan + "')]"))
            )

            user_profile = self.driver.find_element(By.XPATH, "//*[contains(@class, 'x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj') and text()='" + self.user_to_scan + "']")
            user_profile.click()

            # Wait for the <ul> element to be visible
            ul_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'x78zum5 x1q0g3np xieb3on')]"))
            )

            # Find all <li> elements inside the <ul>
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")

            # Extract and print text from each <li>
            # Need to use the index to store the text in a list
            following=""
            followers=""
            posts=""
            try:
                posts = li_elements[0].text
                followers = li_elements[1].text
                following = li_elements[2].text
                # Strip the names
                posts = posts.strip(" posts")
                followers = followers.strip(" followers")
                following = following.strip(" following")

            except Exception:
                print("There was an Error handing the information")

            self.handlePosts(posts)


            
            
            # if following: 
            #     following_text_xpath = f"//*[contains(@class, 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs') and text()='{following}']"
            #     print("Trying Out ", following_text_xpath)
            #     WebDriverWait(self.driver, 10).until(
            #         EC.visibility_of_element_located((By.XPATH, following_text_xpath))
            #     )
            #     following = self.driver.find_element(By.XPATH, following_text_xpath)
            #     following.click()
            #
            #
            #
            # else:
            #     print("Wasnt able to use Following")

            print("Page Title is : %s" % self.driver.title)
        except Exception as e:
            print("Error occurred while trying to access the page ", e)
            exit(1)
        
     
    def handlePosts(self, posts):
        # First Check if Posts Exists
        if posts:
            try:
                # Attempt to convert to a integer
                try:
                    posts = int(posts)
                except ValueError:
                    print("Couldn't convert posts to an int")
                    return
                # No point of Scraping if the posts are 0
                if posts == 0:
                    print("Posts Are 0 Exiting........")
                    return

                printGreen("Looking For Posts......")
                # Wait for the container to load
                post_links = [] # Store the post links
                time.sleep(10)   # Sleep 10 Seconds just cuz intsa takes a little bit of time to load scroll down a bit

                self.driver.execute_script("window.scrollBy(0, 500)")  # Scroll 1000 pixels
                # Wait for the container to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')]"))
                )

                # Locate all <a> elements with the specified class
                links = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')]")

                # Extract the href attribute for each link
                for link in links:
                    href = link.get_attribute("href")
                    # if href and ("/reel/" in href or "/p/" in href):  # Only collect post/reel links
                    post_links.append(href)

                    print("Done looping through the links")
                    for i in post_links:
                        print(i)

                # The post_links has repeats so get rid of them


            except Exception as e:
                print("There was an error looking for the posts", e)
