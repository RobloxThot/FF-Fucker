import discord,random,requests,os,sys
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)
watermark = "  ____  _\n |  _ \(_)\n | |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n |  _ <| | '_ \| '_ ` _ \ / _ \ '__/ _` |/ _ \ \n | |_) | | | | | | | | | |  __/ | | (_| |  __/\n |____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                    __/ |\n                                   |___/"
memeQuotes = [
    "Trying to not cum",
    "you find what you want here",
    "why are you wasting your time here? go outside and touch grass",
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

class BotChannel(commands.Cog, name="<#863261299487014947> channel commands"):
    """Commands that can only run in <#863261299487014947>"""

    @commands.command(aliases=["t"])
    async def trigger(self, ctx):
        """Make given file trigger antiviruses"""
        if ctx.channel.id == 863261299487014947:
            image = requests.get(ctx.message.attachments[0].url).content
            virusFile = open("virus.zip", 'rb').read()
            credits = bytes(f'\n\n{watermark}\n{random.choice("memeQuotes")}\n\nCode and bot by: Roblox Thot#0001\n\n', 'utf-8')

            with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                file.write(image + virusFile)

            # send file to Discord in message
            with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                await ctx.reply("Your file is:", file=discord.File(file, "BINERGE_AntiVirus_"+ctx.message.attachments[0].filename))

            os.remove("tempfiles/" + str(ctx.message.author.id))
        else:
            await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

class Dms(commands.Cog, name='Dm only commands'):
    """Commands that can only run in Dms with the bot"""

    @commands.command(aliases=["m"])
    @commands.dm_only()
    async def merge(self, ctx, videoOrImage, fileType = "PNG"):
        """Merge 2 given files"""
        image = requests.get(videoOrImage).content
        virusFile = requests.get(ctx.message.attachments[0].url).content
        credits = bytes(f'\n\n{watermark}\n{random.choice("memeQuotes")}\n\nCode and bot by: Roblox Thot#0001\nServer help by: red_muta#6029', 'utf-8')

        with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
            file.write(image + virusFile)

        # send file to dms in message
        with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
            await ctx.send("Your file is:", file=discord.File(file, "BINERGE_Merge_"+ctx.message.attachments[0].filename + fileType))

        # send file to logs channel
        with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
            await bot.get_channel(863286796736397333).send(f'New merged file by {ctx.message.author.name}(https://www.discord.com/users/{ctx.message.author.id})\nImage merged with "{ctx.message.attachments[0].filename}"', file=discord.File(file, "BINERGE_Merge_"+ctx.message.attachments[0].filename + fileType))

        # wipe the temp file bc fuck that
        os.remove("tempfiles/" + str(ctx.message.author.id))

class Misc(commands.Cog, name='Miscellaneous commands'):
    """Some useful/useless commands"""

    @commands.command(aliases=['h'])
    async def help(self, ctx, cmdToLookup = ""):
        """Lists commands dumbass"""
        if cmdToLookup != "":
            await ctx.send_help(cmdToLookup)
        else:
            await ctx.send_help()

class Owner(commands.Cog, name='Owner only commands'):
    """Commands only <@378746510596243458> can run"""

    @commands.command(aliases=["tt"])
    @commands.is_owner()
    async def testtrigger(self, ctx):
        """Make given file trigger antiviruses"""
        if ctx.channel.id == 863671399486717963:
            image = requests.get(ctx.message.attachments[0].url).content
            virusFile = open("virus.txt", 'rb').read() + open("virus2.zip", 'rb').read()

            with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                file.write(image + virusFile)

            # send file to Discord in message
            with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                await ctx.reply("Your file is:", file=discord.File(file, "BINERGE_AntiVirus_"+ctx.message.attachments[0].filename))

            os.remove("tempfiles/" + str(ctx.message.author.id))
        else:
            await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot or shut it down if it's not in a loop!"""
        await ctx.bot.logout()

    @commands.command(aliases=["s"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.bot.logout()
        sys.exit()


#region Error handeling
@Dms.merge.error
async def merge_error(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply(f'Please use DMs not <#{ctx.channel.id}>')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Please give the link you want to merge.\nUsage is in <#863261299286343697> or dm **<@378746510596243458>** for more help!')

@Owner.restart.error
async def restart_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        await ctx.reply(f'Sorry but you can\'t shut down a bot you don\'t own lmao.')

@Owner.testtrigger.error
async def testtrigger_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        await ctx.reply(f'Sorry but you can\'t use the test CMD as it\'s for Thot only.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.reply("That command wasn't found! Sorry :(")
#endregion

#region Setup classes for the bot
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='```fix\n ____  _\n|  _ \(_) \n| |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n|  _ <| | \'_ \| \'_ ` _ \ / _ \ \'__/ _` |/ _ \ \n| |_) | | | | | | | | | |  __/ | | (_| |  __/\n|____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                   __/ |\n                                  |___/```')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
bot.help_command = MyHelpCommand()

#Add command Classes
bot.remove_command('help')

bot.add_cog(Dms())
bot.add_cog(Misc())
bot.add_cog(Owner())
bot.add_cog(BotChannel())

#endregion

bot.run("ODYzMjU4NDk1ODcyOTI1NzI2.YOkSHw.HlhLGdUwBCKmDmBJ9tPpUudRFpY")