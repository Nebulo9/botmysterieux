import discord, random, re
from discord.ext import commands
from ..setup.logger import LOGGER
from ..setup.data import is_feature_enabled

class ReplyCog(commands.Cog):
    INSULTS_REPLIES = ('Oh! Surveille ton langage!','Comment tu parles ???','Pas super bienveillant...','C\'est vraiment pas sympa.')
    
    FUNNY_REPLIES = {
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
}
    
    def __init__(self,bot: discord.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.bot.user.id:
            guild_id = message.guild.id
            if is_feature_enabled('reply',guild_id=guild_id):
                random.seed()
                content = message.content.lower()
                # Filtering the dict to only keep entries which key is a substring of the message content
                replies = {key: value for key, value in self.FUNNY_REPLIES.items() if re.compile(rf"^.*\s*{key}\W*$").match(content)}
                
                if replies:
                    # Getting a random value from the dict's entries
                    keys = list(replies.keys())
                    random_key = random.choice(keys)
                    matching_values = replies[random_key]
                    matching_values = list(replies.values())[0]
                    chance = random.randint(0,2)
                    if chance == 0:
                        if len(matching_values) > 1:
                            reply = random.choice(matching_values)
                        else:
                            reply = matching_values[0]
                        LOGGER.debug(f"Replying to message '{content}' from {message.author.name} in {message.guild.name} - {guild_id} with '{reply}'.")
                        await message.reply(reply)
                        
                