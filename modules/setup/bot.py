import discord
from ..cogs.joke import JokeCog
from ..cogs.settings import SettingsCog
from ..cogs.role import RoleCog
from ..cogs.reply import ReplyCog
from ..cogs.ratio import RatioCog

bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot_intents.members = True
bot_intents.presences = True
bot_intents.guilds = True
bot_intents.reactions = True

bot = discord.Bot(command_prefix='$', intents=bot_intents)

bot.add_cog(JokeCog(bot))
bot.add_cog(SettingsCog(bot))
bot.add_cog(RoleCog(bot))
bot.add_cog(ReplyCog(bot))
bot.add_cog(RatioCog(bot))