import discord
from discord.ext import commands
import asyncio
import datetime
import __main__
import math

# pip install PyNaCl
# pip install youtube-dl
# requires the appropriate opus library in the same dir
# requires opus to be installed, apt-get install libopus0, or pacman -S opus

# this script was originally written to work across multiple servers, it has been changed to *barely* work on only one server.

# TODO 
# cooldown for heat


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')



class VoiceEntry:
    def __init__(self, message, player, datetime, heat):
        self.requester = message.author
        self.channel = message.channel
        self.player = player
        self.datetime = datetime
        self.heat = heat

    def __lt__(self, other):
        selfpriority = (self.heat, self.datetime)
        otherpriority = (other.heat, other.datetime)
        return selfpriority < otherpriority

    def __str__(self):
        fmt = '*{0.title}* requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [{0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.playerheat = {} # keep track of how often each user requests. -------------
        self.queue = [] # easily track the songs without messing with threads
        if self.bot.music_priorityqueue:
            self.songs = asyncio.PriorityQueue() # gotta keep priority -----------------
        else:
            self.songs = asyncio.Queue()
        main_loop = asyncio.get_event_loop()
        main_loop.create_task(self.loop_cooldown())

    async def loop_cooldown(self):
        """This function will decrease the user's heat every 10mins"""
        while True:
            # decrement heat if greater value than 0
            for k,v in self.playerheat.items():
                if(self.playerheat[k] > 0):
                    self.playerheat[k] = self.playerheat[k]-1
            await asyncio.sleep(600) # wait 10 more seconds.
            

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    async def embed_for_me(self, msg):
        em = discord.Embed(colour=0xfff, title=msg)
        await self.bot.send_message(self.current.channel, embed=em)
        

    def getheat(self, author):
        if author in self.playerheat:
            return self.playerheat[author]
        else:  # unable to retrieve heat, create new
            self.playerheat[author] = 1
            return 1

        
    def updateheat(self, message):
        newheat = 1 if message.channel.id == self.bot.request_channel else 5 # higher heat tax if wrong channel
        if message.author in self.playerheat:
            self.playerheat[message.author] += newheat
        else:
            self.playerheat[message.author] = newheat
            
    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self): # 'main' loop for tunes
        while True:
            #print("next through the loop")
            self.skip_votes.clear()
            self.play_next_song.clear()
            jeff = await self.songs.get() # these lines are separate because async
            if self.bot.music_priorityqueue:
                self.current = jeff[1] #these twins are separate but never too far apart
                self.queue.sort() #make sure smallest is at index 0 first
                del self.queue[0]
            else:
                self.current = jeff #add to music queue
                del self.queue[0] # apparantly pop(0) doesn't work? and no splicing for lists?
            await self.embed_for_me('♪ Now playing '+str(self.current))
            #await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Tunes:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        self.msg_badchannel = ""
        self.msg_unauthorized = "If you don't like the music then !skip or leave the channel."





    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    async def embed_for_me(self, msg, ctx):
        em = discord.Embed(colour=0xfff, title='♪ '+msg)
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        if str(ctx.message.author.voice_channel) is not null or str(ctx.message.author.voice_channel.id) != self.bot.music_channel:
            await self.embed_for_me('I can only play in Music voicechannel. This is '+str(ctx.message.author.voice_channel),ctx)
            return False
            
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.embed_for_me('Already in a voice channel...',ctx)
        except discord.InvalidArgument:
            await self.embed_for_me('This is not a voice channel...',ctx)
        else:
            await self.embed_for_me('Ready to play audio in '+channel.name,ctx)
            

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.embed_for_me('You are not in a voice channel.',ctx)
            return False
            
        if str(summoned_channel.id) != self.bot.music_channel:
            await self.embed_for_me('I can only play in Music voicechannel, this channel is '+str(summoned_channel),ctx)
            return False
            
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        if (ctx.message.author.voice_channel is None) or str(ctx.message.author.voice_channel.id) != self.bot.music_channel:
            await self.embed_for_me('I can only play in Music voicechannel, this channel is '+str(ctx.message.author.voice_channel),ctx)
            return False
            
        if not self.bot.testing and str(ctx.message.channel.id) != self.bot.request_channel:
            await self.embed_for_me('You can only request from #bottesting',ctx) 
            return False
        
        state = self.get_voice_state(ctx.message.server)
        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        opts = {
            'default_search': 'auto',
            'quiet': True
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                print("could not summon")
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next, before_options=beforeArgs)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            if not state.is_playing() and state.current is not None:
                print("There might be an error")
            heat = state.getheat(ctx.message.author)
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player, datetime.datetime.now(), heat)
            await self.embed_for_me('Enqueued ' +str(entry)+'. Your heat is now '+str(heat), ctx)
            state.updateheat(ctx.message)
            
            if self.bot.music_priorityqueue:
                await state.songs.put((heat,entry))
                state.queue.append(entry)
            else:
                await state.songs.put(entry)
                state.queue.append(entry)


    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            #player.volume = value / 100  # :P
            await self.embed_for_me('Set the volume to {:.0%}'.format(value/100), ctx)            


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        if str(ctx.message.author.id) not in self.bot.admins_dict and self.bot.music_authoritarian:
            await self.embed_for_me(self.msg_unauthorized,ctx)
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()


    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        if str(ctx.message.author.id) not in self.bot.admins_dict and self.bot.music_authoritarian:
            await self.embed_for_me(self.msg_unauthorized,ctx)
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        if str(ctx.message.author.id) not in self.bot.admins_dict and self.bot.music_authoritarian:
            await self.embed_for_me(self.msg_unauthorized,ctx)
            return False
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

            
    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx):
        """shows songs in the current queue"""
        state = self.get_voice_state(ctx.message.server)
        em = discord.Embed(colour=0xfff, title="Dank Tune Song Queue")
        em.set_footer(text="♪ DJ Minion Spinning The Decks ♪", icon_url="https://cdn.discordapp.com/avatars/173177975045488640/61d53ada7449ce4a3e1fdc13dc0ee21e.png")
        
        if self.bot.music_priorityqueue:
            state.queue.sort() #make sure it's in the right order
        msg = ""
        spot_in_line = 1
        counter = 1
        for text in state.queue:
            if(spot_in_line >= 106):
                break;
            msg += "**"+str(spot_in_line)+"**: "+str(text)+"\n" # this breaks due to char limits
            
            if(counter > 5):
                em.add_field(name="Batch of tunes",value=msg)
                msg = "" #reset msg
                counter = 1 # reset limit
            #THIS ONLY BREAKS WHEN YOU HAVE 107 SONGS IN QUEUE
            counter += 1    
            spot_in_line+=1
               
        if len(msg) > 2:       
            em.add_field(name="The best of the worst", value=msg)
        await self.bot.send_message(ctx.message.channel, embed=em)


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """
        if (ctx.message.author.voice_channel is None) or str(ctx.message.author.voice_channel.id) != self.bot.music_channel:
            await self.embed_for_me('You can only skip in Music voicechannel, this channel is '+str(ctx.message.author.voice_channel),ctx)
            return False        
        
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.embed_for_me('Not playing any music right now...',ctx)
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.embed_for_me('Requester requested skipping song...',ctx)        
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            skipnum = len(self.bot.get_channel(self.bot.music_channel).voice_members)
            if total_votes >= math.floor(skipnum/2):
                await self.embed_for_me('Skip vote passed, skipping song...',ctx)
                state.skip()
            else:
                await self.embed_for_me('Skip vote added, currently at [{}/{}]'.format(total_votes, math.floor(skipnum/2)),ctx)
        else:
            await self.embed_for_me('You have already voted to skip this song.',ctx)


    @commands.command(pass_context=True, no_pm=True)
    async def bump(self, ctx):
        """vote to bump the indexed song to the front."""
        # TODO
        if (ctx.message.author.voice_channel is None) or str(ctx.message.author.voice_channel.id) != self.bot.music_channel:
            await self.embed_for_me('You can only skip in Music voicechannel, this channel is '+str(ctx.message.author.voice_channel),ctx)
            return False   
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.embed_for_me('Not playing any music right now...',ctx)
            return
           

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.embed_for_me('Not playing anything.',ctx)
        else:
            skip_count = len(state.skip_votes)
            await self.embed_for_me('Now playing {} [skips: {}/3]'.format(state.current, skip_count),ctx)
        
        
        
def setup(bot):
    bot.add_cog(Tunes(bot))
    if __main__.__file__ == "bot.py": # use test channels
        print("set to test channels")
        bot.testing = True
        bot.request_channel = "304837708650643459"
        bot.music_channel = "312693106736889867"
    else: # use production channels
        bot.testing = False
        print("set to production channels")
        bot.request_channel = "354084037465473025"
        bot.music_channel = "228761314644852737"
    bot.music_priorityqueue = False
    bot.music_authoritarian = False
    bot.admins_dict = {"173702138122338305":"henry",
     "173177975045488640":"nos"
    }

