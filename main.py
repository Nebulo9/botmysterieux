import discord, os,json
from dotenv import load_dotenv
from modules.setup.logger import LOGGER
from modules.setup.bot import bot
from modules.setup.data import DATA_DIR, save_guild_data, get_guild_data

@bot.slash_command(name='help')
async def help(ctx:discord.ApplicationContext):
    """Shows the help message."""
    embed = discord.Embed(title='Help', description='List of available commands:',color=0xf7cd63)
    embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
    for command in bot.commands:
        embed.add_field(name=command.name,value=command.description,inline=False)
    await ctx.send_response(embed=embed,ephemeral=True)

@bot.listen()
async def on_ready():
    activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.dnd,activity=activity)
    LOGGER.info('BotMysterieux is ready.')
    LOGGER.debug(f'Registered {len(bot.commands)} commands.')
    for guild in bot.guilds:
        guild_id = guild.id
        path = os.path.join(DATA_DIR, f'{guild_id}.json')
        if not os.path.exists(path):
            with open(path,'w') as f:
                json.dump({'features':{'joke':{'enabled': False},'role':{'enabled': False}, 'reply': {'enabled': False}, 'ratio': {'enabled': False}}}, f, indent=2)
                LOGGER.debug(f'Created data file for guild {guild.name} - {guild_id}.')
    
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)