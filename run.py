from sys import exception
import undetected_chromedriver as uc  # For bypassing bot detection
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.common.keys import Keys  # For keyboard actions
from selenium.webdriver.support.ui import WebDriverWait  # For explicit waits
from selenium.webdriver.support import expected_conditions as EC  # For conditions in waits
import time  # For basic sleep delays
from selenium.webdriver.chrome.options import Options
from social_media_scraper.colors import ColorText
import threading
from social_media_scraper.randomizer import Randomizer

# from fastapi import FastAPI from fastapi.websockets import WebSocket
# import asyncio

# Open Interface
# read inputfile - contains url of direct message link for people
# code opens sum amount of pages
# Wait There
# Next will be sum of amount

class InstagramBot:
    def __init__(self, username, password, user_to_scan, headless, max_retries=3):
        self.ct = ColorText()
        self.username = username
        self.password = password
        self.user_to_scan = user_to_scan
        self.base_url = 'https://www.instagram.com/'
        self.headless = headless
        self.max_retries = max_retries
        self.driver = None
        driverThread = threading.Thread(target=self.initDriverWrapper)
        loadingThread = self.ct.getThreadForLoading(100)
        self.ct.loadingWhileScripting(driverThread, loadingThread)

    def initDriverWrapper(self):
        """Wrapper method to initialize the Selenium driver."""
        self.driver = self.initDriver()

    def start(self):
        if self.driver == None:
            self.ct.printColored("Driver is None", color="red")
            return
        self.ct.printColored("Starting Script....", color="green")
        self.startScript()
        self.driver.quit()


    def initDriver(self):
        # Options
        options = Options()
        options.add_argument("--user-data-dir=/Users/aryanrogye/Library/Application Support/Google/Chrome/Profile 1")
        options.add_argument("--profile-directory=Default")  # Use the default profile
    
        # Google Chrome Binary File
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        # This is Set Through the Consutructor
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
        self.ct.printColored("Driver initialized!", color="green")
        return driver

    def startScript(self) :
        if self.driver == None:
            self.ct.printColored("Driver is None", color="red")
            return

        while (self.max_retries >= 0):
            try:
                self.driver.get(self.base_url)
                # THIS IS FOR NOT SIGNED IN
                def signIn():
                    if self.driver == None:
                        return
                    try: 
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Phone number, username, or email')]"))
                        )
                        username_input = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Phone number, username, or email')]")
                        username_input.send_keys(self.username)

                        password_input = self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Password')]")
                        password_input.send_keys(self.password)

                        login_button = self.driver.find_element(By.XPATH, "//*[contains(@class, 'acan _acap _acas _aj1- _ap30')]")
                        login_button.click()
                    except Exception:
                        self.ct.printColored("This Is Good You Are Signed In Already So Nothing U need to do", color="cyan")
                # Retry the search functionality
                # Create threads
                signInThread = threading.Thread(target=signIn)
                loadingThread = self.ct.getThreadForLoading(100,delay=0.3)
                self.ct.loadingWhileScripting(signInThread, loadingThread)

                self.ct.printColored("Navigating back to the home page...", color="cyan")
                self.driver.get(self.base_url)


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
                    self.ct.printColored("There was an Error handing the information", color="red")

                self.handlePosts(posts, self.max_retries)
                self.ct.printColored("Script completed successfully!", color="green")
                break
            except Exception as e:
                self.max_retries -= 1  # Decrement retry count on failure
                self.ct.printColored(f"Error occurred: {e}", color="red")

                if self.max_retries < 0:
                    self.ct.printColored("Max retries reached. Exiting...", color="red")
                    exit(1)  # Exit after retries are exhausted
                else:
                    continue

            finally:
                self.ct.printColored("NO RETRIES USED LETS GOOO", color="green")        
    

    def handlePosts(self, posts, maxTries = 3):
        if self.driver == None:
            return
        # First Check if Posts Exists
        links = []
        if posts:
            try:
                # Attempt to convert to a integer
                try:
                    posts = int(posts)
                except ValueError:
                    self.ct.printColored("Couldn't convert posts to an int", color="red")
                    return
                # No point of Scraping if the posts are 0
                if posts == 0:
                    self.ct.printColored("Posts Are 0 Exiting........", color="red")
                    return

                self.ct.printColored("Waiting For Screen To Load...", color="magenta", underline=True)
                self.ct.coolLoading(10, cooler=True)

                self.ct.printColored("Looking For Posts......", color="green")
                # Wait for the container to load
                post_links = [] # Store the post links
                def scroll():
                    if self.driver == None:
                        return
                    for i in range(maxTries):
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
                        time.sleep(1)
                scrollThread = threading.Thread(target=scroll)
                scrollLoading = self.ct.getThreadForLoading(100)
                self.ct.loadingWhileScripting(scrollThread, scrollLoading)

                self.ct.printColored("Done looping through the links", color="green")
                # The post_links has repeats so get rid of them
                unique_links = set(post_links)
                self.ct.printColored("Done Making UniqueSet", color="blue")
                links = unique_links
            except Exception:
                print("There was an error looking for the posts")
        
        reelsAndPosts = []
        for i in links:
            if ".meme" in f"{i}":
                reelsAndPosts.append(i) 
                self.ct.printColored(i, color="yellow")

        # Over Here Now want to open up a tab with each page
        # Thing is we want to add a delay to all of this cuz we want to look realistic
        size = len(reelsAndPosts) - 1
        rand = Randomizer.randomize_3minutes()
        while(size >= 0):
            rand = Randomizer.randomize_3minutes()
            self.driver.get(reelsAndPosts[0])
            self.getPostCommentUserNames()
            time.sleep(rand)
            size = size - 1

    def getPostCommentUserNames(self):
        # //*[contains(@class, '_a9zc')]
        if self.driver == None:
            return
        try:
            userPath = "//*[contains(@class, 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83')]"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, userPath))
            )
            userNames = self.driver.find_elements(By.XPATH, userPath)
            print(userNames)
        except Exception:
            self.ct.printColored("Something Went wrong getting users from comments", color="red")
        


