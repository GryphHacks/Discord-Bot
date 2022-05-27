import discord
from discord.ext import commands
from discord_components import  Select, SelectOption


#List of Roles and Emoji
yearRoles = ['1st Year','2nd Year','3rd Year','4th Year','5th Year +','Alumni','High School']
pronounRoles = ['He/Him','She/Her','They/Them','Other']

class TestCog(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    #Listener which will say that the cog is ready in the bot
    @commands.Cog.listener()
    async def on_ready(self):
            print('Roles is online')
            
    #Listener which will tell if a member has joined and will auto add roles if needed
    # @commands.Cog.listener()
    # async def on_member_join(self,member):
    #     role = discord.utils.get(member.guild.roles,name ='Hacker')
    #     await member.add_roles(role)
        
    

    @commands.command(name = "addR")
    # @commands.has_role('Staff')
    @commands.has_permissions(administrator=True)
    async def addRoles(self,ctx):
        await ctx.message.delete() 
        await ctx.send("Hello, Please Select Your Year of study",
            components = [
                Select(placeholder="Select Your Year Of Study!", options=[
				SelectOption(label=yearRoles[0], value=yearRoles[0]),	
                SelectOption(label=yearRoles[1], value=yearRoles[1]), 
                SelectOption(label=yearRoles[2], value=yearRoles[2]),
                SelectOption(label=yearRoles[3], value=yearRoles[3]),
                SelectOption(label=yearRoles[4], value=yearRoles[4]),
                SelectOption(label=yearRoles[5], value=yearRoles[5]),
                SelectOption(label=yearRoles[6], value=yearRoles[6])])
            ]
        )

        await ctx.send( "Hello, Please Select Your Pronoun",
            components = [
                Select(placeholder="Pronoun!", options=[
                SelectOption(label=pronounRoles[0], value=pronounRoles[0]), 
                SelectOption(label=pronounRoles[1], value=pronounRoles[1]),
                SelectOption(label=pronounRoles[2], value=pronounRoles[2]),
                SelectOption(label=pronounRoles[3], value=pronounRoles[3]),
               ])
            ]
        ) 
    
    @commands.Cog.listener()
    async def on_select_option(self,interaction):
        await interaction.respond(type=6)
        member = interaction.guild.get_member(interaction.user.id)
        role = discord.utils.get(interaction.guild.roles)   
        if interaction.component[0].value in yearRoles:
          roles = member.roles
          print(roles)
          role_names = [role.name for role in roles]
          checkYear =  any(item in role_names for item in yearRoles)
          if checkYear is True:
            checker = list(set(role_names) & set(yearRoles))
            print(checker)
            role = discord.utils.get(interaction.guild.roles, name=checker[0])
            await member.remove_roles(role)
          for x in range(0,len(yearRoles)):
            if interaction.component[0].value == yearRoles[x]:
                role = discord.utils.get(interaction.guild.roles, name=yearRoles[x])
                await member.add_roles(role)  

        else:
          role = discord.utils.get(interaction.guild.roles)
          roles = member.roles
          print(roles)
          role_names = [role.name for role in roles]
          checkPronouns =  any(item in role_names for item in pronounRoles)
          if checkPronouns is True:
            checker = list(set(role_names) & set(pronounRoles))
            print(checker)
            role = discord.utils.get(interaction.guild.roles, name=checker[0])
            await member.remove_roles(role)
          for x in range(0,len(pronounRoles)):
            if interaction.component[0].value == pronounRoles[x]:
              role = discord.utils.get(interaction.guild.roles, name=pronounRoles[x])
              await member.add_roles(role)  
          print("Done")


    @commands.command(name = "addSponsor")
    @commands.has_permissions(administrator=True)
    async def sponsor(self,ctx,member:discord.Member):
        await ctx.message.delete()
        await member.add_roles(discord.utils.get(member.guild.roles,name='Sponsor'))
        await ctx.send(f'Done Sponsor Role has been added to {member.mention}')
 
        
        
def setup(client):
    client.add_cog(TestCog(client))