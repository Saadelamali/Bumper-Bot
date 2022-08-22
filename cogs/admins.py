import disnake as discord
from disnake.ext import commands
from main import cl 

class Admins(commands.Cog):
   def __init__(self, bot):
       self.bot = bot
  
   @commands.command(aliases = ["Add", "ADD"])
   @commands.is_owner()
   @commands.cooldown(1, 5, commands.BucketType.user)
   async def add(self, ctx, *, guild : int):
    premium = await cl.find_one({"_id": 849658396675276841})#A list
    if guild in premium["list"]:
        await ctx.send("already in the premium list")
        return
    info = self.bot.get_guild(guild)    
    try:
      await cl.update_one({"_id" : 849658396675276841},{"$push" : {"list" : guild}})
      await ctx.send(f"<:zeroon1yes:866375654751338516> {info.name} added to the list.")
    except Exception as e:
      await ctx.send(f"Error: ``{e}``")
      
   @commands.command(aliases = ["Remove", "REMOVE"])
   @commands.is_owner()
   @commands.cooldown(1, 5, commands.BucketType.user)
   async def remove(self, ctx, *, num : int):
     await cl.update_one({"_id" : 849658396675276841},{"$pull" : {"list" : num}})
     guild = self.bot.get_guild(num)
     await ctx.send(f"<:zeroon1yes:866375654751338516> {guild.name} Removed from the list!!")
        
   @commands.command(aliases = ["Check", "CHECK"])
   @commands.is_owner()
   @commands.cooldown(1, 5, commands.BucketType.user)
   async def check(self, ctx):
     premium = await cl.find_one({"_id": 849658396675276841})#A list
     guilds = []
     for i in premium["list"]:
       guild = self.bot.get_guild(i)   
       guilds.append(f"Name : {guild.name} | ID : {guild.id} | Owner : {guild.owner} ")
     embed = discord.Embed(description='\n\n'.join(guilds), color = discord.Color.blue())    
     await ctx.send(embed=embed)

   @commands.command(aliases = ["Ban", "BAN"])
   @commands.guild_only()
   @commands.is_owner()
   async def ban(self, ctx, guild: int):
    try: 
      server = self.bot.get_guild(guild) or await self.bot.fetch_guild(guild)
    except Exception:
      pass
    check = await cl.find_one({"_id": 849658396675276841})
    if guild in check["banned"]:
      await ctx.send("This server is already banned")
      return
    await cl.update_one({"_id": guild}, {"$push": {"banned": guild}})
    await ctx.send(f"Successfully banned {server.name}")
    
   @commands.command(aliases = ["Unban", "UNBAN"])
   @commands.guild_only()
   @commands.is_owner()
   async def unban(self, ctx, guild: int):
    try: 
      server = self.bot.get_guild(guild) or await self.bot.fetch_guild(guild)
    except Exception:
      pass
    check = await cl.find_one({"_id": 849658396675276841})
    if guild not in check["banned"]:
      await ctx.send("This server is not banned")
      return
    await cl.update_one({"_id": guild}, {"$pull": {"banned": guild}})
    await ctx.send(f"Successfully unbanned {server.name}")
    
      
        
def setup(bot):
  bot.add_cog(Admins(bot))