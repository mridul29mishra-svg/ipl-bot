import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# -------------------- FLASK KEEP ALIVE --------------------

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))  # Railway PORT fix
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------- DISCORD BOT --------------------

intents = discord.Intents.default()
intents.message_content = True  # Fix warning

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Check if bot is working")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Bot is working!")

@bot.tree.command(name="help", description="Show all commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="📖 Help Menu", color=0x00ff00)
    embed.add_field(name="/balance", value="Check your coins", inline=False)
    embed.add_field(name="/leaderboard", value="Top players", inline=False)
    embed.add_field(name="/history", value="Your bets", inline=False)
    embed.add_field(name="/matches", value="Upcoming IPL matches", inline=False)
    await interaction.response.send_message(embed=embed)

# -------------------- START BOT --------------------

keep_alive()  # start web server
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("ERROR: Bot token not found. Set DISCORD_TOKEN in Railway.")
else:
    bot.run(token)
