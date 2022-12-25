import disnake as discord
from disnake.ext import commands
import re
import utils
from replit import db

if 'msgs' not in db:
  db['msgs'] = {}

class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def tupper(self, inter, content, member: discord.Member=None):
    '''
    Impersonate someone

    Parameters
    ----------
    content: What you want to say
    member: Member to impersonate
    '''
    if not member: member = inter.author
    await inter.send('_ _', delete_after=0)
    webhook = (await utils.Webhook(inter))
    sent = await webhook.send(content=content, username=member.display_name, avatar_url=member.avatar, wait=True)
    db['msgs'][str(sent.id)] = inter.author.id
  
  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author.bot:
      return
    reg = ':[0-9a-zA-Z_]+:'
    other = re.split(reg, msg.content)
    emjs = re.findall(reg, msg.content)
    content=other[0]
    for i in range(len(emjs)):
      myemjs = tuple(filter(lambda emj: emj.name==emjs[i][1:-1], self.bot.emojis))
      emj = f'<:{myemjs[0].name}:{myemjs[0].id}>' if (any(myemjs) and not other[i].endswith('<')) else emjs[i]
      content+=emj+other[i+1]
    if content==msg.content: return
    if msg.reference and len(msg.content.split())==1:
      await self.react.__call__(msg, myemjs[0], msg.reference.resolved)
    else:
      webhook = (await utils.Webhook((await self.bot.get_context(msg))))
      sent = await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.avatar, wait=True)
      db['msgs'][str(sent.id)] = msg.author.id
      await msg.delete()

  @commands.slash_command()
  async def react(self, inter, emoji:discord.Emoji, message:discord.Message):
    '''
    Let a Tupper add a Reaction

    Parameters
    ----------
    emoji: The Emoji to react with
    message:  The Message Url you want to react to
    '''
    await message.add_reaction(emoji)
    if isinstance(inter, discord.Message):
      sent = await inter.author.send('Reaction added!\nMake sure to add your own Reaction for it to stay')
      await inter.delete()
    else:
      await inter.send('Reaction added!\nMake sure to add your own Reaction for it to stay', ephemeral=True)
    try:
      await self.bot.wait_for('reaction_add', check=lambda react, user: react.message==message and user==inter.author, timeout=10)
      await message.remove_reaction(emoji, self.bot.user)
      if sent: await sent.delete()
    except:
      await message.remove_reaction(emoji, self.bot.user)
      if sent: await sent.delete()
  
  @commands.message_command(name='Tupper Info')
  async def tup_info(self, inter, msg):
    await inter.send(embed=utils.Embed(
      inter,
      f'Tupper sent by {msg.guild.get_member(db["msgs"][str(msg.id)]).mention}'
    ), ephemeral=True)
  
  @commands.message_command(name='Delete Tupper')
  async def del_tup(self, inter, msg):
    if str(msg.id) not in db['msgs']: raise commands.CommandError('This is not a Tupper')
    if db["msgs"][str(msg.id)] != inter.author.id: raise commands.CommandError('You do not own this Tupper')
    await msg.delete()
    await inter.send(embed=utils.Embed(inter, 'Tupper has succesfully been deleted'), ephemeral=True)
    
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot: return
    if str(payload.message_id) not in db['msgs']: return
    msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name == '❌' and db["msgs"][str(payload.message_id)] == payload.member.id:
      
      await msg.delete()
    if payload.emoji.name == '❓':
      await payload.member.send(embed=utils.Embed(
        msg,
        f'Tupper sent by {str(msg.guild.get_member(db["msgs"][str(payload.message_id)]))}'
      ))
        
def setup(bot):
  bot.add_cog(Test(bot))