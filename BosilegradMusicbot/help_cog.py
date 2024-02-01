import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.help_message = """
        
 ```
 Komandi:
 
 !help - Pokazue ti komandite
 !p <tvojata pesma ovde> - Naodi pesmata na yt
 !q -  Pokazue ti sto ste narucili(ega e chalga)
 !skip - Idi dalje
 !clear - Otkazues narucenite pesmi
 !leave - Fajront
 !pause - Pauzira 
 !resume - Nastavlja da sviri
 ```       
        
 """
        self.text_channel_text = []
        
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text.text_channels:
                self.text_channel_text.append(channel)
                
        await self.send_to_all(self.help_message)
        
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)
    
    @commands.command(name = 'help', help = 'Pokazue site komandi')
    async def help(self, ctx):
          await ctx.send(self.help_message)
          
