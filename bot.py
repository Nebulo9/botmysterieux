# BotMysterieux

import os, random, re, discord, requests, json
from util import Mapping
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

INSULTS_REPLIES = ('Oh! Surveille ton langage!','Comment tu parles ???','Pas super bienveillant...','C\'est vraiment pas sympa.')

REPLIES = Mapping({
    'quoi':('FEUR!','FEUUUUUUUUUUUUUUUUUR!','fEuR','feur UwU'),
    'pourquoi':('POUR FEUR!','POUR FEUUUR!',' POUR FEUUUUUUUUUUUUUUUUUR!','pOuR fEuR','pour feur UwU'),
    'hein': ('Deux!','Deux, Trois, Quatre...','Stituteur'),
    'deux': ('années', 'ans d\'études'),
    'mais': ('Juin','On'),
    'ou': ('Zbékistan!',),
    'où': ('Zbékistan!',),
    'comment': ('Taire!',),
    'quand': ('Tique!',),
    'qui': ('Che Lorraine!',),
    'ah': ('B!','AAAAAAAAAAAH!','LPHABET!'),
    'oui': ('STITI!','stiti (trop marrant)','non.'),
    'non': ('si.','Bah si!'),
    'ouais': ('STERN!', 'stern (western t\'as la ref?)'),
    'bon': ('Jour','Soir','Ne nuit'),
    'connard': INSULTS_REPLIES,
    'connasse': INSULTS_REPLIES,
    'con': INSULTS_REPLIES,
    'conne': INSULTS_REPLIES,
    'débile': INSULTS_REPLIES,
    'debile': INSULTS_REPLIES,
    'abruti': INSULTS_REPLIES,
    'abrutie': INSULTS_REPLIES,
    'salaud': INSULTS_REPLIES,
    'salope': INSULTS_REPLIES,
    'salopard': INSULTS_REPLIES,
    'enculé': INSULTS_REPLIES,
    'enculée': INSULTS_REPLIES,
    'encule': INSULTS_REPLIES,
    'enculee': INSULTS_REPLIES
})

RATIOS_MESSAGES = ('Ratio','Pas lu + Ratio', 'On s\'en fout','Vu et s\'en tape')

GUILDS_SETTINGS = dict()

def get_response(url:str,attr=""):
    try:
        if attr:
            return requests.get(url).json()[attr]
        else:
            return requests.get(url).json()
    except Exception as e:
        print(e)
        return dict()

def is_feature_enabled(guild_id:int,feature:str):
    return GUILDS_SETTINGS[str(guild_id)]["features"][feature]["enabled"]

def reload_settings():
    directory = "guilds/"
    for guild_id in GUILDS_SETTINGS.keys():
        file = os.path.join(directory,guild_id + ".json")
        with open(file,'w') as outstream:
            outstream.write(json.dumps(GUILDS_SETTINGS[guild_id]))
        settings = None
        with open(file) as instream:
            settings = json.load(instream)
        GUILDS_SETTINGS[guild_id] = settings

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix='$',intents=intents)

@bot.tree.command(name="help")
async def help_command(interaction:discord.Interaction):
    embed = discord.Embed(title='Help', description='List of available commands:',color=0xf7cd63)
    embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
    for command in bot.tree.get_commands():
        embed.add_field(name=command.name,value=command.description,inline=False)
    await interaction.response.send_message(embed=embed,ephemeral=True)

