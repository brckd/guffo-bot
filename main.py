import disnake as discord
from disnake.ext import commands
import utils

import time

from replit import db
import os

import logging
import sys

# Reset
if 'prefix' not in db:
    db['prefix'] = {}

# Configs
# db['dfprefix'] = '/'
# db['color'] = discord.Colour(0x886bd5).value
db['test_guilds'] = [840977388385075210, 961956901329989662]
db['activity'] = 'Guffo Simulator: The Sequel'
db['owners'] = [
    691572882148425809,  # Bricked
    820948920112119839,  # Guffo
    859485709043105804,  # Furbuffo
    801462631793033239,  # Gnegni
    774365314779054160,  # Minify
    888390298999345172,  # XXXL
    830071104088440875,  # Telcaum
    724887486366613554,  # Gab157
    774297041898700810  # Zordan
]

bot = commands.Bot(
    command_prefix=lambda bot, msg: commands.when_mentioned_or(
        db['prefix'][str(msg.guild.id)]
        if (str(msg.guild.id) in db['prefix']) else db['dfprefix'])(bot, msg),
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions.none(),
    intents=discord.Intents.all(),
    owner_ids=set(db['owners']) if 'owners' in db else {691572882148425809},
    help_command=None,
    test_guilds=db['test_guilds'])

log_level = logging.INFO
log_format = logging.Formatter('[%(levelname)s] %(message)s')

bot.log = logging.getLogger(__name__)
bot.log.setLevel(log_level)
bot.handler = logging.StreamHandler(sys.stdout)
bot.handler.setLevel(log_level)
bot.handler.setFormatter(log_format)
bot.log.addHandler(bot.handler)

bot.log.info('Starting...')


@bot.listen()
async def on_connect():
    bot.log.info('Connecting...')
    await bot.change_presence(activity=discord.Game(name='connecting...'))


@bot.listen()
async def on_ready():
    bot.log.info('Ready!')
    await bot.change_presence(activity=discord.Game(name=db['activity']))
    bot.launch_time = time.time()


@bot.slash_command()
@commands.is_owner()
async def cogs(inter):
    '''
  Lists currently available Cogs

  Indicators
  ----------
  ✅: Loaded Cog
  ❌: Unloaded Cog
  '''
    await inter.send(embed=utils.Embed(
        inter, '\n'.join([
            f'✅ {filename[:-3]}' if filename[:-3].title() in bot.cogs.keys()
            else f'❌ {filename[:-3]}' for filename in os.listdir('./cogs')
            if filename.endswith('.py')
        ])),
                     ephemeral=True)


@bot.slash_command()
@commands.is_owner()
async def load(
    inter,
    cogs: str = commands.Param(choices=list(
        filter(lambda cog: cog in bot.cogs.values(), utils.cog_files())))):
    '''
  Load Cogs

  Parameters
  ----------
  cogs: Select a Cog to load
  '''

    if isinstance(cogs, str):
        cogs = [cogs]
    msg = ''
    for cog in cogs:
        cog = cog.lower()
        bot.load_extension(f'cogs.{cog}')
        msg += f'> **{cog.title()}**\n'
    db['cogs'] = tuple(bot.cogs.keys())
    await inter.send(embed=utils.Embed(inter, msg), ephemeral=True)


@bot.slash_command()
@commands.is_owner()
async def unload(
    inter,
    cogs: str = commands.Param(choices=list(
        filter(lambda cog: cog not in bot.cogs.values(), utils.cog_files())))):
    '''
  Unload Cogs

  Parameters
  ----------
  cogs: Select a Cog to unload
  '''

    if isinstance(cogs, str):
        cogs = [cogs]
    msg = ''
    for cog in cogs:
        cog = cog.lower()
        bot.unload_extension(f'cogs.{cog}')
        msg += f'> **{cog.title()}**\n'
    db['cogs'] = tuple(bot.cogs.keys())
    await inter.send(embed=utils.Embed(inter, msg), ephemeral=True)


@bot.slash_command()
@commands.is_owner()
async def reload(
    inter,
    cogs: str = commands.Param(choices=list(
        filter(lambda cog: cog not in bot.cogs.values(), utils.cog_files())))):
    '''
  Reload Cogs

  Parameters
  ----------
  cogs: Select a Cog to reload
  '''

    if isinstance(cogs, str):
        cogs = [cogs]
    msg = ''
    for cog in cogs:
        cog = cog.lower()
        bot.reload_extension(f'cogs.{cog}')
        msg += f'> **{cog.title()}**\n'
    await inter.send(embed=utils.Embed(inter, msg), ephemeral=True)


bot.log.info('Loading Cogs...')
for cog in utils.cog_files():
    if f'{cog.lower()}.py' in os.listdir('./cogs'):
        bot.load_extension(f'cogs.{cog.lower()}')
    else:
        db['cogs'].remove(cog)
bot.log.info('Cogs Loaded!')

bot.run(os.environ['token'])
