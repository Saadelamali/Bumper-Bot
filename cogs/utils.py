import json
import motor
import disnake as discord
from disnake.ext import commands
from .cooldown.CustomCooldown import is_premium
from main import Report, cl

with open("settings.json") as f:
   get = json.load(f)

slash_command_invite = get["invite_url"]   

class Utils(commands.Cog):
   def __init__(self, bot):
      self.bot = bot 
         
   @commands.slash_command(name= "bump", description="Bumps your server to other servers")
   @commands.guild_only()
   @commands.dynamic_cooldown(is_premium.cooldown, type = commands.BucketType.guild)
   async def Bump(self, inter):
      await inter.response.defer(with_message = True)
      check = await cl.find_one({"_id" : inter.guild.id})
      bump_info = []
      bump_info.extend([check['channel'], check['invite'], check['description'], check['color'], check['banner']])
      guilds = cl.find()
      
      if check is None:
         await inter.send("Please setup your server, try `/setup channel` command!", ephemeral=True)
         self.Bump.reset_cooldown(inter)
         return
      elif bump_info[0] == "None":
         await inter.send("Please setup your server, try `/setup channel` command!", ephemeral=True)
         self.Bump.reset_cooldown(inter)
         return
      elif bump_info[1] == "None":
         await inter.send("Please setup your server, try `/setup invite` command!", ephemeral=True)
         self.Bump.reset_cooldown(inter)
         return
      elif check["tags"] == "None":
         await inter.send("Run `/setup tag` and choose your tag")
         self.Bump.reset_cooldown(inter)
         return
      
      embed = discord.Embed(color = discord.Color(0x3dbb20))
      embed.set_thumbnail(url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}")
      embed.set_author(name=inter.guild.name,icon_url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}")
      embed.add_field(name="Server Successfully Bumped",value=f"> **Note** : You can get bumper premium from voting at [top.gg](https://top.gg/bot/908043115649187880/vote) (30 votes) or boosting (1  boost)  [join our guild](https://discord.gg/QF28uQus8d) for more information!")
      await inter.send(embed=embed)
      
      premium = await cl.find_one({"_id": 849658396675276841})
      view = Report(self.bot, check["_id"])
      view.add_item(discord.ui.Button(style = discord.ButtonStyle.url, label="Click To Join", url = f"{bump_info[1]}"))
      if inter.guild.id not in premium["list"]:
        if bump_info[3] != 327680 and bump_info[4] != "None":
            await cl.update_one({"_id" : inter.guild.id},{"$set" : {"color" : 327680, "banner": "None"}})
            
        elif bump_info[4] != "None" or bump_info[3] != 327680:
            if bump_info[4] != "None":
                await cl.update_one({"_id" : inter.guild.id},{"$set" : {"banner" : "None"}})
            elif bump_info[3] != 327680:
                 await cl.update_one({"_id" : inter.guild.id},{"$set" : {"color" : 327680}})
        
      async for x in guilds:
         c_ = x["channel"]
         if c_ == "None":
            continue
         
         if str(check["tags"]) != str(x["tags"]):
            continue
   
         em = discord.Embed(color = bump_info[3])
         em.add_field(name="<:guild:912104201277022210> Server Name", value=inter.guild.name,inline= False)
         em.add_field(name="<:description:912802838177009704> Description", value=f"{'This server doesnt have a description' if bump_info[2] == 'None' else bump_info[2]}",inline= False)
         em.add_field(name="<:Id:912108381903421490> Server ID", value=inter.guild.id,inline= False)
         em.add_field(name="<:owner:912099748671029248> Server Owner", value=inter.guild.owner,inline= False)
         em.add_field(name="<:Boosts:912097830942957568> Server Boosts", value=f"{inter.guild.premium_subscription_count} Boost(s)",inline= False)
         em.add_field(name="<:Members:912103420134064238> Server Member Count", value=f"{inter.guild.member_count} Members",inline= False)
         em.set_image(url=f"{'' if bump_info[4] is 'None' else bump_info[4]}")
         em.set_author(name=inter.guild.owner, icon_url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}")        
         em.set_thumbnail(url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}") 
         other_bump_channels = self.bot.get_channel(c_)
         try:
            await other_bump_channels.send(embed=em, view=view)
         except Exception:
            continue
 
   @commands.slash_command(name = "vote", description="Vote for bumper")
   @commands.guild_only()
   async def Vote(self, inter):
      await inter.response.defer(with_message = True)
      name = inter.author.name
      embed = discord.Embed(description="Vote for me at [Top.gg](https://top.gg/bot/908043115649187880) and [Dbl.com](https://discordbotlist.com/bots/bumper-1985)",
      color=discord.Color(0x050000))
      embed.set_author(name=name, icon_url=inter.author.avatar.url)
      await inter.send(embed=embed)
      
   @commands.slash_command(name = "preview", description="Shows you your server ADS")
   @commands.guild_only()
   @commands.cooldown(1, 3, commands.BucketType.guild)
   async def Preview(self, inter):
        await inter.response.defer(with_message = True)
        check = await cl.find_one({"_id" : inter.guild.id})
         
        if check is None:
            await inter.send("This serer doesn't have any data, please setup your server", ephemeral=True)
            return

        bump_info = []
        bump_info.extend([check['channel'], check['invite'], check['description'], check['color'], check['banner']])
        em = discord.Embed(color = bump_info[3])
        em.add_field(name="<:guild:912104201277022210> Server Name", value=inter.guild.name,inline= False)
        em.add_field(name="<:description:912802838177009704> Description", value=f"{'This server doesnt have a description' if bump_info[2] == 'None' else bump_info[2]}",inline= False)
        em.add_field(name="<:Id:912108381903421490> Server ID", value=inter.guild.id,inline= False)
        em.add_field(name="<:owner:912099748671029248> Server Owner", value=inter.guild.owner,inline= False)
        em.add_field(name="<:Boosts:912097830942957568> Server Boosts", value=f"{inter.guild.premium_subscription_count}",inline= False)
        em.add_field(name="<:Members:912103420134064238> Server Member Count", value=f"{inter.guild.member_count} members",inline= False)
        em.set_image(url=f"{'' if bump_info[4] is 'None' else bump_info[4]}")
        em.set_author(name=inter.guild.owner,icon_url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}")        
        em.set_thumbnail(url=f"{'' if inter.guild.icon is None else inter.guild.icon.url}") 
        await inter.send(embed=em)
   
   @commands.slash_command(name="invite", description="Invite Bumper to your server")
   @commands.guild_only()
   async def Invite(self, inter):
      await inter.response.defer(with_message = True)
      embed = discord.Embed(
        description =f"[Bot Invite]({slash_command_invite})\n[Support Server](https://discord.gg/QF28uQus8d)",
        color = 0x050000
      )
      embed.set_author(name=inter.author.name,icon_url=inter.author.avatar.url)
      await inter.send(embed=embed)
   
   @commands.slash_command(name="botinfo", description="Shows you the information about bumper")
   @commands.guild_only()
   async def Botinfo(self, inter):
      await inter.response.defer(with_message = True)
      em = discord.Embed(description = f"{self.bot.user.name} is a bump bot made by Saad.#5088 to help you to grow your discord server!",
        color = 0x050000
      )
      em.set_author(name=f"{self.bot.user.name}")
      em.add_field(name="Information",value=f"```yml\nLibrary   ::  Disnake\nDatabase  ::  MongoDB Atlas\nLatency   ::  {round(self.bot.latency*1000)} ms\nUsers     ::  {len(self.bot.users):,}\nServers   ::  {len(self.bot.guilds):,}\nShard ID  ::  {inter.guild.shard_id}```",inline=False)
      em.add_field(name="Links",value=f"[Invite-{self.bot.user.name}]({slash_command_invite}) **|** [Support Server](https://discord.gg/QF28uQus8d)")
      await inter.send(embed=em) 
    
   @commands.slash_command(name= "help", description="Shows you the help")
   @commands.guild_only()
   async def Help(self, inter):
      await inter.response.defer(with_message = True)
      view = discord.ui.View()
      view.add_item(discord.ui.Button(style = discord.ButtonStyle.url, label="Invite Link", url="https://discord.com/api/oauth2/authorize?bot_id=908043115649187880&permissions=137439308944&scope=bot%20applications.commands"))
      view.add_item(discord.ui.Button(style = discord.ButtonStyle.url, label = "Support Server", url = "https://discord.gg/QF28uQus8d"))
      url = "https://images.saymedia-content.com/.image/ar_16:9%2Cc_fill%2Ccs_srgb%2Cq_auto:eco%2Cw_1200/MTc0NDcyOTY4MjU5MjQ5Nzk4/10-ways-to-get-more-users-to-your-discord-server.png"
      emb = discord.Embed(
        title = f"Hello {inter.author.name}", 
        description="I am a bot that can grow your discord server. Easy to setup and easy to use, all you have to do is run `/setup` command. Also you can bump your discord every **60 minutes**!!!!",
        color = 0x050000
      )
      emb.set_thumbnail(url=self.bot.user.avatar.url)
      emb.add_field(name="**Commands**",value="> `/bump :` Bumps this server\n> `/setup channel <channel> :` Sets your bump channel (like a partnering channel) \n> `/setup invite <channel> :`\n> `/botinfo :` Shows you bumper's information\n> `/invite :` Add Bumper to your amazing server\n> `/vote :` Support us by voting for bumper",inline=False)
      emb.add_field(name="**Need help?**",value="Join the [support server.](https://discord.gg/QF28uQus8d) We're going to explain everything to you!",inline=False)
      emb.set_image(url=url)
      await inter.send(embed=emb, view=view)   
   
def setup(bot):
  bot.add_cog(Utils(bot))
