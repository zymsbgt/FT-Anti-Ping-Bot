import discord
import os
import time
import pytz
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open('do_not_ping.txt', 'r') as file:
    do_not_ping = [line.strip() for line in file.readlines()]

@client.event
async def on_ready():
    servers = client.guilds
    print("Servers I'm currently in:")
    for server in servers:
        print(server.name)
    print('server successfully started as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    userid = message.author.id
    user_message = str(message.content)
    channel = str(message.channel.name)
    mentioned_users = message.mentions

    if message.author == client.user or message.author.bot:
        return

    for user in mentioned_users:
        if str(user.id) in do_not_ping:
            userWithoutHashtag = str(user).split('#')[0]
            print(f'{username} in #{channel}: {user_message}')
            if message.reference is None: 
                await message.channel.send(f'{username}, please **do not ping** {userWithoutHashtag}!')
            else: # user was ping-replied
                await CheckReply(message, username, userWithoutHashtag)
    
    # This code exists here solely for testing purposes.
    if "anti ping check" in message.content:
        print(f'{username} in #{channel}: {user_message}')
        if message.reference is None: 
            await message.channel.send(f'{username}, please **do not ping** {username}!')
        else: # user was ping-replied
            for user in mentioned_users:
                userWithoutHashtag = str(user).split('#')[0]
                await CheckReply(message, username, userWithoutHashtag)

async def CheckReply(message, username, userWithoutHashtag):
    print('in reply to')
    reply_message = await message.channel.fetch_message(message.reference.message_id)
    print(f'{reply_message}')
    time_difference = datetime.utcnow().replace(tzinfo=pytz.utc) - reply_message.created_at
    if time_difference < timedelta(minutes=30):
        print(f"{message.author} mentioned {userWithoutHashtag} in a reply less than 30 minutes after the original message was sent. Skip sending reminder")
    else:
        print(f"{message.author} mentioned {userWithoutHashtag} in a reply more than 30 minutes after the original message was sent. Ping reminder sent.")
        await message.channel.send(f'{username}, please **do not ping** {userWithoutHashtag}!')
    return

async def on_message_edit(before, after):
    if before.content != after.content:
        pass
    # Check if the edited message mentions any users from 'do_not_ping' list (does not work yet)
    mentioned_users = after.mentions
    for user in mentioned_users:
        if str(user.id) in do_not_ping:
            userWithoutHashtag = str(user).split('#')[0]
            await after.channel.send(f'{userWithoutHashtag} has been mentioned in an edited message. Please **do not ping** them!')

token = os.getenv('DISCORD_TOKEN')
client.run(token)