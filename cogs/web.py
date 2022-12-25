from web import web, shutdown
from disnake.ext import commands

class Web(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    bot.loop.create_task(self.init())

  async def init(self):
    await self.bot.wait_until_ready()
    await web(self.bot)
  
  def cog_unload(self):
    shutdown()

def setup(bot):
  bot.add_cog(Web(bot))