import os
import logging

LOGGER: logging.Logger = logging.getLogger("Env Creator")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class Setup_Guide:
    def __init__(self):
        self.into_lines = [
            "=== Redeem Counter Bot ===",
            "====== Setup  Guide ======",
            "First things First, you MUST have a python enviroment set up,",
            "either a virtual enviroment or a system wide environment.",
            "you must be using python 3.11 or higher (python 3.14 is not fully compatable)",
            "install the python modules using `pip install requirements.txt`", 
            "This bot will require 2 twitch accounts",
            "1 bot account and 1 streamer account.",
            "there are 4 steps to use this bot:"
            "1. create a twitch app.",
            "2. set up the enviroment variables in '.env'",
            "3. autherize the bots",
            "4. run the bots",
            "where would you like to start?",
            "selection: "
        ]
        self.app_lines = [
            "=== Redeem Counter Bot ===",
            "====== Setup  Guide ======",
            "====== App Creation ======"
            "The first thing you need to do is create a twitch app.",
            "To begin, as the streamer's account visit 'https://dev.twitch.tv/console'",
            "On the left panel select Applications",
            "Then left panel"

        ]
    
    def start(self):
        clear_console()
        for i in range(self.into_lines.__len__()-2):
            print(self.into_lines[i])
        selection = input(self.into_lines[len-1])
        match selection:
            case 1:
                self.setup_app()
            case 2:
                self.setup_env()
            case 3:
                self.setup_auth()
            case 4:
                self.setup_run()
            case _:
                pass
    
    def setup_app(self):
        pass

    def setup_env(self):
        pass

    def setup_auth(self):
        pass

    def setup_run(self):
        pass
                