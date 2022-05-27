import discord
from discord.ext import commands
import json
from discord.ext import tasks
counter=0
msg_id=0 
import time
class ticket(commands.Cog):
    global checkFaq
    checkFaq=False
    global number
    number =0
    def __init__(self,client):
        self.client = client
        self.counter = counter
    @commands.Cog.listener()
    async def on_ready(self):
        print('Announcement Is Online')
        self.loop.start()
    
    @commands.command(name = 'question')
    @commands.cooldown(1,10,commands.BucketType.user)
    async def Question(self,ctx,*,arg):
        if ctx.channel.name != "ask-a-mentor":
		        await ctx.send("Any Question Should be directed to the <#890155931785121792> channel instead")
		        return
        await ctx.message.delete()
        emoji = ['❎','💁','✅']
        QuestionID = 890155968044871721
        channel = self.client.get_channel(QuestionID)
        global counter
        counter+=1

        await ctx.author.send("Thanks your message has been sent your ticket Number is {} a mentor will be with you shortly please watch your DM's for a message from a mentor".format(counter))
        QuestionEmbed = discord.Embed(title = "Ticket Number: {}".format(counter),description ="Answering Question",color = 0xFFFF00)
        QuestionEmbed.add_field(name = 'Discord Username:',value = ctx.author.mention,inline = False)
        QuestionEmbed.add_field(name = 'Question Asked:',value = arg,inline = False)
        message = await channel.send(embed = QuestionEmbed)
        for x in range(0,len(emoji)):
            await message.add_reaction(emoji[x])
        with open ('./cogs/JSON/tickets.json') as json_file:
            data = json.load(json_file)
            tickets ={
                'message_id':message.id,
                'emojiNotAnswered':emoji[0],
                'emojiCurrentlyAnswered':emoji[1],
                'emojiAnswered':emoji[2],
                'ticketNumber':counter,
                'question':arg,
                
            }
            data.append(tickets)
        
        with open('./cogs/JSON/tickets.json','w') as j:
            json.dump(data,j,indent = 4)
                
            
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        RawReactionChannelID = 890155968044871721
        channel = self.client.get_channel(RawReactionChannelID)
        def wrapper(context):
            def check_msg(message):
                return context.author == message.author
            return check_msg
        if payload.member.bot:
            pass
        else:
            with open('./cogs/JSON/tickets.json') as ticket:
                ticketData = json.load(ticket)
                for i in range (len(ticketData)):
                     
                    if ticketData[i]['emojiCurrentlyAnswered'] == payload.emoji.name and ticketData[i]['message_id'] == payload.message_id:
                        message = await channel.fetch_message(payload.message_id)
                        await message.edit(f'Question Being Answered by {payload.member.mention}')
                    elif ticketData[i]['emojiAnswered'] == payload.emoji.name and ticketData[i]['message_id'] == payload.message_id:
                        message = await channel.fetch_message(payload.message_id)
                        intTicketNumber = int(ticketData[i]['ticketNumber'])
                        await message.edit(f'Ticket Number {str(intTicketNumber)} Has Been Answered by{payload.member.mention}')
                        await payload.member.send("Enter The Question You Answered")
                        msg1 = await self.client.wait_for('message',timeout=300, check=lambda message: message.author == payload.member and isinstance(message.channel, discord.DMChannel))
                        
                        await payload.member.send(f'Done You Have Entered "{msg1.content}".')
                        await payload.member.send("Enter the Answer to the Question")
                        msg2 = await self.client.wait_for('message',timeout=300, check=lambda message: message.author == payload.member and isinstance(message.channel, discord.DMChannel))
                        await payload.member.send(f'Done You Have Entered "{msg2.content}".')

                        with open ('./cogs/JSON/FAQ.json') as  FAQFile:
                            data = json.load(FAQFile)
                            Question = {
                                'Question':msg1.content,
                                'Answer':msg2.content,
                            }
                            data.append(Question)
                        with open('./cogs/JSON/FAQ.json','w') as FAQWrite:
                            json.dump(data,FAQWrite,indent = 4)
                        ticketData.pop(i)
                        with open('./cogs/JSON/tickets.json','w') as ticketWrite:
                            json.dump(ticketData,ticketWrite,indent = 4)

                    elif ticketData[i]['emojiNotAnswered'] == payload.emoji.name and ticketData[i]['message_id'] == payload.message_id:
                        message = await channel.fetch_message(payload.message_id)
                        await message.edit(f'Question Has been Already Answered Previously or Question is not relavant deemed by {payload.member.mention}')
                        ticketData.pop(i)
                        with open('./cogs/JSON/tickets.json','w') as ticketWrite:
                            json.dump(ticketData,ticketWrite,indent = 4)
						
					
						
						
                        
    
    @commands.command(name = 'faq')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def faq(self,ctx):
        await ctx.message.delete()
        time.sleep(1)
        FAQEmbed = discord.Embed(title = 'Frequently/Previously Asked Questions',description = 'A List of Previously Asked Question in the Ticket System')
        with open('./cogs/JSON/FAQ.json') as FAQFile:
            FAQData  = json.load(FAQFile)
            for x in FAQData:
                FAQEmbed.add_field(name = 'Question: {}'.format(x['Question']),value = 'Answer: {}'.format(x['Answer']),inline = False)
        global message
        message = await ctx.send(embed = FAQEmbed)
        print(message.id)
        global checkFaq
        checkFaq = True

    @tasks.loop(minutes=10.0)
    async def loop(self):
        channel = self.client.get_channel(890155895655383060)
        messageID = await channel.fetch_message(976336454164828171)
        FAQEmbed = discord.Embed(title = 'Frequently/Previously Asked Questions',description = 'A List of Previously Asked Question in the Ticket System')
        with open('./cogs/JSON/FAQ.json') as FAQFile:
              FAQData  = json.load(FAQFile)
              for x in FAQData:
                  FAQEmbed.add_field(name = 'Question: {}'.format(x['Question']),value = 'Answer: {}'.format(x['Answer']),inline = False)
                  
				  
        await messageID.edit(embed = FAQEmbed)
       
    # @commands.command(name = 'channelT')
    # async def channelTickets(self,ctx,channel: discord.TextChannel):
    #     global channelID
    #     channelID = channel.id
    #     return channelID

def setup(client):
    client.add_cog(ticket(client))
