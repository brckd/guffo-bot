import disnake as discord
from disnake.ext import commands
import utils
from replit import db
import re
import math
import random

class Custom(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def send(self, ctx, *, text):
    '''
    Send a message with Markdown formatting

    Parameters
    ----------
    text: the text to send
    '''
    
    # evaluate code
    code = map(lambda code: str(eval(
      code[1:-1],
      {"__builtins__": None},
      {
        'int': int, 'str': str, 'list': list, 'dict': dict, 'map': map, 'len': len, # builtins
        're': re, 'math': math, 'random': random, # libs
        'ctx': ctx, # vars
        'img': lambda member: f'![{member.display_name}]({member.display_avatar})' # helpers
      }
    )), re.findall(r'{[^{}]+}', text))
    
    other = re.split(r'{[^{}]+}', text)
    text = other.pop(0)+''.join(map(lambda c,o: c+o, code, other))

    # format lists
    text = re.sub(r'^ ?[-*+] ', '_ _• ', text, re.MULTILINE)
    text = re.sub(r'^ ?\[ \] ', '_ _\\☐ ', text, re.MULTILINE)
    text = re.sub(r'^ ?\[[xX]\] ', '_ _\\☑ ', text, re.MULTILINE)
    
    content = ''.join(re.split(r'```md\n[^`]*```', text))
    embeds = re.findall(r'```md\n[^`]*```', text)

    # format webhook
    username = ctx.author.display_name
    avatar_url = ctx.author.display_avatar.url
    match = re.search(r'!\[.+\]\(https?://\S+\)', content)
    if match:
      tupper = match.group().split('](')
      username = tupper[0][2:]
      avatar_url = tupper[1][:-1]
      content = content[:match.span()[0]] + content[match.span()[1]:]
      if not content: content = '_ _'
      
        
    # format embeds
    for i, embed in enumerate(embeds):
      
      headers = re.findall(r'^#+ .+$', embed[6:-3], flags=re.MULTILINE)
      descs = re.split(r'^#+ .+$', embed[6:-3], flags=re.MULTILINE)
      
      # format tables
      for desc in descs:
        for table in re.finditer(r'(^(\|[^|].+[^|]\|\n*)+$)', desc, flags=re.MULTILINE):
          colums = (list(zip(*map(
            lambda line: line.strip('|').split('|'),
            table.group().split('\n')
            ))))
          print(colums)
          
        
      # format author
      match = re.search(r'!\[.+\]\(https?://\S+\)', descs[0])
      if match:
        name, icon_url = match.group().split('](')
        author = {'name': name[2:], 'icon_url': icon_url[:-1]}
        descs[0] = descs[0][:match.span()[0]] + descs[0][match.span()[1]:]
      else: author = {}
      
      # format footer
      match = re.search(r'!\[.+\]\(https?://\S+\)', descs[-1])
      if match:
        text, icon_url = match.group().split('](')
        footer = {'text': text[2:], 'icon_url': icon_url[:-1]}
        descs[-1] = descs[-1][:match.span()[0]] + descs[-1][match.span()[1]:]
        if not descs[-1]: descs[-1] = '_ _'
      else: footer = {}

      title = ''
      desc = descs.pop(0)
      if desc.strip() == '':
        title = '#'.join(headers.pop(0).split('# ')[1:])
        desc = descs.pop(0)
      
      # format headers
      fields = list(map(lambda header, desc: {'name': header.split('# ')[1], 'value': desc}, headers, descs))
      
      # split in chunks
      n = 1024
      fields = [{'name': (field['name']+'_ _' if i==0 else '_ _'), 'value': chunk+'_ _', 'inline': False} for field in fields for i, chunk in enumerate([field['value'][i:i+n] for i in range(0, len(field['value'])+1, n)])]
      
      # embed
      embeds[i] = discord.Embed.from_dict({
        'color': db['color'],
        'author': author,
        'title': title,
        'description': desc,
        'fields': fields,
        'footer': footer
        })
    webhook = await utils.Webhook(ctx)
    sent = await webhook.send(username=username, avatar_url=avatar_url, content=content, embeds=embeds, wait=True)
    db['msgs'][str(sent.id)] = ctx.author.id
    
def setup(bot):
  bot.add_cog(Custom(bot))