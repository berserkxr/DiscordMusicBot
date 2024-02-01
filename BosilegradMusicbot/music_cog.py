import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False
        
        self.music_queue = []
        self.YDL_OPTIONS = {'format' : 'bestaudio'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}
                
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)
        
    def search_yt(self, item):
        if item.startswith('https://'):
            title = self.ydl.extract_info(item, download=False)['title']
            return{'source': item, 'title': title}
        search = VideosSearch(item, limit=1)
        return{'source': search.result()['result'][0]['link'], 'title':search.result()['result'][0]['title']}
    
        
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            
            #zemi url na videoto
            m_url = self.music_queue[0][0]['source']
            
            #izbrisi iz queue pesmata koja trenutno pusta
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= 'ffmpeg.exe',**self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))           
        else:
            self.is_playing = False
            
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                
                if self.vc == None:
                    await ctx.send('Ne mogu da uleznem')
                    return
                
            else:
                await self.vc.move_to(self.music_queue[0][1])
                
            self.music_queue.pop()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= 'ffmpeg.exe', **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
                
            
        else:
            self.is_playing = False
                 
    @commands.command(name='play', aliases=['p', 'pusti'], help='Sviraj')
    async def play(self, ctx, *args):
        query = ' '.join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send('```Mora prvo da uleznes u channel!```')
            return        
        if self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send('```Ne mogu da simnem pesmata jbg```')
            else:
                await ctx.send('```Pesmata e dodadena u redosled```')
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)
    @commands.command(name='pause', help='Pauzira ti pesmata')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            
    @commands.command(name='resume',aliases = ['r'], help='Pusti pak')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            
    @commands.command(name='skip',aliases = ['s'], help='Sledeca')
    async def pause(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #pusti sledeca ako ima u queue
            await self.play_music(ctx)
            
    @commands.command(name='queue', aliases=['q'], help = 'Pokazue koi si narucil')
    async def queue(self, ctx):
        retval = ''       
        for i in range(0, len(self.music_queue)):
            retval += f"{i+1} -" + self.music_queue[i][0]['title'] + '\n' 
            
        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send('```Nema nista poruceno, rokaj```')
            
    @commands.command(name = 'clear', aliases = ['c'], help='Glupi poruceni, trazi drugi')
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('Nema vise poruceni')
        
    @commands.command(name = 'leave', aliases = ['disconnect', 'l', 'd'], help='prati ciganino doma')
    async def leave(self, ctx):
        self.is_playing = False
        self.is_pause = False
        await self.vc.disconnect()