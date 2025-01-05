import json


def load_role_config():
    try:
        with open("./json/config_roles.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_role_config(data):
    with open("./json/config_roles.json","w") as file:
        json.dump(data, file, indent=4)


def load_secret_role_config():
    try:
        with open("./json/config_secret_roles.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_secret_role_config(data):
    with open("./json/config_secret_roles.json","w") as file:
        json.dump(data, file, indent=4)


def get_messages_secret_role(guild_id, channel_id):
    print(f"Guild ID: {guild_id}, Channel ID: {channel_id}")
    try:
        with open("./json/config_secret_roles.json","r") as file:
            data = json.load(file)

        guild_data = data.get(str(guild_id), {})
        channel_data = guild_data.get(str(channel_id), {})
        return list(channel_data.keys())
    
    except:
        return []

 


if __name__ == "__main__":
    save_role_config({})
