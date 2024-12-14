import os
from dotenv import load_dotenv # For loading environment variables
from run import InstagramBot


def run_bot():
    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    # user_to_scan = 'aryan_rogye'
    user_to_scan = "chillguy.meme"
    bot = InstagramBot(username, password, user_to_scan, True, max_retries=4)
    bot.start()

if __name__ == '__main__':
    run_bot()
