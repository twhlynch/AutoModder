import discord, subprocess
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot_token = ""
request_channel_id = 10000000000000000
guild_id = 100000000000000

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Ready!")

@tree.command(
    name='mod',
    description='Request a modded APK (name, URL, or list of names/URLs)'
)
async def submit(interaction: discord.Interaction, app_list: str):
    user_id = interaction.user.id
    await interaction.response.send_message(f'Request for `{app_list}` submitted.')
    subprocess.Popen(["python", "download_apk.py", app_list])

client.run(bot_token)
