import disnake as discord
from disnake.ext import commands
from replit import db
import utils

if 'roles' not in db:
  db['roles'] = {}

commands.MessageConverter
class React(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['ar'])
  @commands.has_permissions(manage_roles=True)
  async def addrole(self, ctx, emoji: str, role: commands.RoleConverter, message: commands.MessageConverter=None):
    if not message:
      reference = ctx.message.reference
      if reference:
        message = reference.resolved
      else:
        message = ctx.message
    msgid = str(message.id)

    if msgid not in db['roles']:
      db['roles'][msgid] = {}
    await message.add_reaction(emoji)
    db['roles'][msgid][emoji] = role.id

  @commands.command(aliases=['rr'])
  @commands.has_permissions(manage_roles=True)
  async def rmrole(self, ctx, emoji: str, message: commands.MessageConverter=None):
    if not message:
      reference = ctx.message.reference
      if reference:
        message = reference.resolved
      else:
        message = ctx.message
    msgid = str(message.id)

    if msgid not in db['roles']:
      db['roles'][msgid] = {}
    await message.remove_reaction(emoji, ctx.guild.me)
    del db['roles'][msgid][emoji]
      
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    guild = self.bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
      return
    if member.bot:
      return
    emoji = str(payload.emoji)
    msgid = str(payload.message_id)

    if msgid in db['roles']:
      if emoji in db['roles'][msgid]:
        await member.add_roles(guild.get_role(db['roles'][msgid][emoji]))
      
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    guild = self.bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
      return
    if member.bot:
      return
    emoji = str(payload.emoji)
    msgid = str(payload.message_id)

    if msgid in db['roles']:
      if emoji in db['roles'][msgid]:
        await member.remove_roles(guild.get_role(db['roles'][msgid][emoji]))


  @commands.command()
  @commands.is_owner()
  async def poll(self, ctx, message: commands.MessageConverter=None):
    if not message:
      reference = ctx.message.reference
      if reference:
        message = reference.resolved
      else:
        message = ctx.message

    lb = message.reactions
    lb.sort(key=lambda reaction: reaction.count, reverse=True)
    await message.reply(embed=utils.Embed(message, title=f'Option {lb[0].emoji} Won!', description='\n'.join(f'{reaction.emoji}: {reaction.count}' for reaction in lb)))

  @commands.Cog.listener()
  async def on_message_delete(self, msg):
    if str(msg.id) in db['roles']:
      del db['roles'][str(msg.id)]

def setup(bot):
  bot.add_cog(React(bot))