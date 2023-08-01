import os, time, shutil, requests, discord

async def discordAnnounce(message):
    bot_token = "YOUR_BOT_TOKEN_HERE"
    announce_channel_id = 10000000000000000
    guild_id = 100000000000000

    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        guild = bot.get_guild(guild_id)
        announce_channel = guild.get_channel(announce_channel_id)

        if announce_channel:
            await announce_channel.send(f"{message} ||@everyone||")

        await bot.close()

    await bot.start(bot_token)

def upload_apks(list, folder, output):
    for name in list:
        if name.endswith(".apk") and name.startswith("modded-"):
            if not os.path.exists(output):
                os.makedirs(output)
            print(f"Uploading {name}")
            url = 'https://store1.gofile.io/uploadFile'
            with open(name, 'rb') as file:
                files = {'file': (name, file)}
                response = requests.post(url, files=files)

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok':
                    discordAnnounce(f"## {data['data']['fileName']} uploaded to {data['data']['downloadPage']}")
            shutil.copy(name, os.path.join(output, name))
            os.remove(name)

def scan_folder(folder):
    while True:
        files = os.listdir(folder)
        if files:
            upload_apks(files, folder, 'apks')
        time.sleep(5)

if __name__ == "__main__":
    scan_folder(os.path.dirname(os.path.realpath(__file__)))