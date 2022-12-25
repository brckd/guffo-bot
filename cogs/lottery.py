from disnake.ext import commands
import disnake as discord
import random
from PIL import Image
import utils
import time
import datetime
from replit import db
import os


class Lottery(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.slash_command()
  @commands.is_owner()
  async def spin(self, inter):
    '''
    Generate random ascending Numbers from 1 to 9
    '''
    nums = random.sample(range(1, 9), 3)
    nums.sort()
    
    history = []
    async for msg in inter.channel.history(after=(datetime.datetime.fromtimestamp(db['spinned']) if 'spinned' in db else None)):
      if sum(c.isdigit() for c in msg.content)==3: 
        for m in filter(lambda m: m.author==msg.author, history):
          history.remove(m)
        history.append(msg)
    match = lambda msg: [str(n) for n in nums if str(n) in msg.content]
    matches = max([len(match(msg)) for msg in history]) if any(history) else 0
    winners = [(msg.author, match(msg)) for msg in history if len(match(msg))==matches]
    
    send = f'{winners[0][0].mention} won <:clap:968443589325651968> Enjoy the new role and the prize! <:guffo_happy:976495961721438228> <:confetti:977574168939872276>' if matches==3 else \
    'Nobody won but '+' '.join(f'{memb.mention} ({", ".join(match)})' for memb, match in winners)+' came close <:guffo:968444036354543626>' if matches==2 else \
    'Noone came close <:sweatsmile:968445668798652436>'
    embed=utils.Embed(inter, send, ', '.join(str(num) for num in nums))
    await inter.send(embed=embed)
    db['spinned'] = time.time()
    sent = await inter.original_message()
    
    tiles = Image.open("assets/tiles.png")
    guffos = Image.new('RGBA', (tiles.size[0], tiles.size[1]), (250,250,250,0))
    guffo = Image.open("assets/guffo.png")
    
    for i in nums:
      guffos.paste(
        guffo,
        (tiles.size[0]//3*((i-1)%3),tiles.size[1]//3*((i-1)//3))
      )
    
    spin = Image.alpha_composite(tiles, guffos)
    spin.save('assets/spin.png')
    await sent.edit(embed=embed.set_image(file=discord.File('assets/spin.png')))
  
  @commands.Cog.listener()
  async def on_message(self, msg):
    return
    

def setup(bot):
  bot.add_cog(Lottery(bot))