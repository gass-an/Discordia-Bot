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





if __name__ == "__main__":
    save_role_config({})
