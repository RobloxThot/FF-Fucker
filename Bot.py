import discord,random,requests,os
from PIL import Image
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)
watermark = "  ____  _\n |  _ \(_)\n | |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n |  _ <| | '_ \| '_ ` _ \ / _ \ '__/ _` |/ _ \ \n | |_) | | | | | | | | | |  __/ | | (_| |  __/\n |____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                    __/ |\n                                   |___/"
memeQuotes = [
    "Trying to not cum",
    "can you find what you want here?",
    "hi skid",
    "why are you wasting your time here? go outside and get a partner",
    "why are you wasting your time here? go outside and touch your mom",
    "Sponsored by raycon earbuds",
    "This file is sponsored by nord vpn",
#   "",
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(
        activity=discord.Game(name="with viruses. ☣️")
    )

    print('------')

@bot.command()
async def trigger(ctx):
    """Make given file trigger antiviruses"""
    if ctx.channel.id == 863261299487014947:
        image = requests.get(ctx.message.attachments[0].url).content
        virusFile = open("MEMZ-Clean.bat", 'rb').read()
        credits = bytes(f'\n\n{watermark}{random.choice("memeQuotes")}\n\nCode and bot by: Roblox Thot#0001\n\n', 'utf-8')

        with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
            file.write(image + virusFile)

        # send file to Discord in message
        with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
            await ctx.reply("Your file is:", file=discord.File(file, ctx.message.attachments[0].filename+"_AntiVirus.png"))
        
        os.remove("tempfiles/" + str(ctx.message.author.id))
    else:
        await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

@bot.command()
@commands.dm_only()
async def merge(ctx, link):
    """Merge 2 given files"""
    image = requests.get(link).content
    virusFile = requests.get(ctx.message.attachments[0].url).content
    credits = bytes(f'\n\n{watermark}{random.choice("memeQuotes")}\n\nCode and bot by: Roblox Thot#0001\nServer help by: red_muta#6029', 'utf-8')

    with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
        file.write(image + virusFile + credits)
    
    # send file to dms in message
    with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
        await ctx.send("Your file is:", file=discord.File(file, ctx.message.attachments[0].filename+"_Merge.png"))
    
    # send file to logs channel
    with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
        await bot.get_channel(863286796736397333).send(f'New merged file by {ctx.message.author.name}({ctx.message.author.id})\nImage merged with "{ctx.message.attachments[0].filename}"', file=discord.File(file, ctx.message.attachments[0].filename+"_Merge.png"))

    # wipe the temp file bc fuck that
    os.remove("tempfiles/" + str(ctx.message.author.id))

@bot.command(aliases=["shutdown"])
@commands.is_owner()
async def restart(ctx):
    """Restart the bot duh!"""
    await ctx.bot.logout()

bot.run("ODYzMjU4NDk1ODcyOTI1NzI2.YOkSHw.HlhLGdUwBCKmDmBJ9tPpUudRFpY")