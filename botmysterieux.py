# botmysterieux.py

import discord
from discord.ext import commands
import random
import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

INSULTS_REPLIES = ('Oh! Surveille ton langage!','Comment tu parles ???','Pas super bienveillant...','C\'est vraiment pas sympa.')

REPLIES = {
    'quoi':('FEUR!','FEUUUR!','FEUUUUUUUUUUUUUUUUUR!','fEuR','feur UwU'),
    'pourquoi':('POUR FEUR!','POUR FEUUUR!',' POUR FEUUUUUUUUUUUUUUUUUR!','pOuR fEuR','pour feur UwU'),
    'hein': ('Deux!','Deux, Trois, Quatre...','Deux LOLILOL!'),
    'mais': ('Juin',),
    'ah': ('B!','AAAAAAAAAAAH!','LPHABET!'),
    'oui': ('STITI!','stiti (trop marrant)','non.'),
    'non': ('si.','Bah si!','oui'),
    'ouais': ('STERN!', 'stern (western t\'as la ref?)'),
    'connard': INSULTS_REPLIES,
    'connasse': INSULTS_REPLIES,
    'con': INSULTS_REPLIES,
    'conne': INSULTS_REPLIES,
    'débile': INSULTS_REPLIES,
    'debile': INSULTS_REPLIES,
    'abruti': INSULTS_REPLIES,
    'abrutie': INSULTS_REPLIES,
    'salaud': INSULTS_REPLIES,
    'salope': INSULTS_REPLIES
}

def get_response(url,attr=""):
        try:
            if attr:
                return requests.get(url).json()[attr]
            else:
                return requests.get(url).json()
        except Exception as e:
            print(e)
            return dict()

class BotMysterieux(commands.Bot):
    def get_response(self,url,attr=""):
        try:
            if attr:
                return requests.get(url).json()[attr]
            else:
                return requests.get(url).json()
        except Exception as e:
            print(e)
            return dict()

    async def on_ready(self):
        activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
        await self.change_presence(status=discord.Status.dnd,activity=activity)
        print(f'{self.user} has connected to Discord!')
    
    async def on_message(self,message):
        if message.author != self.user:
            content = message.content.lower()
            for key in REPLIES.keys():
                    pattern = re.compile(rf"^.*\s*{key}\W*$")
                    if pattern.match(content):
                        random.seed()
                        chances = random.randint(0,1)
                        if chances == 0:
                            l = REPLIES[key]
                            index = random.randint(0,len(l)-1)
                            await message.reply(l[index])
                            break

# class BotMysterieux(discord.Client):
#     def get_response(self,url,attr=""):
#         try:
#             if attr:
#                 return requests.get(url).json()[attr]
#             else:
#                 return requests.get(url).json()
#         except Exception:
#             return dict()

#     async def on_ready(self):
#         activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
#         await self.change_presence(status=discord.Status.dnd,activity=activity)
#         print(f'{self.user} has connected to Discord!')
#         servers = []
#         for guild in self.guilds:
#             servers.append({'id':guild.id,'name':guild.name})
#         print(f'Servers: {servers}')
    
#     async def on_message(self,message):
#         if message.author != self.user:
#             content = message.content.lower()
#             if content.startswith("$blague"):
#                 joke = self.get_response("https://blague.xyz/api/joke/random","joke")
#                 if joke:
#                     embed=discord.Embed(title="blague.xyz", url="https://blague.xyz/", color=0xf7cd63)
#                     embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
#                     embed.add_field(name=joke["question"], value=joke["answer"], inline=False)
#                     await message.channel.send(embed=embed)
#                 else:
#                     await message.reply("Désolé, je ne peux pas faire de blague pour le moment.")
#             else:
#                 for key in REPLIES.keys():
#                     pattern = re.compile(rf"^.*\s*{key}\W*$")
#                     if pattern.match(content):
#                         random.seed()
#                         chances = random.randint(0,1)
#                         if chances == 0:
#                             l = REPLIES[key]
#                             index = random.randint(0,len(l)-1)
#                             await message.reply(l[index])
#                             break



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=',',intents=intents)
# bot = BotMysterieux(intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(name='un jeu mystérieux...',type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.dnd,activity=activity)
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        content = message.content.lower()
        for key in REPLIES.keys():
                pattern = re.compile(rf"^.*\s*{key}\W*$")
                if pattern.match(content):
                    random.seed()
                    chances = random.randint(0,1)
                    if chances == 0:
                        l = REPLIES[key]
                        index = random.randint(0,len(l)-1)
                        await message.reply(l[index])
                        break

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def blague(ctx):
    joke = get_response("https://blague.xyz/api/joke/random","joke")
    if joke:
        embed=discord.Embed(title="blague.xyz", url="https://blague.xyz/", color=0xf7cd63)
        embed.set_author(name="BotMysterieux", icon_url="https://cdn.discordapp.com/app-icons/1056222165835448390/da3b5cbbd76cc27cf7ce6541e6e99502.png?size=64")
        embed.add_field(name=joke["question"], value=joke["answer"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.reply('Désolé, je ne peux pas faire de blague pour le moment.')

print(f'{bot.commands}')

bot.run(TOKEN)
