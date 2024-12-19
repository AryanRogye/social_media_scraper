import curses
import os
from dotenv import load_dotenv
from undetected_chromedriver import subprocess # For loading environment variables
from backend.social_media_scraper.InstagramBot import InstagramBot
from backend.social_media_scraper.colors import ColorText
import argparse
from backend.social_media_scraper.logs_parser_tui import logsT

def run_gui():
    script_path = os.path.join(os.path.dirname(__file__), "./backend/runG")
    ColorText().coolerLoading(10)
    ColorText().printColored("Launching GUI", color="green")
    try:
        subprocess.run(["sh", script_path], check=True)
        ColorText().printColored("Success Launching GUI", color="green")
        return
    except subprocess.CalledProcessError as e:
        ColorText().printColored(f"Error Launching GUI: {e}", color="red")
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

    parser_gui = subparsers.add_parser("gui", help="Lauch The GUI")
    
    # Parse arguments
    args = parser.parse_args()
    if args.command == "parse":
        username = args.username
        if not args.username:
            username = curses.wrapper(logsT)
        run_bot(username, args.headless, args.retries)
    elif args.command == "gui":
        run_gui()
    
