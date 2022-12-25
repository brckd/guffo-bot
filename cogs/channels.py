import disnake as discord
from disnake.ext import commands
from replit import db
from typing import Union
import utils

if 'counters' not in db:
  db['counters']={}

if 'types' not in db:
  db['types']={}

def channeltype(type):
  return f'**{type.title()} Channel**'
class Mediatype(str):
  pass

class Channels(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.loop.create_task(self.load())

  @commands.group()
  @commands.is_owner()
  async def type(self, ctx):
    if not ctx.invoked_subcommand:
      await self.show.__call__(ctx, ctx.channel)
  
  @type.command()
  async def show(self, ctx, filter: Union[discord.TextChannel, Mediatype]):
    if type(filter)==list:
      await ctx.reply(embed=utils.Embed(ctx, '\n'.join((f"<#{channel}>: {channeltype(db['types'][channel])}" for channel in db['types']))))

    if type(filter)==discord.TextChannel:
      await ctx.reply(embed=utils.Embed(ctx, f"<#{filter.id}>: {channeltype(db['types'][str(filter.id)])}"))
      
    if type(filter)==Mediatype:
      await ctx.reply(embed=utils.Embed(ctx, f'{channeltype(filter)}:'+'\n'+'\n'.join((f'<#{channel}>' for channel in db['types'] if db['types'][channel]==filter))))
    

  async def load(self):
    for name in ['text', 'image', 'audio', 'video', 'files']:
      @commands.command(name=name, cog=self)
      async def command(ctx, channel: discord.TextChannel=None):
        if not channel:
          channel = ctx.channel
        channelid = str(channel.id)
        db['types'][channelid] = ctx.command.name
        if ctx.command.name=='text':
          del db['types'][channelid]
        await ctx.reply(embed=utils.Embed(ctx, f'<#{channelid}> is now a {channeltype(ctx.command.name)}!'))
      self.type.add_command(command)
      
  @commands.Cog.listener()
  async def on_message(self, message):
    channelid = str(message.channel.id)
    if (await self.bot.get_context(message)).command or channelid not in db['types']:
      return
    if not any([attachment.content_type.startswith(db['types'][channelid]) for attachment in message.attachments]) and not db['types'][channelid]=='text':
      await message.delete()

  
  @commands.command(aliases=['ac'])
  @commands.is_owner()
  async def addcounter(self, ctx, role:discord.Role='@everyone'):
    if role=='@everyone':
      role = ctx.guild.roles[0]
    channel = await ctx.guild.create_voice_channel(
      name=f'{role.name}: {len([member for member in ctx.guild.members if role in member.roles])}',
      overwrites= {ctx.guild.roles[0]: discord.PermissionOverwrite(connect=False)}
      )
    db['counters'][role.id] = channel.id
    
  @commands.command(aliases=['rc'])
  @commands.is_owner()
  async def rmcounter(self, ctx, role:commands.RoleConverter='@everyone'):
    if role=='@everyone':
      role = ctx.guild.roles[0]
    roleid = str(role.id)
    if roleid in db['counters']:
      await self.bot.get_channel(db['counters'][roleid]).delete()
      del db['counters'][roleid]
    else:
      raise commands.ChannelNotFound(role.name)

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    for roleid in db['counters']:
      role = after.guild.get_role(int(roleid))
      channel = after.guild.get_channel(db['counters'][roleid])
      if not channel:
        return
      name = f'{role.name}: {len([member for member in after.guild.members if role in member.roles])}'
      if channel.name != name:
        await channel.edit(name=name)

def setup(bot):
  bot.add_cog(Channels(bot)) 