import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import datetime
from datetime import datetime
from pytz import timezone
import math
import json

#time function used to calulate the time now and the time in the future and converts them into seconds
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

class announcemnet(commands.Cog):
    def __init__(self,client):
        self.client = client
        
#once bot is ready it will log on and the task will start
    @commands.Cog.listener()
    async def on_ready(self):
        print('Announcement Is Online')
        self.timer.start()

    #Will loop through the whole list and then add up all the times in the announcements
    @tasks.loop(seconds=5.0)
    async def timer(self):
        # print('start')
        #Read the data and checks if there is content in the file
        data  = json.load(open("./cogs/JSON/announcements.json"))
        if len(data) ==0:
                return
        else:
            #Move through the data in the list to check if there is an announcement which will calulate the seconds and then will post the announcemnet at the desired time
            # if the seconds are greater than 0 and will also check if the time is to short
            for x in range (0,len(data)):
                seconds = time(int(data[x]['year']),int(data[x]['month']),int(data[x]['day']),int(data[x]['hour']),int(data[x]['minutes']))
                if seconds > 0:
                    #cimter will start and will wait until the desired time after it will post the message in the desired channel at the desired time
                        print('Timer Will Now start and announcements will be posted at desired time')
                        await asyncio.sleep(seconds)
                        channel = self.client.get_channel(int(data[x]['channelID']))
                        print("Done")
                        await channel.send(data[x]['text'])
                        return
                # else:
                #       # print("Time Too short")

                
                
     

    #this command is used to add announcements to the json file which can be used later many uses and can only be used by a a person with the admin permission
    @commands.command(name = 'addA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def addAnnouncement(self,ctx,year,month,day,hour,minutes,channel:discord.TextChannel,*,arg):

        #checks if the timestamp is too short if not then the announcement will be added to the json file
        seconds = time(int(year), int(month), int(day), int(hour), int(minutes))
        if seconds < 0:
            await ctx.send('Unable to add Message due to invalid timestamp')
        else:
            with open ('./cogs/JSON/announcements.json') as json_file:
                data = json.load(json_file)
                announcements ={'text':arg,'year':year,'month':month,'day':day,'hour':hour,'minutes':minutes,'channelID':channel.id,}
                data.append(announcements)
            with open('./cogs/JSON/announcements.json','w') as j:
                json.dump(data,j,indent = 6)
            await ctx.send("Done announcement Have been Saved")
            
                    
    # This command will list all of the announcements currently in the json file
    @commands.command(name = 'listA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def listAnnounceent(self,ctx):
        await ctx.message.delete()
        counter = 0
        announcementL = discord.Embed(title = 'Announcements',description = ' List of Announcements')
        with open('./cogs/JSON/announcements.json') as ticket:
            announcements = json.load(ticket)
            for x in announcements:
                counter+=1
                announcementL.add_field(name = f'Announcements {str(counter)}',value = 'Announcement: {}\nTime:\nYear:{}\nMonth:{}\nDay:{}\nHour:{}\nMinute:{}'.format(x['text'],x['year'],x['month'],x['day'],x['hour'],x['minutes']),inline=False)
        await ctx.send(embed = announcementL)



    #This command is used to delete a certain number of annoucements based on argument given by the user
    @commands.command('delA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    # @commands.has_any_role()
    async def deleteAnnouncements(self,ctx,arg):
        await ctx.message.delete()
        #loads the json file and checks if there are any announcements
        obj  = json.load(open("./cogs/JSON/announcements.json"))

        if len(obj) == 0:
            await ctx.send("You have no announcements to delete")
        #checks if user has given an index greater than the desired number    
        elif int(arg) > len(obj):
             await ctx.invoke(self.client.get_command('listA'))
             await ctx.send("Number is out of index please enter a number from 1-{}".format(len(obj)))
        else:
            #object gets popped from the list 
            for i in  range(0,len(obj)):
                if i == int(arg)-1:
                    obj.pop(i)
                    break
            # Output the updated file with pretty JSON                                      
            open("./cogs/JSON/announcements.json", "w").write(
                json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
            )
            await ctx.invoke(self.client.get_command('listA'))
            self.timer.restart()
       


    @commands.command(name = 'editA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def editAnnouncement(self,ctx,num,year,month,day,hour,minutes,channel:discord.TextChannel,*,arg):
        await ctx.message.delete()
        index,data,seconds = int(num)-1,json.load(open("./cogs/announcements.json")),time(int(year), int(month), int(day), int(hour), int(minutes))
        if len(data) == 0:
            await ctx.send("Your Have no announcements to edit")
        elif index >= len(data):
            await ctx.send("Index for edit message is too large please try again")
        elif seconds <0:
            await ctx.send('Timestamp too short try again')
        else:
            data[index]['year'],data[index]['month'],data[index]['day'],data[index]['hour'],data[index]['minutes'],data[index]['channelID'],data[index]['text']  = year,month,day,hour,minutes,channel.id,arg
            with open('./cogs/JSON/announcements.json','w') as j:
                json.dump(data,j,indent = 6)
            await ctx.send("Done announcement Have been Saved")
            await ctx.invoke(self.client.get_command('listA'))
            self.timer.restart()




    @commands.command(name = 'setupA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def addAnnouncementCategory(self,ctx):
       await ctx.message.delete()
       categoryA = await ctx.guild.create_category('Announcements')
       channel =  await ctx.message.guild.create_text_channel('Announcement',category = categoryA)
       f = open("./cogs/setupA.txt", "w")
       f.write(str(channel.id))
       f.close()


    #stop the loop which can be used incase of an emergency
    @commands.command(name = 'stopA')
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator = True)
    async def stop(self,ctx):
        await ctx.message.delete()
        self.timer.stop()
        await ctx.send(f'Done Timer has been stopped by {ctx.author.mention}and Announcements will not be posted Remember to Enable the timer again')
    #starts the loop back up when called

    @commands.command(name = 'startA')
    @commands.has_permissions(administrator = True)
    async def start(self,ctx):
        self.timer.start()
        await ctx.send(f'Done Timer has been restarted by {ctx.author.mention} and announcements will start to post again')

     #Error Checking   
    @listAnnounceent.error
    @editAnnouncement.error
    @addAnnouncement.error
    @deleteAnnouncements.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Do not have permissons for this command.")
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("You Are missing one or more Arguments")
        if isinstance(error,commands.TooManyArguments):
            await ctx.send('You Have too many Arguments in Place')
        if isinstance(error,commands.CommandNotFound):
            await ctx.send('That Command Does not exist')

def setup(client):
    client.add_cog(announcemnet(client))