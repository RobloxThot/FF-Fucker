import discord,random,requests,os,sys,ffmpeg,pyfiglet
from discord.ext import commands
from bs4 import BeautifulSoup
from pytube import YouTube
from io import StringIO, BytesIO
from PIL import Image
import datetime, time

#Custom imports
from imports import YouTubeTools
from imports import videoInfo

start_time = time.time()
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents, case_insensitive=True)
watermark = "╭━━━┳━━━┳━━━╮\n┃╭━━┫╭━━┫╭━━╯\n┃╰━━┫╰━━┫╰━━╮\n┃╭━━┫╭━━┫╭━━╯\n┃┃╱╱┃┃╱╱┃┃\n╰╯╱╱╰╯╱╱╰╯"
fileWatermark = "\n\n /$$$$$$$$ /$$$$$$$$ /$$$$$$$$ \n| $$_____/| $$_____/| $$_____/ \n| $$      | $$      | $$ \n| $$$$$   | $$$$$   | $$$$$ \n| $$__/   | $$__/   | $$__/ \n| $$      | $$      | $$ \n| $$      | $$      | $$ \n|__/      |__/      |__/"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(
        activity=discord.Game(name="with FFmpeg. 🎵")
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
            return "%3.2f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def ThotOnly():
    def checkUser(ctx):
        return ctx.message.author.id == 378746510596243458
    return commands.check(checkUser)

def dashVarLength(var:str):
    """
    Adds dashes for however long a string is
    """
    dashOutput=""
    for y in range(len(var)):
        dashOutput+="-"
    return dashOutput

def getFileType(imageLink:str):
    """
    Gets the file type for a image link
    """
    contentType = requests.head(imageLink).headers["Content-Type"]

    return contentType.split("/",1)[1]
#endregion

class BotChannel(commands.Cog, name="<#863261299487014947> channel commands"):
    """Commands that can only run in <#863261299487014947>"""

    @commands.command(aliases=["t"])
    async def Trigger(self, ctx):
        """Make given file trigger antiviruses"""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                if ctx.channel.id == 863261299487014947:
                    image = requests.get(ctx.message.attachments[0].url).content
                    virusFile = open("virus.zip", 'rb').read()

                    with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                        file.write(image + virusFile)

                    # send file to Discord in message
                    with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                        await ctx.reply(
                            "(Deleting after 1 min)\nYour file is:",
                            file=discord.File(file, "FFF_AntiVirus_"+ctx.message.attachments[0].filename),
                            delete_after=60
                        )
                    await ctx.message.delete()
                    os.remove("tempfiles/" + str(ctx.message.author.id))
                else:
                    await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')
            else:
                await ctx.reply(f'You need to add a file.')

    @commands.command(aliases=["sl"])
    async def ShortLong(self, ctx):
        """Make given file get longer when played"""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                if ctx.channel.id == 863261299487014947:
                    audio = requests.get(ctx.message.attachments[0].url).content
                    slFile = open("shortlong.ogg", 'rb').read()

                    with open("tempfiles/" + str(ctx.message.author.id), "wb") as file:
                        file.write(audio + slFile)

                    # send file to Discord in message
                    with open("tempfiles/" + str(ctx.message.author.id), "rb") as file:
                        await ctx.reply("Your file is:", file=discord.File(file, "FFF_ShortLong_"+ctx.message.attachments[0].filename))

                    os.remove("tempfiles/" + str(ctx.message.author.id))

                else:
                    await ctx.reply(f'Please use <#863261299487014947> not <#{ctx.channel.id}>')
            else:
                await ctx.reply(f'You need to add a file.')

class Dms(commands.Cog, name='Dm only commands'):
    """Commands that can only run in Dms with the bot"""

    @commands.command(aliases=["m"])
    @commands.dm_only()
    async def merge(self, ctx, videoOrImage, fileType = "PNG"):
        """Merge 2 given files"""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                image = requests.get(videoOrImage).content
                virusFile = requests.get(ctx.message.attachments[0].url).content
    
                # send file to dms in message
                await ctx.send("Your file is:", file=discord.File(BytesIO(image + virusFile), "FFF_Merge_"+ctx.message.attachments[0].filename + "." + fileType))
    
                # send file to logs channel
                await bot.get_channel(863286796736397333).send(f'New merged file by {ctx.message.author.name}(<https://www.discord.com/users/{ctx.message.author.id}>)\nImage merged with "{ctx.message.attachments[0].filename}"', file=discord.File(BytesIO(image + virusFile), "FFF_Merge_"+ctx.message.attachments[0].filename + "." + fileType))
            else:
                await ctx.reply(f'You need to add a file.')

class Misc(commands.Cog, name='Miscellaneous commands'):
    """Some useful/useless commands"""

    @commands.command(aliases=['h'])
    async def Help(self, ctx, cmdToLookup = ""):
        """Lists commands dumbass"""
        if cmdToLookup != "":
            await ctx.send_help(cmdToLookup)
        else:
            await ctx.send_help()

    
    @commands.command(aliases=['info','ui'])
    @commands.guild_only()
    async def UserInfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=discord.Color.blurple(), description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.command(aliases=['u', 'ut', 'up'])
    async def UpTime(self, ctx):
        """Bot uptime"""
        embed = discord.Embed(colour=discord.Color.blurple())
        embed.add_field(name="Uptime", value=upTime())
        embed.set_footer(text="Made by Roblox Thot")
        try:
            await ctx.reply(embed=embed)
        except discord.HTTPException:
            await ctx.reply("Current uptime: " + upTime())

    @ThotOnly()
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

    @ThotOnly()
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

    @commands.command(aliases=["ascii","aa","art"])
    async def AsciiArt(self, ctx, Message):
        """
        Makes a lot of Ascii Art.
        """
        asciiArt=""
        async with ctx.channel.typing():
            for x in pyfiglet.FigletFont.getFonts():
                asciiArt += f'{x}\n\n{dashVarLength(x)}\n'
                asciiArt += pyfiglet.figlet_format(Message, font=x,)
            f = StringIO(asciiArt)
            await ctx.reply(f'Your file is:', file=discord.File(f, f'Ascii-{Message}.txt'))

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
    async def Glitch(self, ctx):
        """Make a video glitchy."""
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
                    await ctx.reply("Your file is:", file=discord.File(file, "FFF_Glitch_"+ctx.message.attachments[0].filename+".mp4"))
                await statusMsg.delete()
                os.remove(userDir+'.mp4')
            else:
                await ctx.reply("You must send a video.")
        
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.command(aliases=["mp3","con"])
    async def Convert(self, ctx, audioType = "mp3"):
        """Convert video/audio to mp3."""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                statusMsg = await ctx.reply(f'Downloading file please wait!', mention_author=False)
                video = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                videoDir = userDir + ctx.message.attachments[0].filename
        
                with open(videoDir, "wb") as file:
                    file.write(video)
                await statusMsg.edit(content=f'Converting to {audioType}.\nDownloaded file size: {file_size(videoDir)}')
        
                try:
                    stream = ffmpeg.input(videoDir)
                    stream = ffmpeg.output(stream, userDir+"."+audioType)
                    ffmpeg.run(stream,quiet=True)
                except:
                    pass

                os.remove(videoDir)
                
                await statusMsg.edit(content=f'Uploading file.\n{audioType.capitalize()} file size: {file_size(userDir+"."+audioType)}')
                with open(userDir+"."+audioType, "rb") as file:
                    await ctx.reply("Your file is:", file=discord.File(file, ""+ctx.message.attachments[0].filename+"."+audioType))
                await statusMsg.delete()
                os.remove(userDir+"."+audioType)
            else:
                await ctx.reply("You must send a file.")

    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.command(aliases=["l"])
    async def Loud(self, ctx, Volume = 1000):
        """Make video loud."""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                statusMsg = await ctx.reply(f'Downloading file please wait!', mention_author=False)
                video = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                videoDir = userDir + ctx.message.attachments[0].filename
        
                with open(videoDir, "wb") as file:
                    file.write(video)
                await statusMsg.edit(content=f'Boosting the audio.(<https://youtu.be/9EcjWd-O4jI>)\n(Can take up to 30 seconds.)\nDownloaded file size: {file_size(videoDir)}')

                stream = ffmpeg.input(videoDir)
                joined = ffmpeg.concat(stream,stream, v=1, a=1).node
                video = joined[0]
                audio = joined[1].filter('volume', Volume)
                output = ffmpeg.output(video,
                        audio,
                        userDir+".webm",
                        video_bitrate = 1000
                        )

                ffmpeg.run(output, quiet=True)
                await statusMsg.edit(content=f'Uploading audio.\nFile file size: {file_size(userDir+".webm")}')
                with open(userDir+".webm", "rb") as file:
                    await ctx.reply("Your file is:", file=discord.File(file, ""+ctx.message.attachments[0].filename+".webm"))
                await statusMsg.delete()
                os.remove(videoDir)
                os.remove(userDir+".webm")
        
            else:
                await ctx.reply("You must send a file.")

    @commands.command(aliases=["br"])
    async def BitRate(self, ctx, videoBitrate:int = 10000, audioBitrate:int = None):
        """Change video's audio and visual bitrate"""
        # Set audio if user did not set any number for it
        if audioBitrate == None:
            audioBitrate = videoBitrate

        async with ctx.channel.typing():
            if ctx.message.attachments:
                statusMsg = await ctx.reply(f'Downloading video please wait!', mention_author=False)
                video = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                videoDir = userDir + ctx.message.attachments[0].filename
        
                with open(videoDir, "wb") as file:
                    file.write(video)
                await statusMsg.edit(content=f'Changing bitrate.\nDownloaded file size: {file_size(videoDir)}')
        
                try:
                    stream = ffmpeg.input(videoDir)
                    stream = ffmpeg.output(stream, userDir+'.mp4',
                            video_bitrate = videoBitrate,
                            audio_bitrate = audioBitrate)
                    ffmpeg.run(stream, quiet=True,)
                except:
                    pass
                
                os.remove(videoDir)
                await statusMsg.edit(content=f'Uploading video.\nFinal file size: {file_size(userDir+".mp4")}')
                with open(userDir+'.mp4', "rb") as file:
                    await ctx.reply(f'Video Bitrate: {"{:,}".format(videoBitrate)}\nAudio Bitrate: {"{:,}".format(audioBitrate)}\nYour file is:', file=discord.File(file, "FFF_BitRate_"+ctx.message.attachments[0].filename+".mp4"))
                
                await statusMsg.delete()
                os.remove(userDir+'.mp4')
            else:
                await ctx.reply("You must send a video.")

    @commands.command(aliases=["Jpg"])
    @commands.guild_only()
    async def Jpeg(self, ctx, JpegQuality:int = 1):
        """
        Turns image into a crusty Jpg
        """
        async with ctx.channel.typing():
            if ctx.message.attachments:
                imageData = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                imageDir = userDir + ctx.message.attachments[0].filename

                with open(imageDir, "wb") as file:
                    file.write(imageData)
                originalImage = Image.open(imageDir)
                RgbImage = originalImage.convert('RGB')

                RgbImage.save(userDir+'.jpg', quality=0)
                os.remove(imageDir)
                with open(userDir+'.jpg', "rb") as file:
                    await ctx.reply(f'Your file is:', file=discord.File(file, "FFF_Jpg_"+ctx.message.attachments[0].filename+".jpg"))
                os.remove(userDir+'.jpg')
            else:
                ctx.reply("need image file")

class Owner(commands.Cog, name='Owner only commands'):
    """Commands only <@378746510596243458> can run"""

    @commands.command(aliases=["tc"])
    @ThotOnly()
    @commands.guild_only()
    async def testcmd(self, ctx, JpegQuality:int = 1):
        """Owner test command to test shit"""
        async with ctx.channel.typing():
            if ctx.message.attachments:
                imageData = requests.get(ctx.message.attachments[0].url).content
                userDir = "tempfiles/" + str(ctx.message.author.id)
                imageDir = userDir + ctx.message.attachments[0].filename

                with open(imageDir, "wb") as file:
                    file.write(imageData)
                originalImage = Image.open(imageDir)
                RgbImage = originalImage.convert('RGB')

                RgbImage.save(userDir+'.jpg', quality=0)
                os.remove(imageDir)
                with open(userDir+'.jpg', "rb") as file:
                    await ctx.reply(f'Your file is:', file=discord.File(file, "FFF_Jpg_"+ctx.message.attachments[0].filename+".jpg"))
                os.remove(userDir+'.jpg')
            else:
                ctx.reply("need image file")

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def error(self, ctx):
        """Makes the bot fuck up lol"""
        user = await bot.fetch_user(378746510596243458).user.send('hello')

    @commands.command(aliases=["r"])
    @commands.is_owner()
    @commands.guild_only()
    async def restart(self, ctx):
        """Restart the bot or shut it down if it's not in a loop!"""
        await ctx.message.delete()
        await ctx.bot.logout()

    @commands.command(aliases=["s"])
    @commands.is_owner()
    @commands.guild_only()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.message.delete()
        sys.exit()

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def status(self, ctx, statusType, *, statusMsg):
        """Chage status of bot."""
        await ctx.message.delete()
        if statusType.lower() == "playing":
            activityType = discord.Game(name=statusMsg)
        elif statusType.lower() == "streaming":
            activityType = discord.Streaming(name=statusMsg, platform="YouTube", url="https://www.youtube.com/watch?v=UTHLKHL_whs")
        elif statusType.lower() == "listening":
            activityType = discord.Activity(type=discord.ActivityType.listening, name=statusMsg)
        elif statusType.lower() == "watching":
            activityType = discord.Activity(type=discord.ActivityType.watching, name=statusMsg)
        else:
            activityType = discord.Activity(type=discord.ActivityType.listening, name="Cali Swag District - Teach Me How To Dougie")
        await bot.change_presence(
            activity=activityType
        )

    @commands.command(aliases=["yts"])
    @commands.is_owner()
    @commands.guild_only()
    async def YouTubeStatus(self, ctx, VideoIDOrLink):
        """Chage status of bot."""
        await ctx.message.delete()
        videoName = YouTubeTools.getTitle(VideoIDOrLink)

        #Check if its a ID or a link
        if "https://" in VideoIDOrLink:
            videoLink = VideoIDOrLink
        else:
            videoLink = "https://www.youtube.com/watch?v=%s" % VideoIDOrLink

        activityType = discord.Streaming(name=videoName, platform="YouTube", url=videoLink)
        await bot.change_presence(
            activity=activityType
        )

#region Error handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply("That command wasn't found! Sorry :(")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply("You are missing a required argument.\nEither read <#863261299286343697> or run .help. ")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply("One/any of your arguments is fucked.\nEither read <#863261299286343697> or run .help. ")
    elif isinstance(error, commands.errors.NotOwner):
        await ctx.reply(f'Sorry but you can\'t use admin as it\'s for Thot only.')
    elif isinstance(error, commands.errors.MemberNotFound):
        await ctx.reply(f'Could not find that fucker. (They need to be in this server)')
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.reply(f'Please use DMs not <#{ctx.channel.id}>')
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.reply(f'This cmd wont work in DMS.')
    elif isinstance(error, commands.MaxConcurrencyReached):
        await ctx.reply(f'Some one is using a hevy use CMD please wait.')
    else:
        if ctx.message.author.id != 378746510596243458:
            # Dm owner error
            user = await bot.fetch_user(378746510596243458)
            await user.send(f'Error from: <@{ctx.message.author.id}>\nUnhandled error! ```fix\n{error}```')

            # Tell the user the error and that I was Dmed
            await ctx.reply(f'Unhandled error!\nAlready DMed to Thot. ```fix\n{error}```')
        else:
            # Tell the owner the error and don't Dm
            await ctx.reply(f'Hey dumbass fix this error```fix\n{error}```')
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
