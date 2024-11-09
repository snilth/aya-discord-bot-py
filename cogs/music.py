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
                await ctx.send("----------------------------")
        
        if not ctx.voice_client.is_playing():
            await self.play_in_queue(ctx)
            
    async def play_in_queue(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source,
                                  after=lambda e: self.bot.loop.create_task(self.play_in_queue(ctx)))
            
            await ctx.send(f"Now playing: **{title}**")

        
    @commands.command()
    async def pause(self, ctx):
        pass
    
    @commands.command()
    async def resume(self, ctx):
        pass
    
    @commands.command()
    async def skip(self, ctx):
        pass
    
    @commands.command()
    async def loop(self, ctx):
        pass
    

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
    