import discord
from games.roulletteLogic import RouletteLogic
from games.roulletteLogic import getName
from discord.ext import commands



class Roulette():
    def __init__(self, bot):
        self.bot = bot
        self.games = dict()
        
    def inGame(self,player):
        found = False
        gme = None
        for game in self.games:
            if player in self.games[game].players:
                gme = self.games[game]
                break
                
        #So if they are in a game it will us the game if not its null
        return gme
        
        
    @commands.group(pass_context = True)
    async def gameR(self,ctx):
        pass

        
        
    @gameR.command()
    async def help(self):
        
        
        embed = discord.Embed(title="gameR Commands", colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

        embed.add_field(name=".help", value="Displays this help menu.")
        embed.add_field(name=".new <game>", value="Start a new game and join it with the given id")
        embed.add_field(name=".join <game>", value="Joins the given game id")
        embed.add_field(name=".players <game>", value="Lists players in a game")
        embed.add_field(name=".list", value="Lists all games")
        embed.add_field(name=".start", value="Starts the current game your in")
        embed.add_field(name=".fire", value="When its your turn fire the curretly loaded chamber in the gun")
        embed.add_field(name=".spin", value="When its your turn, randomize the location of the bullet and fire, everytime you spin you fire once more")
        embed.add_field(name=".leave", value="Once a game is done you can leave the room")
        embed.add_field(name=".restart", value="Once a game is done, reset the room to get ready to start again, and let new people join")
        embed.add_field(name=".room", value="Displays your current game")
        embed.add_field(name="Source Code", value="https://github.com/henrymzhao/csss-minion/")

        await self.bot.say(embed=embed)

        
    
    
    @gameR.command(pass_context = True)
    async def room(self,ctx):
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in any of the rooms")
            return
        
        self.bot.say(getName(ctx.message.author) + " in Room " + game.gameName + " on channel " + game.channel.name)   
        
    
    @gameR.command(pass_context = True)
    async def start(self,ctx):
        
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return
        
        game.start()
        self.bot.delete_message(ctx.message)
    
    @gameR.command(pass_context = True)
    async def fire(self,ctx):
        await self.bot.delete_message(ctx.message)
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return      
        game.fire(ctx.message.author)
     
    @gameR.command(pass_context = True)
    async def spin(self,ctx):
        await self.bot.delete_message(ctx.message)
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return       
        game.spin(ctx.message.author)
     
    @gameR.command(pass_context = True)
    async def restart(self,ctx):
        await self.bot.delete_message(ctx.message)
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return
        
        game.restart()
    
    
    @gameR.command(pass_context = True)
    async def afk(self,ctx):
        await self.bot.delete_message(ctx.message)
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return
        
        game.afk()
     
    @gameR.command(pass_context = True)
    async def list(self):
        #self.bot.delete_message(ctx.message)
        if len(self.games) > 0:
            keys = self.games.keys()
            await self.bot.say("Current Running games  : " + '\n'.join(keys))
        else:
            await self.bot.say("No games running right now")
    
    @gameR.command(pass_context = True)
    async def new(self,ctx,gameNameInput : str):
        
        if self.inGame(ctx.message.author) != None:
            await self.bot.say("Your already in a game cant create a new one!")
        else:
            gme = RouletteLogic(bot=self.bot,channel=ctx.message.channel,gameName=gameNameInput)
            gme.addPlayer(ctx.message.author)
            self.games[gameNameInput] = gme
            await self.bot.say("Starting Game " + gameNameInput)
            
        await self.bot.delete_message(ctx.message)
        
    @gameR.command(pass_context = True)
    async def join(self,ctx,gameId : str):
        #self.bot.delete_message(ctx.message)
        if self.inGame(ctx.message.author) != None:
            await self.bot.say("Your already in a game cant join a new one!")
            return   
    
        if gameId in self.games:
            if self.games[gameId].isReady():
                self.games[gameId].addPlayer(ctx.message.author)
            else:
                await self.bot.say("Game is running and cant be joined")
        else:
            await self.bot.say("Game not found")
    
    @gameR.command(pass_context = True)
    async def players(self,ctx,gameId : str):
        
        if gameId in self.games:
            await self.bot.say("Current players in this game : " + self.games[gameId].getPlayers())
        else:
            await self.bot.say("Game not found")
            
        await self.bot.delete_message(ctx.message)
    
    @gameR.command(pass_context = True)
    async def newMsg(self,ctx):
        
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
        else:
            game.setNewMsg()
        
        await self.bot.delete_message(ctx.message)
        
    @gameR.command(pass_context = True)
    async def leave(self,ctx):
        await self.bot.delete_message(ctx.message)
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return

        if game.isReady():
            game.removePlayer(ctx.message.author)
            
            if game.getNumPlayers() == 0:
                 del self.games[game.gameName]
                 await self.bot.say("Game : " + game.gameName + " was deleted due to no players")  
        else:
            await self.bot.say("Game is running you cant leave")
            

            
def setup(bot):
    bot.add_cog(Roulette(bot))