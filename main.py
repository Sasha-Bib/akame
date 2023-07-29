import disnake
from disnake.ext import commands
import os
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, test_guilds=[1027311959038767214])

@bot.event
async def on_ready():
    print("Bot is ready!")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


bot.run("")
