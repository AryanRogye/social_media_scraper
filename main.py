import curses
import os
from dotenv import load_dotenv # For loading environment variables
from backend.social_media_scraper.InstagramBot import InstagramBot
from backend.social_media_scraper.colors import ColorText
import argparse
from backend.social_media_scraper.db import db
from backend.social_media_scraper.logs_parser_tui import logsT

def run_gui(file):
    print("GUIIIII")
    pass
def run_bot(user_to_scan, headless, retries):
    # Print The Values For The User
    ColorText().printColored(f"Checking {user_to_scan} Insta Account", color="cyan", underline=True)
    ColorText().coolerLoading(10)
    ColorText().printColored(f"Retries Set To: |{retries}|", color="green", underline=True)
    ColorText().coolerLoading(10)
    ColorText().printColored(f"Headless Set To:  |{headless}|", color="green", underline=True)
    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    bot = InstagramBot(username, password, user_to_scan, headless, retries)
    bot.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Instagram Bot.")
    # Define subcommands
    subparsers = parser.add_subparsers(dest="command", required=True, help="Choose a mode to run: parse or gui")

    # Parser subcommand
    parser_parse = subparsers.add_parser("parse", help="Run the parser to scrape Instagram accounts.")
    parser_parse.add_argument(
        "-u", "--username",
        type=str,
        help="Instagram username to parse."
    )
    parser_parse.add_argument(
        "-r", "--retries",
        type=int,
        default=3,
        help="Maximum retries for errors. Default: 3."
    )
    parser_parse.add_argument(
        "-head", "--headless",
        action="store_false",
        help="Run browser with a visible window (default: headless mode On)."
    )
    
    # Parse arguments
    args = parser.parse_args()
    username = args.username
    if args.command == "parse":
        if not args.username:
            print("No username provided. Please specify --username or choose a saved username.")
            # Add logic to pick a username from logs or exit
            username = curses.wrapper(logsT)
        run_bot(username, args.headless, args.retries)
    elif args.command == "gui":
        run_gui(args.file)
    
