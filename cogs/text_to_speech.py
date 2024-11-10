import discord
from discord.ext import commands
from gtts import gTTS
import asyncio
import os


FFMPEG_OPTIONS = {
    'options': '-vn',
    'executable': r'C:\ffmpeg\ffmpeg.exe'
}

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def say(self, ctx, *, message):
        """ let the bot say in voice channel using gtts: -say <message>"""
        
        if ctx.voice_client is None:
            await ctx.invoke(self.bot.get_command('join'))
        
        await self.text_to_speech(ctx, message)
    
    async def text_to_speech(self, ctx, message):
        try:
            speech = gTTS(text=message, lang="en", slow=False)
            speech.save("tts-audio.mp3")
            
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            
            source = discord.FFmpegPCMAudio("tts-audio.mp3", 
                                            **FFMPEG_OPTIONS)
            ctx.voice_client.play(source)

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove("tts-audio.mp3")
            
        except Exception as error:
            print(f"Error playing audio: {error}")
            
    
async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))     
    