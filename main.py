import os
from dotenv import load_dotenv # For loading environment variables
from social_media_scraper.InstagramBot import InstagramBot


def run_bot():
    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    # user_to_scan = 'aryan_rogye'
    user_to_scan = "chillguy.meme"
    bot = InstagramBot(username, password, user_to_scan, False, max_retries=5)
    bot.start()

if __name__ == '__main__':
    run_bot()
