import discord,random,requests,os,sys,ffmpeg
import datetime, time
from discord.ext import commands
from bs4 import BeautifulSoup
from pytube import YouTube

start_time = time.time()
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)
watermark = "  ____  _\n |  _ \(_)\n | |_) |_ _ __  _ __ ___   ___ _ __ __ _  ___\n |  _ <| | '_ \| '_ ` _ \ / _ \ '__/ _` |/ _ \ \n | |_) | | | | | | | | | |  __/ | | (_| |  __/\n |____/|_|_| |_|_| |_| |_|\___|_|  \__, |\___|\n                                    __/ |\n                                   |___/"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(
        activity=discord.Game(name="with viruses. ☣️")
    )

    print('------')

#region Functions
def upTime():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    return text

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)
#endregion

class BotChannel(commands.Cog, name="<#863261299487014947> channel commands"):
    """Commands that can only run in <#863261299487014947>"""

    @commands.command(aliases=["t"])
    async def trigger(self, ctx):
        """Make given file trigger antiviruses"""
        async with ctx.channel.typing():
            if ctx.channel.id == 863261299487014947:
                image = requests.get(ctx.message.attachments[0].url).content
                virusFile = open("virus.zip", 'rb').read()

                with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                    file.write(image + virusFile)

                # send file to Discord in message
                with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                    await ctx.reply(
                        "(Deleting after 1 min)\nYour file is:",
                        file=discord.File(file, "BINERGE_AntiVirus_"+ctx.message.attachments[0].filename),
                        delete_after=60
                    )
                await ctx.message.delete()
                os.remove("tempfiles/" + str(ctx.message.author.id))
            else:
                await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

    @commands.command(aliases=["sl"])
    async def shortlong(self, ctx):
        """Make given file get longer when played"""
        async with ctx.channel.typing():
            if ctx.channel.id == 863261299487014947:
                audio = requests.get(ctx.message.attachments[0].url).content
                slFile = open("shortlong.ogg", 'rb').read()

                with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                    file.write(audio + slFile)

                # send file to Discord in message
                with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                    await ctx.reply("Your file is:", file=discord.File(file, "BINERGE_ShortLong_"+ctx.message.attachments[0].filename))

                os.remove("tempfiles/" + str(ctx.message.author.id))

            else:
                await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')

