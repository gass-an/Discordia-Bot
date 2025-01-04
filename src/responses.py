import discord
import gestionJson, fonctions
from discord.ext import commands

async def generate_list_roles_embed(roles, current_page, total_pages, guild_id, bot: commands.Bot):
    
    guild = bot.get_guild(guild_id)
    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(guild_id)]
    nb_roles = 0

    embed=discord.Embed(
            title="Liste des rôles",
            description="Voici ci-dessous la liste de tous rôles attribués avec une réaction à un message.",
            colour=discord.Color(0xFF0000)
        ) 

    for message_id in roles:
        channel_id = await fonctions.find_channel_id(bot=bot, message_id=message_id[0], guild_id=guild_id)
        nb_roles += len(message_id[1])
        
        list_roles = ""
        for existing_emoji, existing_role_id in role_config_guild[str(message_id[0])].items():
            role_name = guild.get_role(existing_role_id)
            list_roles += f"{existing_emoji}  **->** `{role_name}`\n"
        
        embed.add_field(name='', value='',inline=False)
        embed.add_field(
            name=f"· https://discord.com/channels/{guild_id}/{channel_id}/{message_id[0]} : ",
            value=f"{list_roles}",
            inline=False
        )
    
    embed.set_footer(text=f"Nombre de rôles attribués : {nb_roles}\nPage {current_page + 1}/{total_pages}")


    thumbnail_path = "./images/logo_PillboxHospital.png"
    thumbnail_file = discord.File(thumbnail_path, filename="logo_PillboxHospital.png")
    embed.set_thumbnail(url="attachment://logo_PillboxHospital.png")

    image_path = f"./images/banner_PillboxHospital.png"
    image_file = discord.File(image_path, filename="banner_PillboxHospital.png")
    embed.set_image(url="attachment://banner_PillboxHospital.png")

    files =[thumbnail_file,image_file]

    return embed,files


