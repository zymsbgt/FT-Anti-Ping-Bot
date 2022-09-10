import discord
import secrets

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('server successfully started as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    userid = message.author.id
    user_message = str(message.content)
    channel = str(message.channel.name)
    
    print(f'{username} in #{channel}: {user_message}')
    
    if message.author == client.user:
        return
    
    if '<@343451476137607179>' in user_message.lower():
        await message.channel.send(f'{username}, please **do not ping** FlashTeens!')
        #await message.channel.send(f'{message.author.mention}, please **do not ping** FlashTeens!')
        
    if userid == 688311805319053336:
        if '<@559210445991444480>' in user_message.lower():
            await message.channel.send(f'{username}, please **do not ping** SprigatitoOTS!')
    
    if 'Infinite Developer' in username:
        if 'breaking news' in user_message.lower():
            await message.channel.send('🔍 ***Searching for who asked***')

client.run(secrets.TOKEN)