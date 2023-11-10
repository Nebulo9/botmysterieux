import discord
from discord.ext import commands
from discord import option
from ..setup.logger import LOGGER
from ..setup.data import get_guild_data, save_guild_data

class SettingsCog(commands.Cog):
    
    FEATURES = ['joke','reply','role', 'ratio']
    
    def __init__(self,bot) -> None:
        self.bot = bot

    @commands.slash_command(name='settings', description='Shows the settings')
    @option(name='action',description='enable, disable or see the value',required=True,choices=['enable','disable','value'])
    @option(name='feature',description='the feature to change',required=True,choices=(FEATURES + ['all']))
    async def settings(self, ctx:discord.ApplicationContext, action:str, feature:str):
        author = ctx.author
        guild_id = ctx.guild.id
        guild_data = get_guild_data(guild_id)
        LOGGER.debug(f'{author} used /settings {action} {feature}.')
        if action in ['enable','disable']:
            val = True if action == 'enable' else False
            LOGGER.debug(f'Setting {feature} to {val}.')
            if feature == 'all':
                for feature in self.FEATURES:
                    guild_data['features'][feature]['enabled'] = val
                await ctx.send_response(f'All features set to {val}',ephemeral=True)
            else:
                guild_data['features'][feature]['enabled'] = val
            save_guild_data(guild_id,guild_data)
            await ctx.send_response(f'{feature} set to {val}',ephemeral=True)
        elif action == 'value':
            if feature == 'all':
                s = ''
                for feature in self.FEATURES:
                    feature_value = guild_data['features'][feature]['enabled']
                    s += f'- {feature} is {feature_value}\n'
                await ctx.send_response(s,ephemeral=True)
            else:
                feature_value = guild_data['features'][feature]['enabled']
                await ctx.send_response(f'{feature} is {feature_value}',ephemeral=True)