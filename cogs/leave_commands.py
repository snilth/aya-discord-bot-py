from discord.ext import commands

class LeaveCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def leave(self, ctx):
        author = ctx.author
        voice_channel = ctx.author.voice.channel
        
        print(f"user: {author}")
        print("command: -leave")
        print(f"voice channel: {voice_channel}")

        await ctx.voice_client.disconnect()
        await ctx.send(f"Aya leave voice channel: {voice_channel}")
        print(f"bot leave {voice_channel}")
        
        print("-----------------------------")
    
    
async def setup(bot):
    await bot.add_cog(LeaveCommands(bot))
        