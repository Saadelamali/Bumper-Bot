import pymongo
import json
import disnake
from disnake.ext import commands
from main import cl

with open("settings.json") as f:
   get = json.load(f)

url = get["database_url"]   
cluster = pymongo.MongoClient(url)
db = cluster["ZeroOn1"]
cle = db["premium"]

class is_premium:
  def cooldown(ctx):
    """Checks if the guild id in the list (premium)"""
    guilds = cle.find_one({"_id" : 849658396675276841})
    if ctx.guild.id in guilds["list"]:
      bucket = commands.Cooldown(rate = 1, per = 1800)  
    else:
      bucket = commands.Cooldown(rate = 1, per = 3600) 
    return bucket
  
class Tags(disnake.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx#check tags slash_command to understand what is this for
  
  @disnake.ui.button(style = disnake.ButtonStyle.grey, label = "NSFW", emoji = "🔞")
  async def nsfw(self, button, inter):
    if self.ctx.author.id == inter.author.id:
      await cl.update_one({"_id": self.ctx.guild.id}, {"$set": {"tags": "nsfw"}})
      await inter.send("Your tag has been updated to nsfw", ephemeral=True)
    else:
      await inter.send("That's not yours buddy", ephemeral=True)
  
  @disnake.ui.button(style = disnake.ButtonStyle.grey, label = "SFW", emoji = "🕊")
  async def sfw(self, button, inter):
    if self.ctx.author.id == inter.author.id:
      await cl.update_one({"_id": self.ctx.guild.id}, {"$set": {"tags": "sfw"}})
      await inter.send("Your tag has been updated to sfw", ephemeral=True)
    else:
      await inter.send("That's not yours buddy", ephemeral=True)
    
  