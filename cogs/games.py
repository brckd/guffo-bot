import disnake as discord
from disnake.ext import commands
from typing import List
import random
import utils

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Games(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def tictactoe(self, inter):
    '''
    Play TicTacToe

    Parameters
    ----------
    player2: invite another Player to Reversi
    '''
    await inter.send('Tic Tac Toe', view=TicTacToe())
  
  @commands.command(name='tictactoe')
  async def tictactoe2(self, ctx):
    '''
    Play TicTacToe

    Parameters
    ----------
    player2: invite another Player to Reversi
    '''
    await ctx.reply('Tic Tac Toe', view=TicTacToe())

  @commands.slash_command()
  async def kill(self, inter, victim: discord.Member):
    '''
    Kill Someone
    
    Parameters
    ----------
    victim: Who gets killed'''
    killer, = random.choices([inter.author.mention, '[Intentional Game Design]', 'Skill Issue'],[1,0.1,0.1],k=1)
    victim = victim.mention
    item = random.choice(['Sword', 'Magic', 'Nonsense', 'Console', 'Love', 'Art', 'Script Limit', 'Syntax Error', 'Nitro Scam', 'Anvil', 'Suspicious Soup', 'Lava', 'Impostor', 'Bread', 'Brick', 'BAH', 'YEE', 'Infinity Gauntlet'])
    mention = random.choice(['@Fanmod', '@Martin Magni', '@everyone', '@Fanbot'])
    reason = random.choice([f'pinging {mention}', f'publishing Drive Mad Kit {random.randint(0,100)}'+random.choice(['',f'on {killer}\'s account']),'giving them a pumpkin with curse of binding', 'correcting their grammar'])
    doing = random.choice(['','',f'whilst trying to escape {killer}', f'whilst fighting {killer}'])
    using = random.choice(['', f'using {item}'])
    msgs=[
      f'{victim} said <:yee:933058850565795920> in <#868127695530233876>',
      f'{victim} sent {random.sample(range(1, 9), 3)[::-1]} in <#841970221064781864>',
      f'{victim} got ejected, he was not the impostor',
      f'{victim} got ejected, he was the impostor',
      'Timeout! Infinite Loop?',
      f'{victim} was banned by {killer}',
      f'{victim} got to bored',
      f'{victim} got spam pinged {victim} {victim} {victim} {victim} {victim} {victim} {victim}',
      f'{victim} tried to steal {killer}\'s {item} but got caught by {mention}',
      f'{victim} starved whilst waiting for fancade 1.8',
      f'{killer} set {victim}\'s velocity to {random.randint(-1000000,1000000)}',
      f'{killer} got teleported to {random.randint(-1000000,1000000)}/{random.randint(-1000000,1000000)}/{random.randint(-1000000,1000000)}',
      f'{victim} lost his breath due to being too surprised',
      f'{victim} rage quitted whilst playing New Super Mario Bros. Wii',
      f'{victim} was banned by {killer} for {reason}',
      f'{killer} deamed of {reason} but then he realized that was not a dream',
      f'{victim} was banned by {killer} for {reason}',
      f'{victim} was killed by {killer} for {reason}',
      f'{killer} used {item} on {victim}',
      f'{victim} tried to eat {item}',
      f'{victim} stepped on {item} to hard',
      f'{victim} likes to swim in {item}',
      f'{victim} tried to mlg with a lava bucket',
      f'{victim} killed himself because of {killer} {reason}',
      f'{victim} was squashed by {killer} {using}',
      f'{victim} was squashed by a falling {item} {doing}',
      f'{victim} was shot by {killer} {using}',
      f'{victim} drowned {doing}',
      f'{victim} experienced kinetic energy {doing}',
      f'{victim} blew up',
      f'{victim} was blown up by {killer} {doing}',
      f'{victim} hit the ground too hard {doing}',
      f'{victim} fell from a high place',
      f'{victim} fell off a ladder',
      f'{victim} went up in flames {doing}',
      f'{victim} burned to death {doing}'
    ]
    await inter.send(embed=utils.Embed(inter, random.choice(msgs)))
    
def setup(bot):
  bot.add_cog(Games(bot))
