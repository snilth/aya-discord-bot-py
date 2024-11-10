import discord
from discord.ext import commands
import yt_dlp



FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': 'True',
    'quiet': True
}

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.looping = False
        
    @commands.command()
    async def play(self, ctx, url):
        """ play a song from youtube url: -play <url> """
        
        if ctx.voice_client is None:
            await ctx.invoke(self.bot.get_command('join'))
            
        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, 
                                        download=False)
                
                title = info['title']
                stream_url = info['url']
                self.queue.append((stream_url, title))
                await ctx.send(f"Added to queue: **{title}**")
        
        if not ctx.voice_client.is_playing():
            await self.play_in_queue(ctx)
            
    async def play_in_queue(self, ctx):
        if self.queue:
            url, title = self.queue[0] if self.looping else self.queue.pop(0)
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                
            ctx.voice_client.play(source,
                                  after=lambda e: self.bot.loop.create_task(self.play_in_queue(ctx)))
            
            
            await ctx.send(f"Now playing: **{title}**")


    @commands.command()
    async def skip(self, ctx):
        """ 
        skip the playing song: -skip
        if the song stop, play_in_queue() will execute
        """
        
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped")
            
    @commands.command()
    async def loop(self, ctx):
        """ looping the current song: -loop """
        
        self.looping = not self.looping         # switching logic
                
        if self.looping:
            if ctx.voice_client and not ctx.voice_client.is_playing():
                await self.play_in_queue(ctx)
        
        status = "Enabled" if self.looping else "Disabled"
        await ctx.send(f"Looping status: **{status}**")
        
    @commands.command()
    async def pause(self, ctx):
        """ 
        pause the playing song: -pause
        """
        
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused")
    
    @commands.command()
    async def resume(self, ctx):
        """ 
        resume the paused song: -resume
        """
        
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed")
    
    

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
    