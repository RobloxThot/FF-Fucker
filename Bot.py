import discord,random,requests
from PIL import Image
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

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
        credits = bytes("\n\n  ____  _\n |  _ \(_)\n | |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n |  _ <| | '_ \| '_ ` _ \ / _ \ '__/ _` |/ _ \ \n | |_) | | | | | | | | | |  __/ | | (_| |  __/\n |____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                    __/ |\n                                   |___/\nCode and bot by: Roblox Thot#0001\nServer help by: red_muta#6029", 'utf-8')

        with open("tempfile", "wb") as file:
            file.write(image + virusFile + credits)

        # send file to Discord in message
        with open("tempfile", "rb") as file:
            await ctx.reply("Your file is:", file=discord.File(file, ctx.message.attachments[0].filename+"_AntiVirus.png"))
    else:
        await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

@bot.command()
@commands.dm_only()
async def merge(ctx, link):
    """Merge 2 given files"""
    image = requests.get(link).content
    virusFile = requests.get(ctx.message.attachments[0].url).content
    credits = bytes("\n\n  ____  _\n |  _ \(_)\n | |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n |  _ <| | '_ \| '_ ` _ \ / _ \ '__/ _` |/ _ \ \n | |_) | | | | | | | | | |  __/ | | (_| |  __/\n |____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                    __/ |\n                                   |___/\nCode and bot by: Roblox Thot#0001\nServer help by: red_muta#6029", 'utf-8')

    with open("tempfile", "wb") as file:
        file.write(image + virusFile + credits)
    
    # send file to dms in message
    with open("tempfile", "rb") as file:
        await ctx.send("Your file is:", file=discord.File(file, ctx.message.attachments[0].filename+"_Merge.png"))
    
    # send file to logs channel
    with open("tempfile", "rb") as file:
        await bot.get_channel(863286796736397333).send(f'New merged file by {ctx.message.author.name}({ctx.message.author.id})\nImage merged with "{ctx.message.attachments[0].filename}"', file=discord.File(file, ctx.message.attachments[0].filename+"_Merge.png"))

    # wipe the temp file bc fuck that
    open("tempfile","w").close()

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    """Shutdown the bot duh"""
    await ctx.bot.logout()

@bot.command()
async def commandName(ctx):
    await bot.send_message(ctx.message.author, "fuck off")

bot.run("")