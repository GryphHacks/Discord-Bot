import discord
from discord.ext import commands
import json
import smtplib, ssl
import os
import random
import string
import time
import asyncio
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
port = 465
smtp_server_domain_name = "smtp.gmail.com"
sender_mail = "gryphhacks-development@socis.ca"
password = os.getenv("EMAIL_PASSWORD")
ssl_context = ssl.create_default_context()
service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
service.login(sender_mail, password) 
def send( emails, content,subject):
		result = service.sendmail(sender_mail, emails, f"Subject: {subject}\n{content}")
class verify(commands.Cog):
	def __init__(self,client):
		self.client = client
		print('hi')



	@commands.Cog.listener()
	async def on_ready(self):
		print('Verify is online and Email has been Logged in ')
		port = 465
		smtp_server_domain_name = "smtp.gmail.com"
		sender_mail = os.getenv('EMAIL')
		password = os.getenv('EMAIL_PASSWORD')
		ssl_context = ssl.create_default_context()
		service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
		service.login(sender_mail, password) 


	@commands.command(name = 'verify')
	async def sendVerify(self,ctx):
		await ctx.message.delete()
		await ctx.send("Click on the Button and the Bot will ask you to Verify yourself Using your Email + Verification Code.If you haven't registered yet Register here: https://7zz0jrazbwj.typeform.com/to/v9Msd4Sj?typeform-source=gryphhacks.com", components=[Button(label="Click here to Verify yourself",style = 1)])

	@commands.Cog.listener()
	async def on_button_click(self,interaction):
		await interaction.respond(type=6)
		await interaction.author.send("Are you Verifying yourself as a mentor or a hacker please type 1 for mentor type 2 for hacker")
		try:
			msg = await self.client.wait_for('message',timeout=300, check=lambda message: message.author == interaction.author and isinstance(message.channel, discord.DMChannel))
		except asyncio.TimeoutError:
			await interaction.author.send("Reply from user timed out please try again")
			return
		with open("./cogs/JSON/checkedIn.txt", "r") as file: 
			words = file.read().splitlines()
	
		
		await interaction.author.send("Enter The Email you Register With")
		try:
			msg1 = await self.client.wait_for('message',timeout=300, check=lambda message: message.author == interaction.author and isinstance(message.channel, discord.DMChannel))
		except asyncio.TimeoutError:
			await interaction.author.send("Reply from user timed out please try again")
			return
		
		if msg1.content in words:
			await interaction.author.send("Email already Exists Please go back to the discord server again and click on the button and Try again with a different Email")
			return;
		await interaction.author.send("Please Enter the Verifcation Code that you were given")
		try:
			msg2 = await self.client.wait_for('message',timeout=300, check=lambda message: message.author == interaction.author and isinstance(message.channel, discord.DMChannel))
		except asyncio.TimeoutError:
			await interaction.author.send("Reply from user timed out please try again")
			return
		if msg.content == "1":
			print("Mentor")
			with open('./cogs/JSON/mentors.json') as json_file:
			    data = json.load(json_file)
			for thing in data:
				if thing['email'].lower() == msg1.content.lower() and thing['ID']==msg2.content:
					await interaction.author.send("Thanks for verifying you will be given the Mentor role enjoy the Hackathon")
					with open("./cogs/JSON/checkedIn.txt","a") as f:
						f.write(str(thing['email'])+"\n")
					member = interaction.guild.get_member(interaction.user.id)
					role = discord.utils.get(member.guild.roles,name ='Mentor')
					await member.add_roles(role)
					return;
			else:
				await interaction.author.send("Incorrect Email or Verification Code if you haven't registered please go to the typeform\n https://7zz0jrazbwj.typeform.com/to/Ebv9KUyq?typeform-source=gryphhacks.com\nOnce you've recieved an email please try again on the discord server once more")
				return
		elif msg.content =="2":
			print("Hacker")
			with open('./cogs/JSON/hackers.json') as json_file:
			    data = json.load(json_file)
			for thing in data:
				if thing['email'].lower() == msg1.content.lower() and thing['ID']==msg2.content:
					await interaction.author.send("Thanks for verifying you will be given the Hacker role enjoy the Hackathon")
					with open("./cogs/JSON/checkedIn.txt","a") as f:
						f.write(str(thing['email'])+"\n")
					member = interaction.guild.get_member(interaction.user.id)
					role = discord.utils.get(member.guild.roles,name ='Hacker')
					await member.add_roles(role)  
					
					return;
			else:
				await interaction.author.send("Incorrect Email or Verification Code if you haven't registered please go to the typeform\n https://7zz0jrazbwj.typeform.com/to/v9Msd4Sj?typeform-source=gryphhacks.com.\nOnce you've recieved an email please try again on the discord server once more")
				return
		else:
			await interaction.author.send("Invalid Choice for Hacker/Mentor please go back to the discord server and click on the button to verify yourself once again")
			return
			


	@commands.command(name = 'generateHackers')
	async def generateHackers(self,ctx):
		afile = open("./cogs/JSON/hackers.txt","r")
		file_contents = afile.read()
		contents_split = file_contents.splitlines()
		characters = string.ascii_letters + string.digits 
		listdict = []
		for i in range(len(contents_split)):
	
			ID2 = ''.join(random.choice(characters) for i in range(8))
			thisdict = {
			'num':i+1,	
			'email':contents_split[i],
			'ID':ID2
			}
			listdict.append(thisdict)
		# await ctx.send(str(listdict))
		with open('./cogs/JSON/hackers.json', 'w') as fp:
			json.dump(listdict, fp,indent=4)	

	@commands.command(name = 'generateMentors')
	async def generateMentors(self,ctx):
		afile = open("./cogs/JSON/mentors.txt","r")
		file_contents = afile.read()
		contents_split = file_contents.splitlines()
		characters = string.ascii_letters + string.digits 
		listdict = []
		for i in range(len(contents_split)):
			
			ID2 = ''.join(random.choice(characters) for i in range(8))
			thisdict = {
			'email':contents_split[i],
			'ID':ID2
			}
			listdict.append(thisdict)
		await ctx.send(str(listdict))
		with open('./cogs/JSON/mentors.json', 'w') as fp:
			json.dump(listdict, fp,indent=4)	




			
	@commands.command(name = 'sendHackers')
	async def sendHackers(self,ctx,range1,range2):
		with open('./cogs/JSON/hackers.json') as json_file:
		    data = json.load(json_file)	
		for i in range(int(range1),int(range2)):
			content = "Hey Hackers!\n\nThank you for your patience and for applying to GryphHacks 2022! Round 2 applications have officially been closed, and all emails will be sent out within the hour. We can't wait to see your amazing hacks this weekend! Before the weekend of the hackathon, there are a couple more steps!\nFirst, make sure you've registered for our Devpost, and join our discord server! Both of them are linked at the bottom of this email! Make sure all your teammates are signed up on devpost and that they're present in the server as well. Important updates and announcements will be posted there!\n\nMake sure to join the Discord server with the discord tag you provided when you first signed up!\n\nFeel free to follow us on our socials, to stay up to date and maybe see some sneak peeks! Our schedule will be released on our site soon,  and checkout our prizes on our Devpost!\n\nGryphHacks 2022 Discord Server: https://discord.gg/EQHarZfqnh\nGryphHacks 2022 Devpost: https://gryphhacks-2022.devpost.com/\n\nYour Discord verification code is: \""+data[i]['ID']+"\"\nUse this code to verify yourself and receive the Hacker role within our GryphHacks Discord server. See you in there! \n\nHappy Hacking,\n\nThe GryphHacks Team "
			send(str(data[i]['email']),content,"Acceptance + Verification Email from Discord bot")
			time.sleep(2)
		await ctx.send("Done Hacker Emails Have been Sent to users ")

	@commands.command(name = 'sendMentors')
	async def sendMentors(self,ctx,range1,range2):	
		with open('./cogs/JSON/mentors.json') as json_file:
		    data = json.load(json_file)	
		for i in range(int(range1),int(range2)):
			content = "Acceptance + Verification Email from Discord bot\n\nHey Mentors! \n\nThank you for waiting patiently! \nWe've got T-3 days till our event kicks off! To ensure that mentors are always present throughout the hacking period, please sign up for a minimum of 2, to a maximum of 4 different shifts, on the following spreadsheet!\nhttps://docs.google.com/spreadsheets/d/1zuDkof7N0qbAoxvvQ-Ve9Mo636CPnX043e69WivllyE/edit#gid=0\nFill out your name, your area of specialization (what languages you're familiar with) and any small crucial details you would like us to know in the notes section!\n\nOnce you have been verified, you will gain access to the Mentor Category on the discord server!\nIf you haven't joined already, please do so:  https://discord.gg/EQHarZfqnh\n\nWe appreciate the help, and will distribute Mentor Appreciation Certificates after our event accordingly.\n\nThis email also contains your verification code, at the very bottom! \n\nYour verification code is: \""+data[i]['ID']+ "\"\nUse this code to verify yourself and receive the Mentor role within our GryphHacks Discord server. See you in there!\n\nHappy Hacking,\nThe GryphHacks Team"
			send(str(data[i]['email']),content,"Acceptance + Verification Email from Discord bot")
			await ctx.send("Done Sent to "+ str(data[i]['email']))
			time.sleep(1)
		await ctx.send("Done MentorEmails Have been Sent to users ")
			
		
	

def setup(client):
    client.add_cog(verify(client))