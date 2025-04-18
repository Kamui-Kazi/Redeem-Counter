def write(data_dict):
    f = open('.env', 'w')
    f.write(f"CLIENT_ID={data_dict["client_id"]}\n")
    f.write(f"CLIENT_SECRET={data_dict["client_secret"]}\n")
    f.write(f"BOT_NAME={data_dict["bot_name"]}\n")
    f.write(f"BOT_ID={data_dict["bot_id"]}\n")
    f.write(f"BOT_PREFIX=\"!\"\n")
    f.write(f"OWNER_NAME={data_dict["owner_name"]}\n")
    f.write(f"OWNER_ID={data_dict["owner_id"]}\n")
    f.write(f"TARGET_NAME={data_dict["target_name"]}\n")
    f.write(f"TARGET_ID={data_dict["target_id"]}\n")
    f.close