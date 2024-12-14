import threading

from run import InstagramBot


def run_bot():
    # GET FROM ENVIRONMENT VARIABLES
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    # user_to_scan = 'aryan_rogye'
    user_to_scan = "chillguy.meme"
    bot = InstagramBot(username, password, user_to_scan, True)

if __name__ == '__main__':
    run_bot()
