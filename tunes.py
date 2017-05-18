import discord
from discord.ext import commands
import asyncio
import __main__

# pip install PyNaCl
# pip install youtube-dl
# requires the appropriate opus library in the same dir
# requires opus to be installed, apt-get install libopus0, or pacman -S opus

# this script was originally written to work across multiple servers, it has been changed to work on only one server.

# TODO 
# cooldown for heat
# dies when requester skips.
# dies when queue with no song in queue
# download entire song first


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        #self.songs = asyncio.PriorityQueue() # gotta keep priority -----------------
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.playerheat = {} # keep track of how often each user requests. -------------
        if self.bot.music_priorityqueue:
            self.songs = asyncio.PriorityQueue() # gotta keep priority -----------------
        else:
            self.songs = asyncio.Queue()

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    def getheat(self, author):
        if author in self.playerheat:
            return self.playerheat[author]
        else:
            print("unable to retrieve playerheat")
        
    def updateheat(self, message):
        newheat = 1 if message.channel.id == self.bot.request_channel else 5 #I like the ternary more
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
            print("next through the loop")
            self.skip_votes.clear()
            self.play_next_song.clear()
            jeff = await self.songs.get() # these lines are separate because async
            if self.bot.music_priorityqueue:
                self.current = jeff[1] #these twins are separate but never too far apart
            else:
                self.current = jeff
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Tunes:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

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

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        if str(ctx.message.author.voice_channel) is not null or str(ctx.message.author.voice_channel.id) != self.bot.music_channel:
            await self.bot.say('I can only play in Music voicechannel, this voicechannel is '+str(ctx.message.author.voice_channel))
            return False
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False
        if str(summoned_channel.id) != self.bot.music_channel:
            await self.bot.say('I can only play in Music voicechannel, this voicechannel is '+str(summoned_channel))
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
            await self.bot.say('I can only play in Music voicechannel, this voicechannel is '+str(ctx.message.author.voice_channel))
            return False
        if str(ctx.message.channel.id) != "293120981067890691":
            await self.bot.say("You can only request from #bottesting")
            return False
        
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'reconnect': 1,
            'reconnect_streamed':1,
            'reconnect_delay_max':5,
            'socket-timeout':5
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                print("could not summon")
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
            print("successfully created player")
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            if not state.is_playing() and state.current is not None:
                print("shit gone south")
            
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            state.updateheat(ctx.message)
            heat = state.getheat(ctx.message.author)
            print("current heat is "+str(heat))
            await self.bot.say("Your heat is now at "+str(heat))
            if self.bot.music_priorityqueue:
                await state.songs.put((heat,entry))
            else:
                await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            #player.volume = value / 100  # :P
            await self.bot.say('Set the volume to {:.0%}'.format(value / 100))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        if str(ctx.message.author.id) not in self.bot.admins_dict and self.bot.music_authoritarian:
            await self.bot.say("If you don't like the music then !skip or leave the channel.")
            return False
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        if str(ctx.message.author.id) not in self.bot.admins_dict and self.bot.music_authoritarian:
            await self.bot.say("If you don't like the music then !skip or leave the channel.")
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
            await self.bot.say("If you don't like the music then !skip or leave the channel.")
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
            
            ### reset doesn't reset audio, this means the audio_player or voice states does the job
    @commands.command(pass_context=True, no_pm=True)
    async def reset(self, ctx):
        """resets the audio, keeping the queue"""
    
        server = ctx.message.server
        state = self.get_voice_state(server)
    
        if state.is_playing():
            player = state.player
            player.stop()
            player.start()
            
    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx):
        """shows songs in the current queue"""
        state = self.get_voice_state(ctx.message.server)
        print("size of pre-main is: "+str(state.songs.qsize()))
        arr = []
        print("Printing type of current song: current, player, voice")
        print(type(state.current)) 
        print(type(state.player))
        print(type(state.voice))
        print(str(state.is_playing()))
        # less logic in loops
        if self.bot.music_priorityqueue:
            q = asyncio.PriorityQueue()
            while not state.songs.empty():
                l = await state.songs.get()
                await q.put(l)
                arr.append(str(l[1]))
        else:
            q = asyncio.Queue()
            while not state.songs.empty():
                l = await state.songs.get()
                await q.put(l)
                arr.append(str(l))
        
        print("size of postpre-q is: "+str(q.qsize()))
        state.songs = q
        print("size of post-q is: "+str(q.qsize()))
        print("size of post-main is: "+str(state.songs.qsize()))
        if len(arr) == 0:
            await self.bot.say("The queue is empty")
        elif len(arr) < 5:
            await self.bot.say("\n\n".join(arr))
        else:
            await self.bot.send_message(ctx.message.author, "\n".join(arr))


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))
        
        
        
def setup(bot):
    bot.add_cog(Tunes(bot))
    if __main__.__file__ == "bot.py": # use test channels
        print("set to test channels")
        bot.request_channel = "304837708650643459"
        bot.music_channel = "312693106736889867"
    else: # use production channels
        print("set to production channels")
        bot.request_channel = "293120981067890691"
        bot.music_channel = "228761314644852737"
    bot.music_priorityqueue = False
    bot.music_authoritarian = False
    bot.admins_dict = {"173702138122338305":"henry",
     "173177975045488640":"nos"
    }

