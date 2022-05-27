import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import datetime
from datetime import datetime
from pytz import timezone
import math
import json

def time(year,month,day, hour,minutes):
	timeZone= timezone('America/New_York')
	timeNow =datetime.now(timeZone)
	timeFuture = datetime(int(year), int(month), int(day), int(hour), int(minutes))
	# timeFuture = datetime(int(year), int(month), int(day), int(hour), int(minutes))
	seconds_int = int(math.ceil( (timeFuture - timeNow.replace(tzinfo=None)).total_seconds()))
	if seconds_int<0:
		return -1
	else:
		return seconds_int

class countdown(commands.Cog):
	def __init__(self,client):
		self.client = client
		
	@commands.Cog.listener()
	async def on_ready(self):
		print('Countdown is now online')
		self.timer.start()

	@tasks.loop(seconds=10.0)
	async def timer(self):
		data  = json.load(open("./cogs/JSON/countdown.json"))
		if len(data) ==0:
			return
		else:
			for x in range (0,len(data)):
				seconds = time(int(data[x]['year']),int(data[x]['month']),int(data[x]['day']),int(data[x]['hour']),int(data[x]['minutes']))
				if seconds > 0:
					day = seconds // (24 * 3600)
					seconds = seconds % (24 * 3600)
					hour = seconds // 3600
					seconds %= 3600
					minutes = seconds // 60
					seconds %= 60
					channel = self.client.get_channel(data[x]['channelID'])
					countdownEmbed = discord.Embed(title = data[x]['text'],description = '',inline = False,colour = 0xa60909)
					countdownEmbed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/865473459491307532/971651126518759474/Gryphon_basic.png")
					countdownEmbed.add_field(name="Days",value = int(day),inline = True)
					countdownEmbed.add_field(name="Hours",value = int(hour),inline=True)
					countdownEmbed.add_field(name="---------------------",value = "--------------------",inline=False)
					countdownEmbed.add_field(name = "Minutes",value = int(minutes),inline = True)
					countdownEmbed.add_field(name = "Seconds",value = int(seconds),inline = True)
					# print(channel)
					messageID = await channel.fetch_message(data[x]['messageID'])
					# print(messageID)
					await messageID.edit(embed = countdownEmbed)

	@commands.command(name = 'countdown')
	async def countdown(self,ctx,year,month,day,hour,minutes,*,arg):
		await ctx.message.delete()
		seconds = float(time(int(year), int(month), int(day), int(hour), int(minutes)))
		# await ctx.send(str(seconds))
		if seconds < 0:
			await ctx.send('Unable to add Message due to invalid timestamp')
		else:
			dayCalc = seconds // (24 * 3600)
			seconds = seconds % (24 * 3600)
			hourCalc = seconds // 3600
			seconds %= 3600
			minutesCalc = seconds // 60
			seconds %= 60
			countdownEmbed = discord.Embed(title = arg,description = '',inline = False,colour = 0xa60909)
			countdownEmbed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/865473459491307532/971651126518759474/Gryphon_basic.png")
			countdownEmbed.add_field(name="Days",value = int(dayCalc),inline = True)
			countdownEmbed.add_field(name="Hours",value = int(hourCalc),inline=True)
			countdownEmbed.add_field(name="---------------------",value = "--------------------",inline=False)
			countdownEmbed.add_field(name="Minutes",value = int(minutesCalc),inline=True)
			countdownEmbed.add_field(name = "Seconds",value = int(seconds),inline = True)
			message = await ctx.send(embed =countdownEmbed)
			with open ('./cogs/JSON/countdown.json') as json_file:
				data = json.load(json_file)
				announcements ={'text':arg,'year':year,'month':month,'day':day,'hour':hour,'minutes':minutes,'messageID':message.id,'channelID':message.channel.id}
				data.append(announcements)
			with open('./cogs/JSON/countdown.json','w') as j:
				json.dump(data,j,indent = 6)
			# await ctx.send("Done countdown Have been Saved")
		
def setup(client):
    client.add_cog(countdown(client))