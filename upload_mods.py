import os, shutil, requests, discord

with open(".token", "r") as f:
    bot_token = f.read().strip()
announce_channel_id = 1135368470679277670
guild_id = 1135362081454043286

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    guild = bot.get_guild(guild_id)
    announce_channel = guild.get_channel(announce_channel_id)
    while True:
        await scan_folder(os.path.dirname(os.path.realpath(__file__)), announce_channel)

async def scan_folder(folder, announce_channel):
    list = os.listdir(folder)
    if list:
        output = "apks"
        for name in list:
            if name.endswith(".apk") and name.startswith("modded-"):
                if not os.path.exists(output):
                    os.makedirs(output)
                print(f"Uploading {name}")
                res = requests.get("https://api.gofile.io/getServer")
                server = "store10"
                if res.status_code == 200:
                    server = res.json()["data"]["server"]
                url = f'https://{server}.gofile.io/uploadFile'
                print(url)
                with open(name, 'rb') as file:
                    files = {'file': (name, file)}
                    response = requests.post(url, files=files)
                print(response)
                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    if data['status'] == 'ok':
                        print(f"## {data['data']['fileName']} uploaded to {data['data']['downloadPage']}")
                        await announce_channel.send(f"## {data['data']['fileName']} uploaded to {data['data']['downloadPage']} ||@everyone||")
                shutil.copy(name, os.path.join(output, name))
                os.remove(name)

bot.run(bot_token)