import discord
from discord.ext import commands

import random as rd
import signal
import json
import re

def timeout_handler(signum, frame):
    raise signal.ItimerError

config_filename = 'config.json'
with open(config_filename, 'r') as f:
    config = json.load(f)

token = config['token']

bot = commands.Bot(
    command_prefix='?',
    description='A cute, automated elf.'
)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):

    if ctx.message.author.nick is None:
        person_name = ctx.message.author.name
    else:
        person_name = ctx.message.author.nick

    greetings = "Hello, %s!" % person_name
    embed = discord.Embed(title=greetings, color=0xeee657)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    print(ctx.message.command)

@bot.command()
async def ooxx(ctx):
    await ctx.send("""Start a tic-tac-toe game.\nIt's still under construction now.""")

@bot.command()
async def calculate(ctx):
    formula = ' '.join(ctx.message.content.split(' ')[1:])
    if re.compile(r'[^0-9+\-*/.()!=\^&|<> ]').search(formula):
        ans_msg = "The formula must be consisted of only digits and operations '+-*/.()!=^&|<>'"
    else:
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, 0.001)
            ans = str(eval(formula))
        # except signal.ItimerError:
        except Exception as e:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            if (isinstance(e, signal.ItimerError)) or \
               (isinstance(e, MemoryError)):
                ans_msg = 'The question is too difficult, I can\'t solve it. QQ'
            else:
                ans_msg = 'The question is a little strange...'
        else:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            if len(ans) > 100:
                ans_msg = 'I have discovered a truly marvelous answer of your question, \nwhich this margin is too narrow to contain.'
            else:
                ans_msg = ans

    embed = discord.Embed(description=ans_msg, color=0xeee657)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    
    embed = discord.Embed(
        title="About Mercedes", 
        description="A cute, automated elf living in %s." % (ctx.guild), 
        color=0xeee657
    )
    
    # give info about you here
    embed.add_field(name="Author", value="Dashex#5966 / kikokushijo @ github")
    
    # Shows the number of servers the bot is member of.
    # embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):

    embed = discord.Embed(
        title="Commands of Mercedes", 
        description="A cute, automated elf living in %s.\nList of commands are:" \
                     % (ctx.guild), 
        color=0xeee657
    )
    embed.add_field(
        name="%sgreet" % bot.command_prefix, 
        value="Gives a greet message", 
        inline=False
    )
    embed.add_field(
        name="%sinfo" % bot.command_prefix, 
        value="Gives my info", 
        inline=False
    )
    embed.add_field(
        name="%shelp" % bot.command_prefix, 
        value="Gives this message", 
        inline=False
    )
    embed.add_field(
        name="%scalculate <formula>" % bot.command_prefix, 
        value="Help you calculate the formula", 
        inline=False
    )

    await ctx.send(embed=embed)

bot.run(token)