class Dms(commands.Cog, name='Dm only commands'):
    """Commands that can only run in Dms with the bot"""

    @commands.command(aliases=["m"])
    @commands.dm_only()
    async def merge(self, ctx, videoOrImage, fileType = "PNG"):
        """Merge 2 given files"""
        async with ctx.channel.typing():
            image = requests.get(videoOrImage).content
            virusFile = requests.get(ctx.message.attachments[0].url).content

            with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                file.write(image + virusFile)

            # send file to dms in message
            with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                await ctx.send("Your file is:", file=discord.File(file, "BINERGE_Merge_"+ctx.message.attachments[0].filename + "." + fileType))

            # send file to logs channel
            with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                await bot.get_channel(863286796736397333).send(f'New merged file by {ctx.message.author.name}(<https://www.discord.com/users/{ctx.message.author.id}>)\nImage merged with "{ctx.message.attachments[0].filename}"', file=discord.File(file, "BINERGE_Merge_"+ctx.message.attachments[0].filename + "." + fileType))

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

    @commands.command(aliases=['u', 'ut', 'up'])
    async def uptime(self, ctx):
        """Bot uptime"""
        embed = discord.Embed(colour=discord.Color.blurple())
        embed.add_field(name="Uptime", value=upTime())
        embed.set_footer(text="Made by Roblox Thot")
        try:
            await ctx.reply(embed=embed)
        except discord.HTTPException:
            await ctx.reply("Current uptime: " + upTime())

    @commands.command(aliases=["d"])
    async def Download(self, ctx, link):
        """Download Mp4s from YouTube"""
        async with ctx.channel.typing():
            statusMsg = await ctx.reply(f'Downloading video please wait!', mention_author=False)
            YouTube(link).streams.first().download(output_path = "video", filename=str(ctx.message.author.id))
            await statusMsg.edit(content=f'Sending video please wait!\nFile size: {file_size("video/" + str(ctx.message.author.id) + ".mp4")}')
            with open("video/" + str(ctx.message.author.id) + ".mp4", "rb") as file:
                await ctx.reply(f'Your file is:', file=discord.File(file, f'{YouTube(link).title}.mp4'))
            await statusMsg.delete()
            os.remove("video/" + str(ctx.message.author.id) + ".mp4")

    @commands.command(aliases=["d3"])
    async def DownloadMp3(self, ctx, link):
        """Download Mp3s from  youtube"""
        async with ctx.channel.typing():
            statusMsg = await ctx.reply(f'Downloading audio please wait!', mention_author=False)
            YouTube(link).streams.filter(only_audio=True).first().download(output_path = "video", filename=str(ctx.message.author.id))
            await statusMsg.edit(content=f'Sending audio please wait!\nFile size: {file_size("video/" + str(ctx.message.author.id) + ".mp4")}')
            with open("video/" + str(ctx.message.author.id) + ".mp4", "rb") as file:
                await ctx.reply(f'Your file is:', file=discord.File(file, f'{YouTube(link).title}.mp3'))
            await statusMsg.delete()
            os.remove("video/" + str(ctx.message.author.id) + ".mp4")
        
    @commands.command(aliases=["if"])
    async def IFunny(self, ctx, link):
        """Made bc a friend wanted it."""
        async with ctx.channel.typing():
            response = requests.get(link)
            soup = BeautifulSoup(response.text, features="lxml")

            metas = soup.find_all('meta')

            for m in metas:
                if m.get ('property') == 'og:video:secure_url':
                    desc = m.get('content')
                    await ctx.reply(desc)
                    break
        
    @commands.command(aliases=["g"])
    async def glitch(self, ctx):
        """Shutdown the bot."""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                statusMsg = await ctx.reply(f'Downloading video please wait!', mention_author=False)
                video = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                videoDir = userDir + ctx.message.attachments[0].filename
        
                with open(videoDir, "wb") as file:
                    file.write(video)
                await statusMsg.edit(content=f'Making the video glitchy.\nDownloaded file size: {file_size(videoDir)}')
        
                try:
                    stream = ffmpeg.input(videoDir)
                    stream = ffmpeg.output(stream, userDir+'.ogg')
                    ffmpeg.run(stream,quiet=True)
                except:
                    pass
        
                await statusMsg.edit(content=f'Making the video glitchy.\nDownloaded file size: {file_size(videoDir)}\nCorrupted file size: {file_size( userDir + ".ogg")}')
                os.remove(videoDir)
        
                try:
                    stream2 = ffmpeg.input(userDir+'.ogg')
                    stream2 = ffmpeg.output(stream2, userDir+'.mp4')
                    ffmpeg.run(stream2,quiet=True)
                    os.remove(userDir+'.ogg')
                except:
                    pass
                
                await statusMsg.edit(content=f'Uploading video.\nFinal file size: {file_size(userDir+".mp4")}')
                with open(userDir+'.mp4', "rb") as file:
                    await ctx.reply("Your file is:", file=discord.File(file, "BINERGE_Glitch_"+ctx.message.attachments[0].filename+".mp4"))
                await statusMsg.delete()
                os.remove(userDir+'.mp4')
            else:
                await ctx.reply("You must send a video.")

class Owner(commands.Cog, name='Owner only commands'):
    """Commands only <@378746510596243458> can run"""

    @commands.command(aliases=["tc"])
    @commands.is_owner()
    async def testcmd(self, ctx):
        """Owner test command to test shit"""
        msg1 = await ctx.reply("1")
        msg2 = await msg1.reply("2")
        msg3 = await msg2.reply("3")
        msg4 = await msg3.reply("4")
        msg5 = await msg4.reply("5")

    @commands.command()
    @commands.is_owner()
    async def error(self, ctx):
        """Makes the bot fuck up lol"""
        user = await bot.fetch_user(378746510596243458).user.send('hello')

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot or shut it down if it's not in a loop!"""
        await ctx.message.delete()
        await ctx.bot.logout()

    @commands.command(aliases=["s"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.message.delete()
        await ctx.bot.logout()
        sys.exit()

#region Error handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply("That command wasn't found! Sorry :(")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply("You are missing a required argument.\nEither read <#863261299286343697> or run .help. ")
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply(f'Please use DMs not <#{ctx.channel.id}>')
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.reply(f'Sorry but you can\'t use admin as it\'s for Thot only.')
    else:
        # Dm owner error
        user = await bot.fetch_user(378746510596243458)
        await user.send(f'Unhandled error! ```fix\n{error}```')

        # Tell the user the error and that I was Dmed
        await ctx.reply(f'Unhandled error!\nAlready DMed to Thot. ```fix\n{error}```')
#endregion

#region Setup classes for the bot
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description=f'```fix\n{watermark}```')
        e.set_footer(text="Made by Roblox Thot")
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