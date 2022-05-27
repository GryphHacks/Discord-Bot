import discord
from discord.ext import commands
from discord.ext import tasks
import json

class schedule(commands.Cog):
	def __init__(self,client):
		self.client = client
		
	@commands.Cog.listener()
	async def on_ready(self):
		print('Schedule is now online')

	@commands.command(name = "schedule")
	async def schedule(self,ctx):

		data= json.load(open("./cogs/JSON/schedule.json"))
		for i in range(len(data)):
			scheduleEmbed = discord.Embed(title = data[i]['date'],description = ' Schedule of Events (Note Times Are Written in EDT)',inline = False,colour = 0xa60909)
			# await ctx.send(embed = scheduleEmbed)
			for x in range(len(data[i]['events'])):
				if data[i]['events'][x]['start_date']!="" and data[i]['events'][x]['end_date']=="":
					string = data[i]['events'][x]['start_date'] +" "+ data[i]['events'][x]['event_name']
				else:
					string = data[i]['events'][x]['start_date'] + " - " +data[i]['events'][x]['end_date'] + " "+data[i]['events'][x]['event_name']
				string2 = data[i]['events'][x]['event_description']
				scheduleEmbed.add_field(name=string,value ="```"+string2+"```" ,inline = False)
			await ctx.send(embed = scheduleEmbed)

		
		
def setup(client):
    client.add_cog(schedule(client))