import json

def load_json(name: str):
    try:
        with open(f"./json/{name}.json","r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json(name:str, data):
    with open(f"./json/{name}.json","w") as file:
        json.dump(data, file, indent=4)


def get_messages_secret_role(guild_id, channel_id):
    try:
        with open("./json/config_secret_roles.json","r") as file:
            data = json.load(file)

        guild_data = data.get(str(guild_id), {})
        channel_data = guild_data.get(str(channel_id), {})
        return list(channel_data.keys())
    
    except:
        return []


if __name__ == "__main__":
    pass
