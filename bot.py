import discord
from discord.ext import commands

import random as rd
import json

config_filename = 'config.json'
with open(config_filename, 'r') as f:
    config = json.load(f)

token = config['token']

bot = commands.Bot(
    command_prefix='?',
    description='A cute, automated elf living in NTUGDRC.'
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
    print(ctx.guild)

@bot.command()
async def ooxx(ctx):
    await ctx.send("""Start a tic-tac-toe game.\nIt's still under construction now.""")

@bot.command()
async def info(ctx):
    
    embed = discord.Embed(
        title="NTUGDRC-ELF", 
        description="A cute, automated elf living in NTUGDRC.", 
        color=0xeee657
    )
    
    # give info about you here
    embed.add_field(name="Author", value="kikokushijo")
    
    # Shows the number of servers the bot is member of.
    # embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    # embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):

    embed = discord.Embed(
        title="NTUGDRC-ELF", 
        description="A cute, automated elf living in NTUGDRC. List of commands are:", 
        color=0xeee657
    )
    embed.add_field(
        name="%sgreet" % bot.command_prefix, 
        value="Gives a nice greet message", 
        inline=False
    )
    embed.add_field(
        name="%sinfo" % bot.command_prefix, 
        value="Gives a little info about the bot", 
        inline=False
    )
    embed.add_field(
        name="%shelp" % bot.command_prefix, 
        value="Gives this message", 
        inline=False
    )

    await ctx.send(embed=embed)

bot.run(token)