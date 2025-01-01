from typing import Final
from dotenv import load_dotenv
import os,discord,json
from discord.ext import commands, tasks
import fonctions, gestionJson


# --------------------------- Récupération des infos dans le .env  (Token / ids) ---------------------
load_dotenv()
TOKEN: Final[str] = os.getenv('discord_token')


# ------------------------------------ Initialisation du bot  ----------------------------------------
intents = discord.Intents.default()
intents.message_content = True  # NOQA
intents.guilds = True
intents.members = True
bot = commands.Bot(intents=intents)


# ------------------------------------ Démarrage du bot  ---------------------------------------------
@bot.event
async def on_ready():
    try:
        # Synchronisation des commandes globales
        await bot.sync_commands()
        print("\nLes commandes globales ont été synchronisées.")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")
    
    print(f"{bot.user} est en cours d'exécution !\n")


# ------------------------------------ Gestion des rôles  --------------------------------------------

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(payload.guild_id)]

    if str(payload.message_id) in role_config_guild and payload.emoji.name in role_config_guild[str(payload.message_id)]:
        guild = bot.get_guild(payload.guild_id)
        role_id = role_config_guild[str(payload.message_id)][payload.emoji.name]
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)

    if role and member:
        await member.add_roles(role)



@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(payload.guild_id)]

    if str(payload.message_id) in role_config_guild and payload.emoji.name in role_config_guild[str(payload.message_id)]:
        guild = bot.get_guild(payload.guild_id)
        role_id = role_config_guild[str(payload.message_id)][payload.emoji.name]
        role = guild.get_role(role_id)
        member = guild.get_member(payload.user_id)

    if role and member:
        await member.remove_roles(role)

# ------------------------------------ Commandes du bot  ---------------------------------------------

# /ping (répond : Pong!) 
@bot.slash_command(name="ping",description="Ping-pong (pour vérifier que le bot est bien UP !)")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("Pong !")



@bot.slash_command(name="add_reaction_role", description="Associe une réaction sur un message défini à un rôle.")
@discord.option("message_link", str, description="Le lien du message qui contiendra la réaction.")
@discord.option("emoji", str, description="L'émoji de la réaction.")
@discord.option("role", discord.Role, description="Le rôle attribué.")
@commands.has_permissions(manage_roles=True)
async def add_reaction_role(interaction: discord.Interaction, message_link: str, emoji: str, role: discord.Role):  
    
    guild_id, channel_id, message_id = fonctions.extract_id_from_link(message_link)    
    role_config = gestionJson.load_role_config()

    if str(guild_id) not in role_config:
        role_config[str(guild_id)] = {}
    
    role_config_guild = role_config[str(guild_id)]
    
    if str(message_id) not in role_config_guild:
        role_config_guild[str(message_id)] = {}
    role_config_guild[str(message_id)][emoji] = role.id

    gestionJson.save_role_config(role_config)

    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)
    await message.add_reaction(emoji)

    await interaction.response.send_message(
        f"Réaction {emoji} associée au rôle @{role.name} pour le message sélectionné : \nMessage : {message.content}", ephemeral=True)
    






# ------------------------------------ Gestion des erreurs de permissions  ---------------------------
@bot.event
async def on_application_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRole):
        await interaction.response.send_message(
            "Vous n'avez pas le rôle requis pour utiliser cette commande.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "Une erreur est survenue lors de l'exécution de la commande.",
            ephemeral=True
        )


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()

