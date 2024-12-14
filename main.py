import os
from dotenv import load_dotenv # For loading environment variables
from social_media_scraper.InstagramBot import InstagramBot
import argparse


def run_bot():
    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    # user_to_scan = 'aryan_rogye'
    user_to_scan = "chillguy.meme"
    bot = InstagramBot(username, password, user_to_scan, True, max_retries=2)
    bot.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Instagram Bot.")
    parser.add_argument(
        "-h",
        type=str,
        default="",
        help=""
    )
    parser.add_argument(
        "-u", "--username",
        type=str,
        default="",
        help="Instagram username to Parse"            
    )
    parser.add_argument(
        "-p", "--parse",
        type=bool,
        default=False,
        help="To Activate Parser",
    )
    run_bot()