@bot.tree.command(name="joke",description="Sends a joke")
async def joke(interaction: discord.Interaction):
    joke = get_response("https://blague.xyz/api/joke/random","joke")
    if joke:
        embed = discord.Embed(title="blague.xyz", url="https://blague.xyz/", color=0xf7cd63)
        embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
        embed.add_field(name=joke["question"], value=joke["answer"], inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('Désolé, je ne peux pas faire de blague pour le moment.')

@bot.tree.command(name="settings",description="Enable, disable or view features.")
@app_commands.describe(action="what action",feature="what feature")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.choices(action=[
    discord.app_commands.Choice(name="enable",value=1),
    discord.app_commands.Choice(name="disable",value=0),
    discord.app_commands.Choice(name="value",value=-1)
],feature=[
    discord.app_commands.Choice(name="ratio",value=1),
    discord.app_commands.Choice(name="reply",value=2),
    discord.app_commands.Choice(name="cities",value=3),
    discord.app_commands.Choice(name="all",value=-1)
])
async def settings(interaction:discord.Interaction,action:discord.app_commands.Choice[int],feature:discord.app_commands.Choice[int]):
    if action.value >= 0:
        val = bool(action.value)
        GUILDS_SETTINGS[str(interaction.guild_id)]["features"][feature.name] = val
        reload_settings()
        await interaction.response.send_message(f'{feature.name} set to {val}',ephemeral=True)
    elif action.value == -1:
        if feature.value >= 0:
            val = GUILDS_SETTINGS[str(interaction.guild_id)]["features"][feature.name]
            await interaction.response.send_message(f'Value of `{feature.name}`: `{val}`',ephemeral=True)
        elif feature.value == -1:
            vals = GUILDS_SETTINGS[str(interaction.guild_id)]["features"]
            s = ""
            for key in vals.keys():
                s += f"Value of `{key}`: `{vals[key]}`\n"
            await interaction.response.send_message(s,ephemeral=True)

#commande pour attribuer rôle avec réaction
#city add <nom> <emoji>
@bot.tree.command(name="addcity",description="Adds a city-role.")
@app_commands.describe(city="which city",emoji="which emoji")
@app_commands.checks.has_permissions(administrator=True)
async def addcity(interaction:discord.Interaction,city:str,emoji:str):
    guild = interaction.guild
    if is_feature_enabled(guild.id,"cities"):
        roles_names = [r.name.lower() for r in guild.roles]
        if city.lower() not in roles_names:
            await guild.create_role(name=city,colour=discord.Color.random(),permissions=guild.roles[0].permissions)
            role_id = [r for r in guild.roles if r.name.lower() == city.lower()][0].id
            GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"].append({"id": role_id,"emoji": emoji})
            reload_settings()
            await interaction.response.send_message(f"Successfully added **{city}**",ephemeral=True)
        else:
            await interaction.response.send_message(f"There is already a role named **{city}**",ephemeral=True)
    else:
        await interaction.response.send_message("You must enable the feature named **cities**",ephemeral=True)

@bot.tree.command(name="removecity",description="Removes a city-role.")
@app_commands.describe(city="which city")
@app_commands.checks.has_permissions(administrator=True)
async def removecity(interaction:discord.Interaction,city:str):
    guild = interaction.guild
    if is_feature_enabled(guild.id,"cities"):
        roles = [r for r in guild.roles if r.name.lower() == city.lower()]
        if roles:
            role = roles[0]
            role_id = role.id
            await role.delete()
            GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"] = [r for r in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"] if r["id"] != role_id]
            reload_settings()
            await interaction.response.send_message(f"**{city}** has been removed",ephemeral=True)
        else:
            await interaction.response.send_message(f"There is no city-role named **{city}**.",ephemeral=True)
    else:
        await interaction.response.send_message("You must enable the feature named **cities**",ephemeral=True)

