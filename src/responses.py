import discord
import gestionJson, fonctions
from discord.ext import commands

async def generate_list_roles_embed(roles, current_page, total_pages, guild_id, bot: commands.Bot):

    guild = bot.get_guild(guild_id)
    role_config = gestionJson.load_role_config()
    nb_roles = 0
    
    embed=discord.Embed(
            title="Liste des rôles",
            description="Voici ci-dessous la liste de tous rôles attribués avec une réaction à un message.",
            colour=discord.Color(0x00FFFF)
        )
    
    if str(guild_id) in role_config:
        
        role_config_guild = role_config[str(guild_id)]
        
        for message_id in roles:
            channel_id = await fonctions.find_channel_id(bot=bot, message_id=message_id[0], guild_id=guild_id)
            nb_roles += len(message_id[1])
            
            list_roles = ""
            for existing_emoji, existing_role_id in role_config_guild[str(message_id[0])].items():
                role_name = guild.get_role(existing_role_id)
                list_roles += f"{existing_emoji}  **->** `{role_name}`\n"
            
            if list_roles != "" :
                embed.add_field(name='', value='',inline=False)
                embed.add_field(
                    name=f"· https://discord.com/channels/{guild_id}/{channel_id}/{message_id[0]} : ",
                    value=f"{list_roles}",
                    inline=False
                )
    
    embed.set_footer(text=f"Nombre de rôles attribués : {nb_roles}\nPage {current_page + 1}/{total_pages}")

    
    thumbnail_path = "./images/logo_Bot.png"
    thumbnail_file = discord.File(thumbnail_path, filename="logo_Bot.png")
    embed.set_thumbnail(url="attachment://logo_Bot.png")

    image_path = f"./images/banner_Bot.png"
    image_file = discord.File(image_path, filename="banner_Bot.png")
    embed.set_image(url="attachment://banner_Bot.png")

    files =[thumbnail_file,image_file]
    return embed,files


def secret_role(user_message: discord.Message, guild_id: int, channel_id: int):
    
    roles = gestionJson.load_secret_role_config()
    try:
        secret_roles_list = list(roles[str(guild_id)][str(channel_id)].items())
    except KeyError:
        return False, None
    
    for secret_role in secret_roles_list : 
        if user_message == secret_role[0]:
            return True, secret_role[1]
    return False, None


