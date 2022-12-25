import disnake as discord
from disnake.ext import commands
import utils

class Errors(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_slash_command_error(self, inter, error):
    await inter.send(embed=utils.Embed(inter, str(error), type(error).__name__, color = discord.Color.red().value), ephemeral=True)
  
  @commands.Cog.listener()
  async def on_message_command_error(self, inter, error):
    await self.on_slash_command_error(inter, error)

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    await ctx.reply(embed=utils.Embed(ctx, str(error), type(error).__name__, color = discord.Color.red().value))

def setup(bot):
  bot.add_cog(Errors(bot))
