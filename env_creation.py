import os
import logging

LOGGER: logging.Logger = logging.getLogger("Env Creator")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class Env_Creation:
    def __init__(self):
        self.menu_lines = [
            "=== Redeem Counter Bot ===",
            "====== .env creator ======",
            "The following prompts are regarding your twitch app.",
            "Client ID: ",
            "Client Secret: ",
            "The following prompts are regarding the Streamer's twitch account.",
            "Streamer Name: ",
            "Streamer ID: ",
            "The following prompts are regarding the Bot's twitch account.",
            "Bot Name: ",
            "Bot ID: ",
        ]
    
    def create(self):
        self.env_data = []
        clear_console()
        for i in range(self.menu_lines.__len__()):
            match i:
                case 3:
                    client_id = input(self.menu_lines[i]) 
                case 4:
                    client_secret = input(self.menu_lines[i])
                case 6:
                    streamer_name = input(self.menu_lines[i])
                case 7:
                    streamer_id = input(self.menu_lines[i])
                case 9:
                    bot_name = input(self.menu_lines[i])
                case 10:
                    bot_id = input(self.menu_lines[i])
                case _:
                    print(self.menu_lines[i])
        
        data_dict = {
            'client_id' : client_id,
            'client_secret' : client_secret,
            'bot_name_1' : streamer_name,
            'bot_id_1' : streamer_id,
            'bot_name_2' : bot_name,
            'bot_id_2' : bot_id,
            'owner_name' : streamer_name,
            'owner_id' : streamer_id,
            'target_name' : streamer_name,
            'target_id' : streamer_id,
        }
        self.write(data_dict)
        LOGGER.info(".env written sucesfully")
        
    
    def write(self, data_dict):
        f = open('.env', 'w')
        f.write(f"CLIENT_ID={data_dict["client_id"]}\n")
        f.write(f"CLIENT_SECRET={data_dict["client_secret"]}\n")
        f.write(f"BOT_NAME_1={data_dict["bot_name_1"]}\n")
        f.write(f"BOT_ID_1={data_dict["bot_id_1"]}\n")
        f.write(f"BOT_NAME_2={data_dict["bot_name_2"]}\n")
        f.write(f"BOT_ID_2={data_dict["bot_id_2"]}\n")
        f.write(f"BOT_PREFIX=\"!\"\n")
        f.write(f"OWNER_NAME={data_dict["owner_name"]}\n")
        f.write(f"OWNER_ID={data_dict["owner_id"]}\n")
        f.write(f"TARGET_NAME={data_dict["target_name"]}\n")
        f.write(f"TARGET_ID={data_dict["target_id"]}\n")
        f.close
                