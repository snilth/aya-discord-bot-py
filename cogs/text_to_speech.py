import discord
from discord.ext import commands
from helper.text_to_speech_helper import text_to_speech



class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def say(self, ctx, *, message):
        """ let the bot say in voice channel using gtts: -say <message>"""
        
        if ctx.voice_client is None:
            await ctx.invoke(self.bot.get_command('join'))
        
        await text_to_speech(ctx.voice_client, message)
    
            
    
async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))     
    