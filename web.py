from flask import Flask, redirect, render_template, request
import logging
from threading import Thread
import disnake as discord

async def web(bot):
  appinfo = await bot.application_info()
  app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
    )

  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

  def help(command):
    return f'''[{command.name}{", " if any(command.aliases) else ""}{", ".join(command.aliases)}] {command.signature}

    {command.help if command.help else ""}

    {command.description if command.description else ""}'''.replace('\n\n', '\n')

  @app.route('/')
  def home():
    return render_template(
      'index.html',
      name = bot.user.name,
      avatar = bot.user.display_avatar.url,
      latency = int(bot.latency*1000),
      guilds = len(bot.guilds),
      cogs = bot.cogs,
      emojis = bot.emojis,
      description = '\n'.join([line for line in appinfo.description.split('\n') if not line.startswith('Doc: ')]).lstrip('\n'),
      url = request.base_url,
      help = help
    )

  @app.route("/invite")
  def invite():
    return redirect(
      discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(permissions=805579856), scopes=('applications.commands%20bot',)))

  @app.route("/server")
  def server():
    return redirect('https://discord.gg/KubGRbRKWXveeyZdqcjy')
  
  @app.route("/code")
  def code():
    return redirect(f'https://replit.com/@{appinfo.owner.name}/{bot.user.name}')
  
  @app.route("/code")
  def spin():
    return redirect(f'https://replit.com/@{appinfo.owner.name}/{bot.user.name}')

  def run():
    try:
      app.run(host='0.0.0.0', port=8080)
    except:
      return

  Thread(target=run).start()


def shutdown():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()