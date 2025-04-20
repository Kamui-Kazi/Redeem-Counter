import os
from bots import main
import logging

LOGGER: logging.Logger = logging.getLogger("Menu")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_bots():
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bots interrupted. Shutting down cleanly...")

def auth_bots():
    try:
        main(True)
    except KeyboardInterrupt:
        print("\n[!] Authentication interrupted.")

class Menu:
    def __init__(self):
        self.menu_lines = [
            "=== Redeem Counter Bot ===",
            "1. Start the Bots",
            "2. Authenticate the Bots (needs to be run the first time)",
            "3. Guide through creation of .env (WIP)",
            "4. Exit"
        ]
    
    def run(self):
        while True:
            clear_console()
            for line in self.menu_lines:
                print(line)
            choice = input("Select an option: ")
            match choice:
                case "1":
                    clear_console()
                    try:
                        main()
                    except KeyboardInterrupt:
                        print("\n[!] Bots interrupted by user.")
                case "2":
                    clear_console()
                    try:
                        main(auth_mode=True)
                    except KeyboardInterrupt:
                        print("\n[!] Auth interrupted by user.")
                case "3":
                    clear_console()
                    print("WIP")
                case "4":
                    clear_console()
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid choice. Please try again.")