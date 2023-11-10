import discord
from discord.ext import commands
from discord import option
from ..setup.logger import LOGGER
from ..setup.data import get_guild_data, is_feature_enabled, save_guild_data

class RoleCog(commands.Cog):
    def __init__(self,bot:discord.Bot) -> None:
        self.bot = bot
        
    @commands.slash_command(name='addrole', description='Creates a role that users can add to themselves.')
    @option(name='role_name',description='the role to add',required=True)
    @option(name='emoji',description='the emoji to use',required=True)
    @commands.has_permissions(administrator=True)
    async def addrole(self, ctx:discord.ApplicationContext, role_name:str, emoji:str):
        """Creates a role that users can add to themselves."""
        author = ctx.author
        guild = ctx.guild
        guild_id = guild.id
        guild_data = get_guild_data(guild_id)
        LOGGER.debug(f'{author} used /addrole.')
        if is_feature_enabled('role',data=guild_data):
            guild_roles = guild.roles
            guild_roles_names = [role.name.lower() for role in guild_roles]
            if role_name.lower() not in guild_roles_names:
                c = await guild.create_role(name=role_name,color=discord.Color.random())
                if 'roles' not in guild_data['features']['role'].keys():
                    guild_data['features']['role']['roles'] = []
                guild_data['features']['role']['roles'].append({'id':c.id,'name':role_name,'emoji':emoji,})
                save_guild_data(guild_id,guild_data)
                await ctx.send_response(f'Role {role_name} created.',ephemeral=True)
            else:
                await ctx.send_response(f'Role {role_name} already exists.',ephemeral=True)
        else:
            await ctx.send_response('This feature is not enabled in this server.',ephemeral=True)
    
    @commands.slash_command(name='removerole', description='Removes a role that users can add to themselves **if it was not added with /addrole.**')
    @option(name='role_name',description='the role to remove',required=True)
    @commands.has_permissions(administrator=True)
    async def removerole(self,ctx:discord.ApplicationContext,role_name:str):
        author = ctx.author
        guild = ctx.guild
        guild_id = guild.id
        guild_data = get_guild_data(guild_id)
        LOGGER.debug(f'{author} used /removerole.')
        if is_feature_enabled('role',data=guild_data):
            guild_roles = guild.roles
            guild_roles_names = [role.name.lower() for role in guild_roles]
            if role_name.lower() in guild_roles_names:
                target_roles = [role for role in guild_roles if role.name.lower() == role_name.lower()]
                target_role_data = [role for role in guild_data['features']['role']['roles'] if role['name'].lower() == role_name.lower()][0]
                for target_role in target_roles:
                    if target_role.id == target_role_data['id']:
                        await target_role.delete()
                        guild_data['features']['role']['roles'] = [role for role in guild_data['features']['role']['roles'] if role['name'].lower() != role_name.lower()]
                        save_guild_data(guild_id,guild_data)
                        await ctx.send_response(f'Role {role_name} deleted.',ephemeral=True)
            else:
                await ctx.send_response(f'Role {role_name} does not exist.',ephemeral=True)
        else:
            await ctx.send_response('This feature is not enabled in this server.',ephemeral=True)
            
    @commands.slash_command(name='rolesmessage',description='Sends a message to the selected channel with the roles to add to yourself.')
    @option(name='action',description='generates the message',required=True,choices=['generate','update','delete'])
    @option(name='channel',description='the channel to send the message to',required=True)
    @option(name='custom_message',description='the message to send',required=False)
    @commands.has_permissions(administrator=True)
    async def rolesmessage(self,ctx:discord.ApplicationContext,action:str,channel:discord.TextChannel,custom_message:str=None):
        """Send a message to the selected channel with the roles that users can add to themselves by reacting to the realted emoji."""
        author = ctx.author
        guild = ctx.guild
        guild_id = guild.id
        guild_data = get_guild_data(guild_id)
        LOGGER.debug(f'{author} used /rolesmessage.')
        if action == 'generate':
            if is_feature_enabled('role',data=guild_data):
                if custom_message:
                    embed = discord.Embed(title='Roles',description=custom_message,color=0xf7cd63)
                else:
                    embed = discord.Embed(title='Roles',description='React to this message to add a role to yourself.',color=0xf7cd63)
                embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
                for role in guild_data['features']['role']['roles']:
                    role_name = role['name']
                    emoji = role['emoji']
                    embed.add_field(name=" ", value=f"{emoji}: {role_name}", inline=False)
                roles_message = await channel.send(embed=embed)
                for role in guild_data['features']['role']['roles']:
                    await roles_message.add_reaction(role['emoji'])
                roles_message_id = roles_message.id
                guild_data['features']['role']['message_id'] = roles_message_id
                save_guild_data(guild_id,guild_data)
                await ctx.send_response(f'Message sent to {channel.mention}.',ephemeral=True)
            else:
                await ctx.send_response('This feature is not enabled in this server.',ehpemeral=True)    
        elif action == 'update':
            if is_feature_enabled('role',data=guild_data):
                if 'message_id' in guild_data['features']['role'].keys():
                    roles_message_id = guild_data['features']['role']['message_id']
                    roles_message = await channel.fetch_message(roles_message_id)
                    if custom_message:
                        embed = discord.Embed(title='Roles',description=custom_message,color=0xf7cd63)
                    else:
                        embed = discord.Embed(title='Roles',description='React to this message to add a role to yourself.',color=0xf7cd63)
                    embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
                    for role in guild_data['features']['role']['roles']:
                        role_name = role['name']
                        emoji = role['emoji']
                        embed.add_field(name=" ", value=f"{emoji}: {role_name}", inline=False)
                    await roles_message.edit(embed=embed)
                    for role in guild_data['features']['role']['roles']:
                        await roles_message.add_reaction(role['emoji'])
                    await ctx.send_response(f'Message updated in {channel.mention}.',ephemeral=True)
                else:
                    await ctx.send_response('No message to update.',ephemeral=True)
            else:
                await ctx.send_response('This feature is not enabled in this server.',ephemeral=True)
        elif action == 'delete':
            if is_feature_enabled('role',data=guild_data):
                if 'message_id' in guild_data['features']['role'].keys():
                    roles_message_id = guild_data['features']['role']['message_id']
                    roles_message = await channel.fetch_message(roles_message_id)
                    await roles_message.delete()
                    del guild_data['features']['role']['message_id']
                    save_guild_data(guild_id,guild_data)
                    await ctx.send_response(f'Message deleted from {channel.mention}.',ephemeral=True)
                else:
                    await ctx.send_response('No message to delete.',ephemeral=True)
            else:
                await ctx.send_response('This feature is not enabled in this server.',ephemeral=True)
        else:
            await ctx.send_response('Invalid action.',ephemeral=True)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload:discord.RawReactionActionEvent):
        user = self.bot.get_user(payload.user_id)
        if user.id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            guild_id = guild.id
            guild_data = get_guild_data(guild_id)
            if is_feature_enabled('role',data=guild_data):
                if 'message_id' in guild_data['features']['role'].keys():
                    roles_message_id = guild_data['features']['role']['message_id']
                    if payload.message_id == roles_message_id:
                        for role in guild_data['features']['role']['roles']:
                            if str(payload.emoji) == role['emoji']:
                                role_id = role['id']
                                target_role = guild.get_role(role_id)
                                await user.add_roles(target_role)
                                LOGGER.debug(f'{user} has now role {target_role.name}.')
                                break
                            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload:discord.RawReactionActionEvent):
        user = self.bot.get_user(payload.user_id)
        if user.id != self.bot.user.id:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            guild_id = guild.id
            guild_data = get_guild_data(guild_id)
            if is_feature_enabled('role',data=guild_data):
                if 'message_id' in guild_data['features']['role'].keys():
                    roles_message_id = guild_data['features']['role']['message_id']
                    if payload.message_id == roles_message_id:
                        for role in guild_data['features']['role']['roles']:
                            if str(payload.emoji) == role['emoji']:
                                role_id = role['id']
                                target_role = guild.get_role(role_id)
                                await user.remove_roles(target_role)
                                LOGGER.debug(f'{user} no longer has role {target_role.name}.')
                                break
    