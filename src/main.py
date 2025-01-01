from typing import Final
from dotenv import load_dotenv
import os,discord,json
from discord.ext import commands, tasks


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
    
    print(f"{bot.user} est en cours d'exécution !")












# ------------------------------------ Gestion des erreurs de permissions  ------------------------------------
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

