from typing import Union
import datetime
import disnake as discord
from disnake.ext import commands
from replit import db
import os


def Embed(msg: Union[commands.Context, discord.Interaction, discord.Message],
          description: str = '',
          title: str = '',
          fields: list = [],
          footer: dict = {},
          image: dict = {},
          image_url: str = None,
          thumbnail: dict = {},
          thumbnail_url: str = None,
          video: dict = {},
          video_url: str = None,
          author: dict = {},
          type: str = 'rich',
          url: str = '',
          timestamp: datetime.datetime = None,
          color: Union[discord.Colour, int] = None,
          colour: Union[discord.Colour, int] = None):
    return discord.Embed.from_dict({
        'title':
        title,
        'description':
        description,
        'footer':
        footer,
        'fields':
        fields,
        'image': {
            'url': image_url
        } if image_url else image,
        'thumbnail': {
            'url': thumbnail_url
        } if thumbnail_url else thumbnail,
        'video': {
            'url': video_url
        } if video_url else video,
        'author':
        author if author else {
            'name':
            msg.command.name.title() if
            (isinstance(msg, commands.Context) and msg.command) else msg.data.
            name.title() if isinstance(msg, discord.Interaction) else '',
            'icon_url':
            'https://cdn.discordapp.com/emojis/968444036354543626.webp?size=1024&quality=lossless'
        } if isinstance(msg, (commands.Context, discord.Interaction)) else {},
        'type':
        type,
        'timestamp':
        timestamp,
        'color':
        color if color else colour if colour else db['color'],
        'url':
        url
    })


async def Webhook(ctx):
    for webhook in (await ctx.channel.webhooks()):
        if webhook.user.id == ctx.bot.user.id and webhook.name == "Guffo Tupper":
            return webhook
    return (await ctx.channel.create_webhook(name="Guffo Tupper"))


def cog_files():
    return [
        filename[:-3].title() for filename in os.listdir('./cogs')
        if filename.endswith('.py') and filename[:-3].title() in db['cogs']
    ]
