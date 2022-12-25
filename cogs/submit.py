import disnake as discord
from disnake.ext import commands
import utils
from replit import db
import re

if 'subs' not in db:
  db['subs']={}

class Submit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def list_categories(inter, input):
    return suggestions if any(suggestions:=list(filter(lambda category: input.title() in category.title(), db['subs'].keys()))) else [f'Register: {input.title()}']
    
  @commands.slash_command()
  async def submit(self, inter, category=commands.Param(autocomplete=list_categories), score:float=None):
    '''
    Submit a Score
    
    Parameters
    ----------
    category: The category if the submission
    score: Score if category is score based
    '''
    if category.startswith('Register: '):
      category = category[10:]
      db['subs'][category]={}
      await inter.send(embed=utils.Embed(inter, f'Registered category: **{category}**'))
      
    if score:
      await inter.send(embed=utils.Embed(inter, f'{inter.author.mention} registered a Score for **{category}**: {score}'))
      db['subs'][category][str(inter.author.id)] = score
    else:
      await inter.send(embed=utils.Embed(inter, f'{inter.author.mention} registered a Submission for **{category}**'))
      sent = await inter.original_message()
      db['subs'][category][str(inter.author.id)] = sent.id
      await sent.add_reaction('⭐')
      
  @commands.slash_command()
  async def leaderboard(self, inter, category=commands.Param(choices=list(db['subs'].keys())), visible: bool=False):
    '''
    List the Scores for a category
    
    Parameters
    ----------
    category: What category to list
    visible: Should anyone see the Leaderboard
    '''
    subs = list(db['subs'][category].items())
    subs.sort(key=lambda sub: sub[1])
    scores=[]
    for i, sub in enumerate(subs):
      scores.append(f'{i+1}. {member.mention if (member:=inter.guild.get_member(int(sub[0]))) else self.bot.get_user(int(sub[0])).name}: {(str(reaction.count-1)+"⭐" if (reaction:=next(filter(lambda reaction: reaction.emoji=="⭐", (await inter.channel.fetch_message(sub[1])).reactions), None)) else 0) if isinstance(sub[1], int) else sub[1]}')
    await inter.send(embed=utils.Embed(inter, title=category, description='\n'.join(scores)), ephemeral= not visible)
    
def setup(bot):
  bot.add_cog(Submit(bot))
