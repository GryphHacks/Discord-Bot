import discord
from discord.ext import commands

yearRoles = ['1st Year','2nd Year','3rd Year','4th Year','5th Year +','Alumni']
pronounRoles = ['He/Him','She/Her','They/Them','Other']

class createRolesCog(commands.Cog):

    def __init__(self,client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('CreateRoles is now online')

    @commands.command(name = 'serverRole')
    # @commands.has_any_role('Staff')
    async def loadRoles(self,ctx):
        perms = discord.Permissions(send_messages=True, read_messages=True)
        for x in yearRoles:
            await ctx.guild.create_role(name = x,permissions = perms)
        for x in pronounRoles:
            await ctx.guild.create_role(name = x,permissions = perms) 

   


def setup(client):
    client.add_cog(createRolesCog(client))