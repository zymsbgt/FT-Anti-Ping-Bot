import discord
import os
import time
from dotenv import load_dotenv # new discord bot token library

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open('do_not_ping.txt', 'r') as file:
    do_not_ping = [line.strip() for line in file.readlines()]

@client.event
async def on_ready():
    print('server successfully started as {0.user}'.format(client))

@client.event
async def on_message(message):
    response=False
    while not response:
        username = str(message.author).split('#')[0]
        userid = message.author.id
        user_message = str(message.content)
        channel = str(message.channel.name)
        mentioned_users = message.mentions

        if message.author == client.user or message.author.bot:
            return

        for user in mentioned_users:
            if str(user.id) in do_not_ping:
                print(f'{username} in #{channel}: {user_message}')
                userWithoutHashtag = str(user).split('#')[0]
                await message.channel.send(f'{username}, please **do not ping** {userWithoutHashtag}!')
                response = True
        time.sleep(5)

token = os.getenv('DISCORD_TOKEN')
client.run(token)
