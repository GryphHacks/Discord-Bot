import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import datetime
from datetime import datetime
from pytz import timezone
import math
import json

def socials(linkedin,github,twitter,email,quora,discord,gryphslack):
	social = ""
	if(linkedin!=""):
		social += "<:linkedin:976920403094155325> Linkedin: " + linkedin + "\n"
	if twitter!="":
		social += "<:twitter:976925038802534451> Twitter: " + twitter + "\n"
	if github!="":
		social  += "<:github:976930007400189983> Github: " + github + "\n"
	if email!="":
		social  += ":envelope: Email: " + email + "\n"
	if quora!="":
		social  += "<:quora:976926258493534228> Quora: " + quora + "\n"
	if discord!="":
		social  += "<:discord:976926212469444658> Discord: " + discord + "\n"
	if gryphslack!="":
		social  += "<:slack:976926009439965184> Gryphslack: " + gryphslack + "\n"
	return social

class contact(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Contacts is now online")

	@commands.command(name = 'contacts')
	async def contacts(self,ctx):
		await ctx.message.delete()
		data= json.load(open("./cogs/JSON/contacts.json"))
		for contact in data:
			countdownEmbed = discord.Embed(title =contact['name'] ,description = contact['role'],inline = False,colour = 0xa60909)
			countdownEmbed.add_field(name="About "+contact['name'],value = contact['description'],inline=False)
			social = socials(contact['social']['linkedin'],contact['social']['github'],contact['social']['twitter'],contact['social']['email'],contact['social']['quora'],contact['social']['discord'],contact['social']['gryphslack'])
			countdownEmbed.set_thumbnail(url =contact['image'])
			if(social!=""):
				countdownEmbed.add_field(name = "Check Them Out Here",value = social,inline = False)
			await ctx.send(embed = countdownEmbed)
		
	
def setup(client):
    client.add_cog(contact(client))