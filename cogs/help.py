import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help commands Is Now Online')

    @commands.command(name = "help")
    async def help(self,ctx):
        helpEmbed = discord.Embed(title = 'Ticket Help',description = 'Ticket/Question Help',inline = False,colour = 0xa60909)
        helpEmbed.add_field(name = '!ticket',value = 'Parameters: <Question Template>',inline = False)
        await ctx.send(embed = helpEmbed)
		
    #Help Command for the adminstator for the announcements
    @commands.command(name = 'helpAdmin')
    @commands.has_permissions(administrator = True)
    async def helpAdmin(self,ctx): 
        await ctx.invoke(self.client.get_command('helpA'))
        await ctx.invoke(self.client.get_command('helpR'))
        await ctx.invoke(self.client.get_command('helpT'))


    @commands.command(name = 'helpA')
    @commands.has_permissions(administrator=True)
    async def helpA(self,ctx):
        #Create and embed and add fields to it which will list all the functions
        helpEmbed = discord.Embed(title = 'Announcement Help',description = 'Bot Announcement commands',inline = False,colour = 0xa60909)
        helpEmbed.add_field(name = '!listA',value = 'Provides the List of announcements',inline = False)
        helpEmbed.add_field(name = '!delA',value = 'Deletes an Announcement\nParameters: <Index of the announcement>',inline = False)
        helpEmbed.add_field(name = '!addA',value = 'Adds an announcement to the Queue\nParameters: <year> <month> <day> <hour> <minute> #<channel Name> <Message>',inline = False)
        helpEmbed.add_field(name = '!editA',value = 'Edits an Announcement\nParameters: <Announcement Index Number> <Same Parameters as AddA>',inline = False)
        helpEmbed.add_field(name ='!startA',value = 'Start the loop back up for the announcement function where the bot can post announcements again',inline = False)
        helpEmbed.add_field(name = '!stopA',value = 'Stops the Loop to the announcement function which will prevent announcements from posting',inline = False)
        await ctx.send(embed = helpEmbed)

    @commands.command(name = 'helpR')
    @commands.has_permissions(administrator = True)
    async def helpR(self,ctx):   
        helpEmbed = discord.Embed(title = 'Roles Help',description = 'Role Commands',inline = False,colour = 0xa60909)
        helpEmbed.add_field(name = '!addR',value = 'Will add the interactive Select Where users can select and add Roles',inline = False)
        await ctx.send(embed = helpEmbed)

    @commands.command(name = 'helpT')
    async def helpT(self,ctx):
        helpEmbed = discord.Embed(title = 'Ticket Help',description = 'Ticket/Question Help',inline = False,colour = 0xa60909)
        helpEmbed.add_field(name = '!ticket',value = 'Parameters: <Question Template>',inline = False)
        helpEmbed.add_field(name = '!faq',value = 'Shows the list of Frequently/Previously Asked Questions',inline = False)
        await ctx.send(embed = helpEmbed)

    @helpA.error
    @help.error
    @helpR.error
    @helpT.error
    async def help_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have Permision for this command")

def setup(client):
    client.add_cog(help(client))

