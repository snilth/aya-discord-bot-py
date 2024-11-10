import discord
from discord.ext import commands
from helper.text_to_speech_helper import text_to_speech
from helper.nicknames import load_nicknames


nicknames = load_nicknames()

class VoiceChannelEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nicknames = nicknames
        
    def get_user_nickname(self, member):
        user_id = str(member.id)
        if user_id in self.nicknames:
            return self.nicknames[user_id]
        return member.display_name
        
    # track voice channel event and trigger tts
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            return
        
        voice_client = member.guild.voice_client
        user_nickname = self.get_user_nickname(member)
        
        # check if user joined voice channel
        if before.channel is None and after.channel is not None:
            print(f"{member.name} joined {after.channel.name}")
            if voice_client and voice_client.channel == after.channel:
                await text_to_speech(voice_client, f"{user_nickname} joined.")
        
        # check if user left voice channel
        elif before.channel is not None and after.channel is None:
            print(f"{member.name} left {before.channel.name}")
            if voice_client and voice_client.channel == before.channel:
                await text_to_speech(voice_client, f"{user_nickname} left.")
        
        # check if user move between voice channel
        elif before.channel != after.channel:
            print(f"{member.name} moved from {before.channel.name} to {after.channel.name}")
            if voice_client:
                if voice_client.channel == after.channel:
                    await text_to_speech(voice_client, f"{user_nickname} move in.")
                elif voice_client.channel == before.channel:
                    await text_to_speech(voice_client, f"{user_nickname} move out.")    
        
async def setup(bot):
    await bot.add_cog(VoiceChannelEvent(bot))
    