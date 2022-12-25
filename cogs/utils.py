from disnake.ext import commands
from replit import db
import replit
import utils
import requests
import json
from bs4 import BeautifulSoup

if 'channels' not in db:
  db['channels']={}
if 'announcechannel' not in db:
  db['announcechannel'] = ''

class MyHelpCommand(commands.MinimalHelpCommand):
  async def send_pages(self):
      destination = self.get_destination()
      e = utils.Embed(self, '')
      for page in self.paginator.pages:
          e.description += page
      await destination.send(embed=e)


class Utils(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  @commands.is_owner()
  async def prefix(self, inter, prefix: str = None):
    '''
    See current Prefix

    Parameters
    ----------
    prefix: Enter new Prefix
    '''
    if not prefix:
      await inter.send(embed=utils.Embed(inter, description=f'Current prefix is: `{db["prefix"][str(inter.guild.id)]}`'))
    else:
      db['prefix'][str(inter.guild.id)] = prefix
      await inter.send(embed=utils.Embed(inter, f'Prefix got changed to: `{prefix}`'))
  
  def tree(self, d, i=0):
    x = d
    if isinstance(d, (replit.database.database.ObservedDict, dict)):
      x = ''
      for key, value in d.items():
        x += '\t'*i + str(key) + ':\n'
        if value == db or type(value) in (replit.database.database.ObservedDict, replit.database.database.ObservedList):
          x += self.tree(value, i+1)
        else:
          x+= '\t'*(i+1) + str(value) + '\n'

    elif isinstance(d, (replit.database.database.ObservedList, list)):
      x = []
      for e in d:
        if e == db or type(e) in (replit.database.database.ObservedDict, replit.database.database.ObservedList):
          x.append(self.tree(e, i+1))
        else:
          x.append(str(e))
      x = '\t'*(i)+', '.join(x)+'\n'
    return x
  
  @commands.slash_command()
  @commands.is_owner()
  async def database(self, inter, key: str = commands.Param(choices=list(db.keys())[:25]), overwrite:str = None):
    '''
    Select none to list all keys
    
    Parameters
    ----------
    key: Select a Key in the Database to view its Value
    overwrite: Overwrite the Key's Value
    '''
    if overwrite:
      db[key]=overwrite
      await inter.send(embed=utils.Embed(inter, f'{key} has been overwritten to ```{self.tree(db[key])}```', key), ephemeral=True)
    else:
      await inter.send(embed=utils.Embed(inter, f'```{self.tree(db[key])}```', key), ephemeral=True)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    msg = (await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id))
    if payload.emoji.name == '❌' and payload.member != self.bot.user and msg.author==self.bot.user:
      await msg.delete()

  @commands.Cog.listener()
  async def on_member_join(self, member):
    for channel in member.guild.text_channels:
      if channel.id == int(db['announcechannel']):
        await channel.send(embed=utils.Embed(None, title='Welcome!', description=f'Hello {member.mention} <:guffo:968444036354543626> Welcome to **{member.guild.name}** <:waving_hand:968445485104914472>', footer={'text': 'make sure to read #rules'}))
      
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    for channel in member.guild.text_channels:
      if channel.id == int(db['announcechannel']):
        await channel.send(embed=utils.Embed(None, title='Bye!',description=f'{member.mention} left the server <:guffo_crying:976495961641746522> All Guffos will remember you <:waving_hand:968445485104914472>', footer={'text': 'please come back'}))
  
  async def suggest(inter, query):
    return json.loads(requests.get(f'http://google.com/complete/search?client=chrome&q={query}').text)[1]

  @commands.slash_command()
  async def google(self, inter, query=commands.Param(autocomplete=suggest)):
    '''
    Query Google search

    Parameters
    ----------
    query: Text to search for
    '''
    request = requests.get(f'https://google.com/search?q={query}')
    soup = BeautifulSoup(request.text, 'html.parser')
    await inter.send(embed=utils.Embed(inter, title=f'Search results for *{query}*', description='\n'.join(f'**[{h.getText()}]({str(h.parent.get("href"))[7:].split("&sa=")[0]})**\n{str(h.parent.get("href"))[7:].split("&sa=")[0]}' for h in soup.find_all('h3')[:5])))
  
def setup(bot):
  bot.help_command = MyHelpCommand()
  bot.help_command.cog = Utils(bot)
  bot.add_cog(Utils(bot))
  