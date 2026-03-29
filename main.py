import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
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

bot.run(os.getenv("DISCORD_TOKEN"))
