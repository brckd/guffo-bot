from disnake.ext import commands
import random
import utils

class Bah(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  #commands
  @commands.command()
  async def bah(self, ctx):
    await ctx.send('<:bah:868130973794058270>')

  @commands.command()
  async def bahword(self, ctx):
    with open('assets/bah.txt', 'r') as word_file:
      await ctx.send(embed=utils.Embed(ctx, random.choice(word_file.read().split()).replace('ba', '<:bah:868130973794058270>')))

def setup(bot):
  bot.add_cog(Bah(bot)) 