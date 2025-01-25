import curses
from multiprocessing import Array
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
def run_bot(user_to_scan, headless, max_retries, id_array):
    # Print The Values For The User
    ColorText().printSeparator();
    ColorText().printColored(f"Insta Account:  \t{user_to_scan}", color="blue_4")
    ColorText().printColored(f"Retries Set To: \t{max_retries}",  color="blue_4")
    ColorText().printColored(f"Headless Set To: \t{not headless}",color="blue_4")
    ColorText().printSeparator();
    
    # Get Length of the id_array
    arr_len = len(id_array)
    for i in range(arr_len):
        if i == arr_len // 2:
            ColorText().printColored(f"Avoiding: \t{id_array[i]}\t | Total: {arr_len}", color="yellow")
            continue
        ColorText().printColored(f"Avoiding: \t{id_array[i]}\t |", color="yellow")
    ColorText().printSeparator();

    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    chromedriver_binary = os.getenv("CHROME_PROFILE_LOCATION")

    if not username or not password or not chromedriver_binary:
        ColorText().printColored(".env not set up right", color="red")
        exit(1)
    
    ColorText().printColored(f"Username: {username}", color="green", underline=True)
    ColorText().printColored(f"Chrome Profile: {chromedriver_binary}", color="green", underline=True)
    ColorText().printSeparator();

    # Ask User To Confirm The Values
    ColorText().printColored("Do You Want To Continue? (y/n)", color="yellow")
    user_input = input()
    if user_input.lower() != "y":
        ColorText().printColored("Exiting...", color="red")
        exit(1)

    bot = InstagramBot(
        username=username, 
        password=password, 
        user_to_scan=user_to_scan, 
        headless=headless,
        chromedriver_binary=chromedriver_binary, 
        id_array=id_array,
        max_retries=max_retries
    )
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
    parser_parse.add_argument(
        "-a", "--avoid",
        type=str,
        help="""Enter the id of the reel/post link you want to avoid
        Example link: https://www.instagram.com/dfw.gsxr/reel/DFN41gDPRNF/
        Enter DFN41gDPRNF
        to enter multiple seperate them with commas so
        -a DFN41gDPRNF,.....,....,....
        """
    )
    parser_parse.add_argument(
        "-l", "--likes",
        type=str,
        help="""Enter the id of the reel/post link you want to like.
        WARNING: This will not parse the comments.
        this overrides the avoid list and only likes the post you specify.
        Example ./runp.sh -u "" -a DFN41gDPRNF -l DFN41gDPRNF.
        this will only parse the likes of the post and not the comments.
        """
    )
    parser_parse.add_argument(
        "-c", "--comments",
        type=str,
        help="""Enter the id of the reel/post link you want to comment.
        WARNING: This will not parse the likes.
        this overrides the avoid list and only comments the post you specify.
        Example ./runp.sh -u "" -a DFN41gDPRNF -c DFN41gDPRNF.
        this will only parse the comments of the post and not the likes.
        """
    )

    parser_gui = subparsers.add_parser("gui", help="Lauch The GUI")
    args = parser.parse_args()
    
    # Parse Arguments
    if args.command == "parse":
        id_array = []
        if args.avoid:
            id_array = [id.strip() for id in args.avoid.split(",") if id.strip()]
        id_array = set(id_array)    # Remove duplicates
        id_array = list(id_array)

        username = args.username
        if not args.username:
            # This will get the username from the TUI
            username = curses.wrapper(logsT)

        # Run bot
        run_bot(username, args.headless, args.retries, id_array)
    # Run GUI
    elif args.command == "gui":
        run_gui()
    
