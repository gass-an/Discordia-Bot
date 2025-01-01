import re

def extract_id_from_link(link: str):
    ids_match = re.match(r"https://discord\.com/channels/(\d+)/(\d+)/(\d+)", link)
    if ids_match:
        guild_id = int(ids_match.group(1))
        channel_id = int(ids_match.group(2))
        message_id = int(ids_match.group(3))
        return guild_id, channel_id, message_id
    return None, None, None

