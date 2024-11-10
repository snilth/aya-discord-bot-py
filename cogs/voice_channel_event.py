import discord
from discord.ext import commands
from helper.text_to_speech_helper import text_to_speech


class VoiceChannelEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            return
        
        voice_client = member.guild.voice_client
        
        if before.channel is None and after.channel is not None:
            print(f"{member.name} joined {after.channel.name}")
            if voice_client and voice_client.channel == after.channel:
                await text_to_speech(voice_client, f"Someone joined.")
        
        elif before.channel is not None and after.channel is None:
            print(f"{member.name} left {before.channel.name}")
            if voice_client and voice_client.channel == before.channel:
                await text_to_speech(voice_client, f"Someone left.")
        
        elif before.channel != after.channel:
            print(f"{member.name} moved from {before.channel.name} to {after.channel.name}")
            if voice_client:
                if voice_client.channel == after.channel:
                    await text_to_speech(voice_client, f"Someone joined.")
                elif voice_client.channel == before.channel:
                    await text_to_speech(voice_client, f"Someone left.")    
        
async def setup(bot):
    await bot.add_cog(VoiceChannelEvent(bot))
    