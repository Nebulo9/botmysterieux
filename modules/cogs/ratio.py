import discord, random
from discord.ext import commands
from ..setup.logger import LOGGER
from ..setup.data import is_feature_enabled

class RatioCog(commands.Cog):
    
    RATIOS_MESSAGES = ('Ratio','Pas lu + Ratio', 'On s\'en fout','Vu et s\'en tape')
    
    def __init__(self,bot: discord.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.bot.user.id:
            guild_id = message.guild.id
            if is_feature_enabled('ratio',guild_id=guild_id):
                chance = random.randint(0,0)
                if chance == 0:
                    reply = random.choice(RatioCog.RATIOS_MESSAGES)
                    LOGGER.debug(f"Replying to message '{message.content}' from {message.author.name} in {message.guild.name} - {guild_id} with '{reply}'.")
                    await message.reply(reply)