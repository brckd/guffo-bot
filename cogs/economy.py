import disnake as discord
from disnake.ext import commands
from replit import db
import random
import time
import utils

if 'xp' not in db:
    db['xp'] = {}

if 'shop' not in db:
    db['shop'] = {}

if 'inv' not in db:
    db['inv'] = {}

db['color'] = discord.Color.from_rgb(255, 127, 148).value


def altmember(ctx, member):
    if member is None:
        if ctx.message.reference is None:
            return ctx.author
        else:
            return ctx.message.reference.resolved.author
    else:
        return member


def othermember(ctx, member):
    if member is None:
        if ctx.message.reference is None:
            return
        else:
            return ctx.message.reference.resolved.author
    else:
        return member


def allbal(member, amount):
    if amount == 'all':
        return db['bal'][str(member.id)]
    else:
        return int(amount)


def cash(amount):
    return f'{amount:3,.0f} <:guffo_coin:888125079710474280>'


def xp(amount):
    return f'{amount:3,.1f} <:up_arrow:875389237233610802>'


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rich(self, ctx):
        name = 'Richest Guffo'
        role = next((r for r in ctx.guild.roles if r.name == name), await
                    ctx.guild.create_role(name=name,
                                          color=discord.Colour.gold()))

        for member in role.members:
            member.remove_roles(role.id)

        members = list(db['bal'].items())
        members.sort(key=lambda i: i[1], reverse=True)

        if members[0]:
            await (await ctx.guild.get_or_fetch_member(int(members[0][0])
                                                       )).add_roles(role)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = altmember(ctx, member)
        if str(member.id) not in db['bal']:
            db['bal'][str(member.id)] = 0
        await ctx.reply(embed=utils.Embed(
            ctx, f"{member.mention} has {cash(db['bal'][str(member.id)])}"))

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        await ctx.reply(embed=utils.Embed(
            ctx, '\n'.join(
                f'`{" " if i<9 else ""}{i+1}.` {member.mention}: {cash(bal)}'
                for i, (member, bal) in enumerate(
                    sorted(((member, db['bal'][str(member.id)])
                            for member in ctx.guild.members
                            if (db['bal'][str(member.id)] != 0 if (
                                str(member.id)) in db['bal'] else False)),
                           key=lambda i: i[1],
                           reverse=True)))))

    @commands.command(aliases=['lvls'])
    async def levels(self, ctx):
        await ctx.reply(embed=utils.Embed(
            ctx, '\n'.join(
                f'`{" " if i<9 else ""}{i+1}.` {member.mention}: {bal}'
                for i, (member, bal) in enumerate(
                    sorted((
                        (member, int((db['xp'][str(member.id)] / 100)**0.4))
                        for member in ctx.guild.members
                        if (int((db['xp'][str(member.id)] / 100)**0.4) != 0 if
                            (str(member.id)) in db['xp'] else False)),
                           key=lambda i: i[1],
                           reverse=True)))))

    @commands.command(
        description='amount:\n?? - set cash\n??xp - set xp\n??lvl - set lvl')
    @commands.is_owner()
    async def set(
        self,
        ctx,
        amount,
        member: discord.Member = None,
    ):
        member = altmember(ctx, member)
        memberid = str(member.id)
        if amount.endswith('xp'):
            amount = int(amount[:-2])
            if memberid not in db['xp']:
                db['xp'][memberid] = 0
            db['xp'][memberid] = amount
            await ctx.reply(embed=utils.Embed(
                ctx, f"{member.mention} now has {xp(amount)}"))

            if int((db["xp"][memberid] / 100)**0.4) > int(
                ((db["xp"][memberid] - amount) / 100)**0.4):
                for channel in filter(lambda channel: 'level' in channel.name,
                                      ctx.guild.text_channels):
                    await channel.send(embed=discord.Embed(
                        title='Level Up',
                        description=
                        f'{ctx.author.mention} has advanced to lvl {int((db["xp"][memberid]/100)**0.4)} 🏁',
                        color=db['color']).set_footer(
                            text=ctx.author.display_name,
                            icon_url=ctx.author.display_avatar.url))
        elif amount.endswith('lvl'):
            amount = int(amount[:-3])
            if memberid not in db['xp']:
                db['xp'][memberid] = 0
            db['xp'][memberid] = (amount**(1 / 0.4)) * 100
            await ctx.reply(embed=utils.Embed(
                ctx, f"{member.mention} now has {amount}lvls"))

            if int((db["xp"][memberid] / 100)**0.4) > int(
                ((db["xp"][memberid] - amount) / 100)**0.4):
                for channel in filter(lambda channel: 'level' in channel.name,
                                      ctx.guild.text_channels):
                    await channel.send(embed=discord.Embed(
                        title='Level Up',
                        description=
                        f'{ctx.author.mention} has advanced to lvl {int((db["xp"][memberid]/100)**0.4)} 🏁',
                        color=db['color']).set_footer(
                            text=ctx.author.display_name,
                            icon_url=ctx.author.display_avatar.url))
        else:
            amount = int(amount)
            db['bal'][memberid] = amount
            await ctx.reply(embed=utils.Embed(
                ctx, f"{member.mention} now has {cash(amount)}"))

    @commands.command()
    @commands.is_owner()
    async def add(self, ctx, amount, member: discord.Member = None):
        member = altmember(ctx, member)
        memberid = str(member.id)
        if amount.endswith('xp'):
            amount = int(amount[:-2])
            if memberid not in db['xp']:
                db['xp'][memberid] = 0
            db['xp'][memberid] += amount
            await ctx.reply(
                embed=utils.Embed(ctx, f"{member.mention} got {xp(amount)}"))

            if int((db["xp"][memberid] / 100)**0.4) > int(
                ((db["xp"][memberid] - amount) / 100)**0.4):
                for channel in filter(lambda channel: 'level' in channel.name,
                                      ctx.guild.text_channels):
                    await channel.send(embed=discord.Embed(
                        title='Level Up',
                        description=
                        f'{ctx.author.mention} has advanced to lvl {int((db["xp"][memberid]/100)**0.4)} 🏁',
                        color=db['color']).set_footer(
                            text=ctx.author.display_name,
                            icon_url=ctx.author.display_avatar.url))

        elif amount.endswith('lvl'):
            return  #todo
        else:
            amount = int(amount)
            if memberid not in db['bal']:
                db['bal'][memberid] = 0
            db['bal'][memberid] += amount
            await ctx.reply(
                embed=utils.Embed(ctx, f"{member.mention} got {cash(amount)}"))

    @commands.command()
    @commands.is_owner()
    async def rm(self, ctx, amount, member: discord.Member = None):
        member = altmember(ctx, member)
        memberid = str(member.id)

        if amount.endswith('xp'):
            amount = int(amount[:-2])
            if memberid not in db['xp']:
                db['xp'][memberid] = 0
            db['xp'][memberid] -= amount
            await ctx.reply(
                embed=utils.Embed(ctx, f"{member.mention} lost {xp(amount)}"))

        elif amount.endswith('lvl'):
            return  #todo
        else:
            amount = int(amount)
            if memberid not in db['bal']:
                db['bal'][memberid] = 0
            db['bal'][memberid] -= amount
            await ctx.reply(
                embed=utils.Embed(ctx, f"{member.mention} lost {cash(amount)}")
            )

    @commands.command()
    async def pay(self, ctx, amount, member: discord.Member = None):
        member = othermember(ctx, member)
        if member is None:
            await ctx.reply(embed=utils.Embed(ctx, 'Choose someone to pay'))
        else:
            amount = allbal(ctx.author, amount)
            if str(member.id) not in db['bal']:
                db['bal'][str(member.id)] = 0
            if str(ctx.author.id) not in db['bal']:
                db['bal'][str(ctx.author.id)] = 0

            if amount <= 0:
                await ctx.reply(embed=utils.Embed(ctx, 'Invalid Amount'))
                return
            if db['bal'][str(ctx.author.id)] < amount:
                await ctx.reply(
                    embed=utils.Embed(ctx, 'You dont have that much money'))
                return

            db['bal'][str(ctx.author.id)] -= int(amount)
            db['bal'][str(member.id)] += int(amount)
            await ctx.reply(embed=utils.Embed(
                ctx, f'You payed {member.mention} {cash(amount)}'))

    async def collect(self, ctx, key, cooldown, reward):
        member = ctx.author
        if str(member.id) not in db['bal']:
            db['bal'][str(member.id)] = 0
        if str(member.id) not in db[key]:
            db[key][str(member.id)] = 0

        if (time.time() - db[key][str(member.id)]) < cooldown:
            await ctx.reply(embed=utils.Embed(
                ctx,
                f"You already collected your {key} reward. Try again <t:{int(db[key][str(member.id)]+cooldown)}:R>"
            ))

        else:
            db[key][str(member.id)] = time.time()
            db['bal'][str(member.id)] += reward
            await ctx.reply(embed=utils.Embed(
                ctx, f'You collected your {key} {cash(reward)}'))

    @commands.command(aliases=['cd'])
    async def cooldown(self, ctx):
        await ctx.reply(
            embed=utils.Embed(ctx, "This command doesn't exist lol"))

    @commands.command()
    async def work(self, ctx):
        await self.collect(ctx, 'work', 60 * 60, random.randint(20, 50))

    @commands.command()
    async def daily(self, ctx):
        await self.collect(ctx, 'daily', 24 * 60 * 60, 50)

    @commands.command()
    async def weekly(self, ctx):
        await ctx.reply(
            embed=discord.Embed(title='CommandNotFound',
                                description='Command "weekly" is not found',
                                color=discord.Color.red().value))
        await ctx.reply(embed=utils.Embed(ctx, 'or is it?'))
        await self.collect(ctx, 'weekly', 7 * 24 * 60 * 60, 50)

    @commands.command()
    async def monthly(self, ctx):
        await self.collect(ctx, 'monthly', 30 * 24 * 60 * 60, 500)

    @commands.command()
    async def shop(self, ctx):
        '''
    Lists all items that are currently in the shop
    '''
        await ctx.reply(embed=utils.Embed(
            ctx, '\n'.join(f'`{i+1}.` {item}: {cash(price)}'
                           for i, (price, item) in enumerate(
                               sorted(((price, item)
                                       for item, price in db['shop'].items()),
                                      reverse=True)))))

    @commands.command()
    async def buy(self, ctx, *, item):
        item = item.title()
        authorid = str(ctx.author.id)
        if str(ctx.author.id) not in db['bal']:
            db['bal'][authorid] = 0

        if authorid not in db['inv']:
            db['inv'][authorid] = {}
        if item not in db['shop']:
            await ctx.reply(embed=utils.Embed(ctx, 'Item not found!'))
        if db['bal'][authorid] < db['shop'][item]:
            await ctx.reply(embed=utils.Embed(ctx, 'Not enough Money!'))
            return
        if item not in db['inv'][authorid]:
            db['inv'][authorid][item] = 0

        if item not in db['inv'][authorid]:
            db['inv'][authorid][item] = 0
        db['bal'][authorid] -= db['shop'][item]
        db['inv'][authorid][item] += 1
        if not authorid in db['xp']:
            db['xp'][authorid] = 0
        db['xp'][authorid] += ((db['shop'][item] / 10)**1.1) * 10
        await ctx.reply(embed=utils.Embed(
            ctx,
            f'Item puchased: `{item}`\n*earned {xp(((db["shop"][item]/10)**1.1)*10)}*'
        ))

        if int((db["xp"][authorid] / 100)**0.4) > int(
            ((db["xp"][authorid] - db["shop"][item]) / 100)**0.4):
            for channel in filter(lambda channel: 'level' in channel.name,
                                  ctx.guild.text_channels):
                await channel.send(embed=utils.Embed(
                    ctx,
                    f'{ctx.author.mention} has advanced to lvl {int((db["xp"][authorid]/100)**0.4)} 🏁',
                    title='Level Up'))

    @commands.command()
    @commands.is_owner()
    async def sell(self, ctx, item, price=None):
        item = item.title()
        if not price:
            del db['shop'][item]
            await ctx.reply(
                embed=utils.Embed(ctx, f'removed item from shop: `{item}`'))
        else:
            db['shop'][item] = int(price)
        await ctx.reply(embed=utils.Embed(
            ctx, f'added item to shop: {item}\nprice: {cash(int(price))}'))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 1003774788227051662: return  # spam
        if msg.author.bot: return
        authorid = str(msg.author.id)
        if not authorid in db['xp']:
            db['xp'][authorid] = 0
        db['xp'][authorid] += 50

        if int((db["xp"][authorid] / 100)**0.4) > int(
            ((db["xp"][authorid] - 50) / 100)**0.4):
            for channel in filter(lambda channel: 'level' in channel.name,
                                  msg.guild.text_channels):
                await channel.send(embed=utils.Embed(
                    msg,
                    f'{msg.author.mention} has advanced to lvl {int((db["xp"][authorid]/100)**0.4)} 🏁',
                    title='Level Up'))

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member = None):
        member = altmember(ctx, member)
        memberid = str(member.id)
        if not memberid in db['xp']:
            db['xp'][memberid] = 0
        await ctx.reply(embed=utils.Embed(
            ctx,
            f"""{member.mention}'s current lvl is {int((db['xp'][memberid]/100)**0.4)}
  with {xp(db['xp'][memberid]-(int((db['xp'][memberid]/100)**0.4))**(1/0.4)*100)} out of {xp((int((db['xp'][memberid]/100)**0.4)+1)**(1/0.4)*100-(int((db['xp'][memberid]/100)**0.4))**(1/0.4)*100)} for next lvl"""
        ))

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        await ctx.reply(embed=utils.Embed(
            ctx, '\n'.join(
                f'`{i+1}.` {item}: {db["inv"][str(ctx.author.id)][item] if item in db["inv"][str(ctx.author.id)] else 0}'
                for i, (price, item) in enumerate(
                    sorted(((price, item)
                            for item, price in db['shop'].items()),
                           reverse=True)))))

    @commands.command(aliases=['rps'])
    async def rockpaperscissor(self, ctx, move=None):
        if str(ctx.author.id) not in db['bal']:
            db['bal'][str(ctx.author.id)] = 0
        prizes = [0, 100, -100]
        if db['bal'][str(ctx.author.id)] < -prizes[2]:
            await ctx.reply(embed=utils.Embed(ctx, 'Not enough Money!'))
            return
        emojis = ['🪨', '📄', '✂️']

        if move is not None and move[0].lower() in ['r', 'p', 's']:
            table = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
            msgs = ['Tie!', 'You win!', 'You lose!']
            usrmove = ['r', 'p', 's'].index(move[0].lower())
            botmove = random.randint(0, 2)
            result = table[usrmove][botmove]
            await ctx.reply(embed=utils.Embed(
                ctx,
                f'{emojis[usrmove]} | {emojis[botmove]}\n{msgs[result]} {cash(prizes[result])}'
            ))
            db['bal'][str(ctx.author.id)] += prizes[result]

        else:
            msg = (await ctx.reply(embed=utils.Embed(ctx, 'Select your Move')))
            for reaction in emojis:
                await msg.add_reaction(reaction)

    @commands.command()
    async def flip(self, ctx, move=None):
        if str(ctx.author.id) not in db['bal']:
            db['bal'][str(ctx.author.id)] = 0
        prizes = [50, -50]
        if db['bal'][str(ctx.author.id)] < -prizes[1]:
            await ctx.reply(embed=utils.Embed(ctx, 'Not enough Money!'))
            return
        emojis = [
            '<:guffo:968444036354543626>', '<:guffo_coin:888125079710474280>'
        ]

        if move is not None and move[0].lower() in ['h', 't']:
            msgs = ['You win!', 'You lose!']
            usrmove = ['h', 't'].index(move[0].lower())
            flip = random.randint(0, 1)
            if flip == usrmove:
                result = 0
            else:
                result = 1
            await ctx.reply(embed=utils.Embed(
                ctx,
                f'{emojis[usrmove]} | {emojis[flip]}\n{msgs[result]} {cash(prizes[result])}'
            ))
            db['bal'][str(ctx.author.id)] += prizes[result]
        else:
            msg = (await ctx.reply(embed=utils.Embed(ctx, 'Select your Move')))
            for reaction in emojis:
                await msg.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        ctx = await self.bot.get_context(reaction.message)
        usrid = str(user.id)
        if user.bot or not any(ctx.message.embeds):
            return
        if not ctx.message.embeds[0].description == 'Select your Move':
            return
        if usrid not in db['bal']:
            db['bal'][str(user.id)] = 0
        rps = ['🪨', '📄', '✂️']
        flip = [867086865768382494, 888125079710474280]
        if reaction.emoji in rps:
            emojis = rps
            prizes = [0, 50, -50]

            await ctx.message.clear_reactions()
            table = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
            msgs = ['Tie!', 'You win!', 'You lose!']
            usrmove = emojis.index(reaction.emoji)
            botmove = random.randint(0, 2)
            result = table[usrmove][botmove]
            await ctx.message.edit(embed=discord.Embed(
                title="Rockpaperscissor",
                description=
                f'{emojis[usrmove]} | {emojis[botmove]}\n{msgs[result]} {cash(prizes[result])}',
                color=db['color']))
            db['bal'][usrid] += prizes[result]

        elif reaction.emoji.id in flip:
            emojis = flip
            prizes = [30, -30]

            await ctx.message.clear_reactions()
            msgs = ['You win!', 'You lose!']
            usrmove = emojis.index(reaction.emoji.id)
            flip = random.randint(0, 1)
            if flip == usrmove:
                result = 0
            else:
                result = 1
            await ctx.message.edit(embed=discord.Embed(
                title="Flip",
                description=
                f'{self.bot.get_emoji(emojis[usrmove])} | {self.bot.get_emoji(emojis[flip])}\n{msgs[result]} {cash(prizes[result])}',
                color=db['color']))
            db['bal'][usrid] += prizes[result]

def setup(bot):
    bot.add_cog(Economy(bot))
