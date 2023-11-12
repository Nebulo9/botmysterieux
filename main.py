import discord, os,json, sys
from discord.ext import commands
from dotenv import load_dotenv
from modules.setup.logger import LOGGER
from modules.setup.bot import bot
from modules.setup.data import DATA_DIR, create_guild_data

@bot.slash_command(name='help')
async def help(ctx:discord.ApplicationContext):
    """Shows the help message."""
    embed = discord.Embed(title='Help', description='List of available commands:',color=0xf7cd63)
    embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
    for command in bot.commands:
        embed.add_field(name=command.name,value=command.description,inline=False)
    await ctx.send_response(embed=embed,ephemeral=True)

@bot.slash_command(name='reload',description='Reloads the bot.')
@commands.is_owner()
async def reload(ctx:discord.ApplicationContext):
    """Reloads the bot."""
    command_name = 'reload'
    LOGGER.info(f'Executing command {command_name}.')
    await ctx.send_response('Reloading...',ephemeral=True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.listen()
async def on_guild_join(guild:discord.Guild):
    """Creates a new guild data file when the bot joins a guild."""
    guild_id = guild.id
    guuld_name = guild.name
    LOGGER.debug(f'Joined guild {guuld_name} - {guild_id}.')
    create_guild_data(guild_id)

@bot.listen()
async def on_guild_remove(guild:discord.Guild):
    """Deletes the guild data file when the bot leaves a guild."""
    guild_id = guild.id
    guuld_name = guild.name
    LOGGER.debug(f'Left guild {guuld_name} - {guild_id}.')
    path = os.path.join(DATA_DIR, f'{guild_id}.json')
    os.remove(path)
    LOGGER.debug(f'Deleted data file for guild {guild_id}.')
    
@bot.listen()
async def on_ready():
    activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.dnd,activity=activity)
    LOGGER.info('BotMysterieux is ready.')
    LOGGER.debug(f'Registered {len(bot.commands)} commands.')
    
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)