import discord
from discord.ext import commands
from ..setup.logger import LOGGER
from ..setup.data import get_response, is_feature_enabled

class JokeCog(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        
    @commands.slash_command(name='joke', description='Tells a joke')
    async def joke(self, ctx:discord.ApplicationContext):
        """Tells a joke."""
        author = ctx.author
        LOGGER.debug(f'{author} used /joke.')
        if is_feature_enabled('joke',guild_id=ctx.guild.id):
            joke = get_response("https://blague.xyz/api/joke/random",'joke')
            if joke:
                embed = discord.Embed(title="blague.xyz", url="https://blague.xyz/", color=0xf7cd63)
                embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
                embed.add_field(name=joke["question"], value=joke["answer"], inline=False)
                await ctx.send_response(embed=embed)
            else:
                await ctx.send_response('Désolé, je ne peux pas faire de blague pour le moment.')
        else:
            await ctx.send_response('Désolé, cette fonctionnalité n\'est pas activée sur ce serveur.')