from discord.ext import commands

class JoinCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def join(self, ctx):
        author = ctx.author
        voice_channel = ctx.author.voice.channel
        
        print(f"user: {author}")
        print(f"voice channel: {voice_channel}")

        await voice_channel.connect()
        await ctx.send(f"Aya join voice channel: {voice_channel}")
        print(f"bot join {voice_channel}")
        

async def setup(bot):
    await bot.add_cog(JoinCommands(bot))
    