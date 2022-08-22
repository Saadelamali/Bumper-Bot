import json
import motor
import disnake as discord
from disnake.ext import commands

with open("settings.json") as f:
   get = json.load(f)

token = get["token"]
url = get["database_url"]
cluster = motor.motor_tornado.MotorClient(url)
db = cluster["ZeroOn1"]
cl = db["premium"] 
rd = db["redeem"]
 
intents = discord.Intents.default()
intents.members = True
intents.guilds = True 

async def timed_or_no(inter):
   if inter.guild.me.current_timeout:
      await inter.send("I'm timed out! please remove it!", ephemeral = True)
   else:
      return True

async def is_banned(inter):
   check = await cl.find_one({"_id": 849658396675276841})#A list
   if inter.guild.id in check["banned"]:
      await inter.send("Hey, this server is banned! join our support server to get unbanned and/or more information https://discord.gg/ZYKtHS6anN", ephemeral= True)
   else:
      return True

class Report(discord.ui.View):
   def __init__(self, bot, inter: int = None):
      super().__init__(timeout = None)
      self.inter = inter
      self.bot = bot
      self.users = {}
   
   @discord.ui.button(style = discord.ButtonStyle.red, label="Report", custom_id="persistent_view:red")
   async def red(self, button, interaction: discord.MessageInteraction):
      try:
         self.users[str(self.inter)]
      except KeyError:   
         self.users[str(self.inter)] = []
          
      if interaction.author.id in self.users[str(self.inter)]:
         await interaction.send("You've already reported this server", ephemeral=True)
         return
      
      await interaction.send(f"Thank you for the report!", ephemeral=True)
      self.users[str(self.inter)].append(interaction.author.id)
      
      guild = self.bot.get_guild()#Support guild id
      channel = guild.get_channel()#A channel where the bot sends the reports
      check = await cl.find_one({"_id": self.inter})
      
      g = self.bot.get_guild(self.inter)
      embed = discord.Embed(title = f"{g.name} Was Reported")
      embed.add_field(name="Reported by", value=f"{interaction.author}", inline=True)
      embed.add_field(name="Tag", value=f"{check['tags']}", inline=True)
      embed.add_field(name="Server name", value=f"{g.name}", inline=True)
      embed.add_field(name="Server id", value=f"{g.id}", inline=True)
      embed.add_field(name = "Server Owner", value = f"{g.owner}", inline=True)
      embed.set_image(url = self.bot.avatar.url)
      await channel.send(embed=embed)
      
class Bumper(commands.AutoShardedBot):
   def __init__(self):
      super().__init__(
         command_prefix = commands.when_mentioned,
         help_command = None,
         activity = discord.Game(name="/help"),
         status = discord.Status.idle,
         intents = intents, 
         shard_count = 3,
         owner_ids = [533992347369865216, 868919848913236038]
      )   
      self.slash_command_check_once(timed_or_no)
      self.slash_command_check_once(is_banned)
      self.added_view = False
         
   async def on_ready(self):
      guild = self.get_guild()#the bot support guild id
      channel = guild.get_channel()#A private channel where the bot sends a message when it is active
      if not self.added_view:
         self.add_view(Report(self))
      try: 
        self.load_extensions("cogs")
      except Exception as e:
         await channel.send(f"Error:\n```{e}```")
      await channel.send("Ready")

   async def on_guild_remove(self, guild):
      check = await cl.find_one({"_id" : guild.id})
      premium = await cl.find_one({"_id" : 849658396675276841})
      if check is None:
         return
      if guild.id in premium["list"]:
         await cl.update_one({"_id" : 849658396675276841},{"$pull" : {"list" : guild.id}})
      data = {
        "_id" : guild.id
      }
      await cl.delete_one(data)
    
   async def on_guild_channel_delete(self, channel):
      guild = channel.guild
      id_ = guild.id
      check = await cl.find_one({"_id" : id_})
      if check is None:
         return 
      if channel.id == check["channel"]:
         await cl.update_one({"_id" : id_},{"$set": {"channel" : "None"}})
      else:
         pass   
   
   async def on_command_error(self, ctx, error) -> None:
      if isinstance(error, commands.CommandOnCooldown):
         return
      elif isinstance(error, commands.NotOwner):
        return await ctx.send("<:zeroon1no:866375710130044968> You can't use this.")
      
   async def on_slash_command_error(self, interaction, exception) -> None:
      if isinstance(exception, commands.CommandOnCooldown):
        num = round(exception.retry_after)
        minutes = num // 60
        seconds = num % 60
        embed = discord.Embed(description=f"Please wait another {'' if minutes == 0 else f'{minutes}m'} {seconds}s until the server can be bumped", color = discord.Color(0xf10000))
        await interaction.send(embed=embed, ephemeral=True)
        
      if isinstance(exception, commands.MissingPermissions):
         embed = discord.Embed(title="Error",
            description="You need **__ADMINISTRATOR__** permission to run this command. ",
            color=discord.Color(0xf10000)
         )
         await interaction.send(embed=embed, ephemeral=True)
         
      if isinstance(exception, commands.ChannelNotFound):
         embed = discord.Embed(title="Error",
            description="Channel not found lol.",
            color=0xf10000
         )
         await interaction.send(embed=embed, ephemeral=True)
       

bot = Bumper()

@bot.command(alaises=["Load","LOAD"])
@commands.guild_only()
@commands.is_owner()
async def load(ctx):
      try: 
        bot.load_extensions("cogs")
      except Exception as e:
         await ctx.send(f"{e}")
         return
      await ctx.send(f"Loaded Successfully")

if __name__ == "__main__":
   bot.run(token)
