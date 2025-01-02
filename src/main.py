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
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member == bot.user:
        return
    
    role = False
    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(payload.guild_id)]

    if str(payload.message_id) in role_config_guild and payload.emoji.name in role_config_guild[str(payload.message_id)]:
        role_id = role_config_guild[str(payload.message_id)][payload.emoji.name]
        role = guild.get_role(role_id)

    if role and member:
            await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    role = False
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
    if guild_id != interaction.guild.id:
        await interaction.response.send_message(
            f"Le lien que vous m'avez fourni provient d'un autre serveur.", 
            ephemeral=True
            )
        return

    guild = interaction.guild
    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)

    bot_highest_role = max(guild.me.roles, key=lambda r: r.position)
    if role.position >= bot_highest_role.position:
        channel = await bot.fetch_channel(channel_id)
        await interaction.response.send_message(
            f"Je ne peux pas attribuer le rôle `{role.name}` car il est au-dessus de mes permissions.",
            ephemeral=True
        )
        return

    try:
        bot_member = guild.get_member(bot.user.id)
        await bot_member.add_roles(role)
        await bot_member.remove_roles(role)
        await message.add_reaction(emoji)
    except discord.NotFound:
        await interaction.response.send_message("Message ou canal introuvable.", ephemeral=True)
        return
    except discord.Forbidden:
        await interaction.response.send_message(
            ("## Un problème est survenu : \n"
            "- Soit je n'ai pas le droit de rajouter une réaction sur ce message.\n"
            "- Soit je n'ai pas le droit de gérer ce rôle."),
            ephemeral=True
            )
        return


    role_config = gestionJson.load_role_config()
    
    if str(guild_id) not in role_config:
        role_config[str(guild_id)] = {}
    
    role_config_guild = role_config[str(guild_id)]
    
    if str(message_id) not in role_config_guild:
        role_config_guild[str(message_id)] = {}
    role_config_guild[str(message_id)][emoji] = role.id

    gestionJson.save_role_config(role_config)
    

    await interaction.response.send_message(
        f"## La réaction {emoji} associée bien associée au rôle `{role.name}` sur le message sélectionné ! \n**Message :**\n {message.content}", ephemeral=True)
    

@bot.slash_command(name="remove_all_reactions", description="Retire toutes les réaction d'un message.")
@discord.option("message_link", str, description="Le lien du message qui contiendra la réaction.")
@commands.has_permissions(manage_roles=True, manage_messages=True)
async def remove_all_reactions(interaction: discord.Interaction, message_link: str):  
    guild_id, channel_id, message_id = fonctions.extract_id_from_link(message_link)    
    if guild_id != interaction.guild.id:
        await interaction.response.send_message(
            f"Le lien que vous m'avez fourni provient d'un autre serveur.", 
            ephemeral=True
            )
        return

    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)
    
    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(guild_id)]
    
    if str(message_id) in role_config_guild:
        del role_config_guild[str(message_id)]
    
    gestionJson.save_role_config(role_config)
    
    try :
        await message.clear_reactions()
    except discord.Forbidden:
        await interaction.response.send_message("Je n'ai pas la permission de supprimer les réactions.", ephemeral=True)
        return
    await interaction.response.send_message(f"## Toutes les réactions ont été supprimées du message sélectionné.\n**Message** : \n{message.content}", ephemeral=True)



@bot.slash_command(name="remove_specific_reaction", description="Retire une réaction spécifique d'un message.")
@discord.option("message_link", str, description="Le lien du message qui contiendra la réaction.")
@discord.option("emoji", str, description="L'émoji de la réaction.")
async def remove_specific_reaction(interaction: discord.Interaction, message_link: str, emoji: str):
    guild_id, channel_id, message_id = fonctions.extract_id_from_link(message_link)    
    if guild_id != interaction.guild.id:
        await interaction.response.send_message(
            f"Le lien que vous m'avez fourni provient d'un autre serveur.", 
            ephemeral=True
            )
        return
    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)

    role_config = gestionJson.load_role_config()
    role_config_guild = role_config[str(guild_id)]

    if str(message_id) in role_config_guild:
        if emoji in role_config_guild[str(message_id)]:
            del role_config_guild[str(message_id)][emoji]
            gestionJson.save_role_config(role_config)
    

    try:
        await message.clear_reaction(emoji)
    except discord.Forbidden:
        await interaction.response.send_message("Je n'ai pas la permission de supprimer les réactions.", ephemeral=True)
        return
    await interaction.response.send_message(f"## L'emoji {emoji} a bien été retiré du message.\n**Message** : \n{message.content}", ephemeral=True)




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

