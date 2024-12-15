import os
from dotenv import load_dotenv # For loading environment variables
from social_media_scraper.InstagramBot import InstagramBot
from social_media_scraper.colors import ColorText
import argparse

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
        required=True,
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
    # GUI subcommand
    parser_gui = subparsers.add_parser("gui", help="Run the GUI for managing and visualizing logs.")
    parser_gui.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Log file to load into the GUI."
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the bot
    if args.command == "parse":
        run_bot(args.username, args.headless, args.retries)
    elif args.command == "gui":
        run_gui(args.file)