@bot.tree.command(name="rolesmessage",description="generates, updates or removes the roles message")
@app_commands.describe(action="what to do")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.choices(action=[
    discord.app_commands.Choice(name="generate",value=1),
    discord.app_commands.Choice(name="update",value=0),
    discord.app_commands.Choice(name="remove",value=-1)
])
async def rolesmessage(interaction:discord.Interaction,action:discord.app_commands.Choice[int]):
    guild = interaction.guild
    if action.value >= 0:
        if GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"] == None and action.value == 1:
            embed = discord.Embed(title='Rôles-villes', description='Clique sur la réaction correspondant à ta ville pour obtenir le rôle',color=0xf7cd63)
            embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
            for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                role_name = interaction.guild.get_role(role["id"])
                emoji = role["emoji"]
                embed.add_field(name=" ", value=f"{emoji}: {role_name}", inline=False)
            await interaction.response.send_message(embed=embed)
            message = await interaction.original_response()
            for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                await message.add_reaction(role["emoji"])
            message_id = message.id
            channel_id = message.channel.id
            GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"] = {"channel_id":channel_id,"message_id":message_id}
            reload_settings()
        else:
            message = guild.get_channel(GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["channel_id"]).get_partial_message(GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["message_id"])
            embed = discord.Embed(title='Rôles-villes', description='Clique sur la réaction correspondant à ta ville pour obtenir le rôle',color=0xf7cd63)
            embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
            for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                role_name = interaction.guild.get_role(role["id"])
                emoji = role["emoji"]
                embed.add_field(name=" ", value=f"{emoji}: {role_name}", inline=False)
            await message.edit(embed=embed)
            for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                await message.add_reaction(role["emoji"])
            await interaction.response.send_message("Message successfully updated.",ephemeral=True)
    else:
        if GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"] != None
            message = guild.get_channel(GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["channel_id"]).get_partial_message(GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["message_id"])
            await message.delete()
            GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"] = None
            reload_settings()
            await interaction.response.send_message("Message successfully removed.",ephemeral=True)
        else:
            await interaction.response.send_message("No message has been generated.",ephemeral=True)
            
@bot.event
async def on_reaction_add(reaction,user):
    if user != bot.user:
        guild = reaction.message.channel.guild
        if is_feature_enabled(guild.id,"cities"):
            message = reaction.message
            channel = message.channel
            if message.id == GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["message_id"] and channel.id == GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["channel_id"]:
                for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                    if reaction.emoji == role["emoji"]:
                        await user.add_roles(guild.get_role(role["id"]))
                        
@bot.event
async def on_reaction_remove(reaction,user):
    if user != bot.user:
        guild = reaction.message.channel.guild
        if is_feature_enabled(guild.id,"cities"):
            message = reaction.message
            channel = message.channel
            if message.id == GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["message_id"] and channel.id == GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["role_message"]["channel_id"]:
                for role in GUILDS_SETTINGS[str(guild.id)]["features"]["cities"]["roles"]:
                    if reaction.emoji == role["emoji"]:
                        await user.remove_roles(guild.get_role(role["id"]))
#commande pour générer le message
#récupérer le message contenant les réactions
#id: 1027188353428365404


@bot.event
async def on_ready():
    activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.dnd,activity=activity)
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        path = "guilds/" + str(guild.id) + ".json"
        if os.path.exists(path):
            with open(path) as instream:
                GUILDS_SETTINGS[str(guild.id)] = json.loads(instream.read())
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s).')
    except Exception as e:
        print(e)

@bot.event
async def on_message(message:discord.Message):
    if message.author != bot.user:
        guild_id = message.guild.id
        if is_feature_enabled(guild_id,'ratio'):
            random.seed()
            ratio_chance = random.randint(0,99)
            if ratio_chance == 0:
                choice = random.choice(RATIOS_MESSAGES)
                ratio_message = await message.reply(choice)
                await ratio_message.add_reaction('\N{THUMBS UP SIGN}')
        if is_feature_enabled(guild_id,'reply'):
            content = message.content.lower()
            replies = REPLIES.filter(lambda key: re.compile(rf"^.*\s*{key}\W*$").match(content)).choice()
            if replies:
                random.seed()
                chances = random.randint(0,2)
                if chances == 0:
                    await message.reply(random.choice(replies))

@bot.event
async def on_guild_join(guild:discord.Guild):
    path = "guilds/" + str(guild.id) + ".json"
    settings = {
        'id': guild.id,
        'features': {
            'ratio': {
                'enabled': True
            },
            'reply': {
                'enabled': True
            },
            'cities': {
                "enabled": False, "roles":[],"role_message": None
            }
        }
    }
    with open(path,'x') as outstream:
        json_settings = json.dumps(settings)
        outstream.write(json_settings)

@bot.event
async def on_guild_remove(guild:discord.Guild):
    path = "guilds/" + str(guild.id) + ".json"
    if os.path.exists(path):
        os.remove(path)
        GUILDS_SETTINGS.delete(str(guild.id))

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)