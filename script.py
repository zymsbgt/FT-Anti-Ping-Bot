from parse_dnp import parse
import discord
import secrets

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

no_ping_list = parse()

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
    
    # This is kinda long... should prob modularize
    # https://www.youtube.com/watch?v=SETnK2ny1R0
    if '<@' in user_message:
        cutoff = user_message.index('<@')
        mention = user_message[cutoff + 2:]
        
        # User has a nick
        if user_message.find('!') == 0:
            mention = mention[1:]
        
        # Just to be sure
        end = mention.find('>')
        if end != -1:
            mentionId = mention[:end]
            # Just to be sure 2
            if mentionId.isdigit() and 17 <= mentionId <= 18:
                # Ping may or may not be disallowed
                if mentionId in no_ping_list:
                    alias = no_ping_list[mentionId]
                    user = client.get_user(mentionId)

                    if not alias and user:
                        # If a user was listed with a username-tag
                        # combination instead of an ID
                        alias = no_ping_list[str(user)]

                    if alias or user:
                        # Make sure alias can't ping anyone
                        sender = alias.replace('@', '@\u200b') if alias else str(user)
                        await message.channel.send(f'{username} please **do not ping** {sender}')
    
    if 'Infinite Developer' in username:
        if 'breaking news' in user_message.lower():
            await message.channel.send('🔍 ***Searching for who asked***')

client.run(secrets.TOKEN)