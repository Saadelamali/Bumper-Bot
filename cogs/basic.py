from io import BytesIO
import disnake as discord
from disnake.ext import commands
from .cooldown.CustomCooldown import Tags
from main import cl

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name = "setup")
    @commands.guild_only()
    async def Setup(self, inter):
      check = await cl.find_one({"_id" : inter.guild.id})
      if check is None:
        data = {
         "_id" : inter.guild.id , 
         "channel" : "None",
         "invite" : "None",
         "description" : "None",
         "color" : 0x050000,
         "banner" : "None",
         "tags": "None"
        }
        await cl.insert_one(data)
    
    @Setup.sub_command(name = "tags", description = "choose the tag") 
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Tags(self, inter):
      await inter.response.defer(with_message = True)
      view = Tags(inter)
      emb = discord.Embed(
        title = "Choose your tag",
        description=f"**Note: ** you might get banned if you chose a tag that doesn't match your server",
        color = 0x050000
      )
      view.message = await inter.send(embed=emb, view=view)
    
    @Setup.sub_command(name = "channel", description = "Sets your bump-channel") 
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Channel(self, inter, channel : discord.TextChannel):
      await inter.response.defer(with_message = True)
      await cl.update_one({"_id" : inter.guild.id},{"$set" : {"channel" : channel.id}})
      emb = discord.Embed(
        description=f"Your bump channel has been updated ({channel.mention})",
        color = 0x050000
        )
      await inter.send(embed=emb)
 
    @Setup.sub_command(name = "invite", description="Sets your invite channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Invite(self, inter, channel : discord.TextChannel):
      await inter.response.defer(with_message = True) 
      inv = await channel.create_invite()
      await cl.update_one({"_id" : inter.guild.id},{"$set" : {"invite" : f"{inv}"}})
      emb = discord.Embed(
         description=f"Your discord server invite has been updated ({inv})",
         color = 0x050000 
       )
      await inter.send(embed=emb)
    
    @Setup.sub_command(name = "description", description="Sets your embed description ")
    @commands.guild_only()
    @commands.has_permissions(administrator=True) 
    async def Description(self, inter, description):
      await inter.response.defer(with_message = True) 
      count = [] 
      for i in description:
        count.append(i)  
   
      if len(count) >= 800:
           await inter.send("Your description length is above 800 characters. ", ephemeral=True)
           return
       
      await cl.update_one({"_id" : inter.guild.id},{"$set" : {"description" : f"{description}"}})
      embed = discord.Embed(description="Your description has been updated.",
      color = 0x050000)
      await inter.send(embed=embed)

    @Setup.sub_command(name = "banner", description="Sets your embed banner")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Banner(self, inter, image: discord.Attachment):
       await inter.response.defer(with_message = True)
       premium = await cl.find_one({"_id": 849658396675276841})
       if inter.guild.id not in premium["list"]:
          embed = discord.Embed(title="Your server doesn't have premium!!", description=f"Your server doesn't have premium version. That means premium features are locked! With {self.bot.user.name} premium you'll be able to access to tons of awesome features! When you upgrade to {self.bot.user.name} premium you get :\n> - Custom Embed Color\n> - Custom Embed Banner\nWant premium?\n[Join here](https://discord.gg/ZYKtHS6anN)", color = 0xf10000)
          embed.set_footer(text="3$/month")
          await inter.send(embed=embed, ephemeral=True)
          return
       
       guild = self.bot.get_guild()#Support guild id
       channel: discord.TextChannel = guild.get_channel()#A channel where the bot sends the images
       file_saved = image.save(BytesIO())
       msg: discord.Message = await channel.send(file = file_saved)
       embed = discord.Embed(description="Your banner has been updated.",
       color = 0x050000)
       embed.set_image(url= msg.attachments[0].url)
       await cl.update_one({"_id" : inter.guild.id},{"$set" : {"banner" : f"{msg.attachments[0].url}"}})
       await inter.send(embed=embed)
 
    @Setup.sub_command(name = "color", description="Sets your embed color")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def Color(self, inter, color: str):
      await inter.response.defer(with_message = True) 
      premium = await cl.find_one({"_id": 849658396675276841})
      if inter.guild.id not in premium["list"]:
         embed = discord.Embed(title="Your server doesn't have premium!!",
         description=f"Your server doesn't have premium version. That means premium features are locked! With {self.bot.user.name} premium you'll be able to access to tons of awesome features! When you upgrade to {self.bot.user.name} premium you get :\n> - Custom Embed Color\n> - Custom Embed Banner\nWant premium?\n[Join here](https://discord.gg/ZYKtHS6anN)",
         color = 0xf10000)
         embed.set_footer(text="3$/month")
         await inter.send(embed=embed, ephemeral=True)
         return
      elif "#" in color:
        color = color.replace("#", "")

      hex_r = int(color, 16)
      embed = discord.Embed(description="Your color has been updated.",
      color = 0x050000)
      await cl.update_one({"_id" : inter.guild.id},{"$set" : {"color" : hex_r}})
      await inter.send(embed=embed)
 
def setup(bot):
  bot.add_cog(Basic(bot))            