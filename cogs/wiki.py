from disnake.ext import commands
import disnake as discord
import requests
import utils
import re
import os
import io

class Wiki(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  async def list_docs(inter, input):
    root='docs'
    return [doc for docs in [filter(lambda doc: input.lower() in doc.lower(), list(map(lambda doc: subroot[len(root)+1:].replace('\\','/')+('/' if len(subroot)>len(root) else '')+doc.replace('.md',''), docs))) for subroot,dirs,docs in os.walk(root)] for doc in docs][:25]

  @commands.slash_command()
  async def doc(self, inter, query=commands.Param(autocomplete=list_docs), visible: bool=False):
    '''
    Browse the Fancade Wiki
    
    Parameters
    ----------
    query: search a Page in the wiki
    visible: wether the result is visible to everyone
    '''
    
    root = f'https://www.fancade.com/wiki/'
    with open(f'docs/{query}.md') as file:
      desc = file.read()
      
    # format local hyperlinks
    others = re.split(r'\[\[[^]]+]]', desc)
    matches = re.findall(r'\[\[[^]]+]]', desc) 
    desc = ''.join(map(lambda other,match: other+f'{"!" if match.startswith("[[uploads/") else ""}[{match[2:-2].split("|")[0].replace("-"," ").split("/")[-1]}]({root+match[2:-2].split("|")[-1].replace(" ","-")})', others, matches))+others[-1]

    # format pictures
    desc = re.sub(r'!\[[^]]+]', '[🖼️]', desc)
    img_url = imgs[0][5:-1] if any(imgs:=re.findall(r'\[🖼️]\(.+\)', desc)) else None
    img = io.BytesIO(requests.get(img_url).content) if img_url else None
    
    desc = re.sub(r'\n(\*|-) ', r'\n• ', desc)
    
    # format headers
    others = re.split(r'\n#+.+\n', desc)
    matches = re.findall(r'\n#+.+\n', desc)
    desc = others.pop(0)
    fields = list(map(lambda match,other: {'name': match[4:], 'value': other}, matches, others))
    n = 1024
    fields = [{'name': (field['name'] if i==0 else '_ _'), 'value': chunk} for field in fields for i, chunk in enumerate([field['value'][i:i+n] for i in range(0, len(field['value']), n)])]

    # embed
    embed = utils.Embed(inter, title=query, url=root+query.lower().replace(' ','-'), description=desc, fields=fields)
    if img: embed.set_thumbnail(file=discord.File(img, filename=img_url.split('/')[-1]))
      
    await inter.send(embed=embed, ephemeral=not visible)
    
def setup(bot):
  bot.add_cog(Wiki(bot)) 