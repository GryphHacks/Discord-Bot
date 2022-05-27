import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord_components import DiscordComponents
# from keep_alive import keep_alive


load_dotenv()
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)
client.remove_command('help')

    
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name="VSCode"))
  print('logged in as')
  print(client.user.name)
  print(client.user.id)
  print('-----')
  DiscordComponents(client)


@client.command()
async def load(ctx,extention):
  client.load_extension(f'cogs.{extention}')
  await ctx.send('Done')

@client.command()
async def unload(ctx,extention):
  client.unload_extension(f'cogs.{extention}')
  await ctx.send('Done')

@client.command()
async def rerun(ctx,extention):
  client.unload_extension(f'cogs.{extention}')
  client.load_extension(f'cogs.{extention}')
  await ctx.send('Done unload and load ')


@client.command()
async def unloadAll(ctx):
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.unload_extension(f'cogs.{filename[:-3]}')
  await ctx.send('Done')


@client.command()
async def loadAll(ctx):
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
  await ctx.send('Done')

  
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# keep_alive()

client.run(os.getenv("TOKEN2"))

	