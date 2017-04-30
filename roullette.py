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
        commands = "\n list : display all running games"
        commands += "\n new : create a new game"
        commands += "\n join <gameId>: join a game that is ready"
        commands += "\n players <gameId>: list players in a game"
        commands += "\n -----IN GAME-----"
        commands += "\n start : start the game when you have enough players"
        commands += "\n fire : when its your turn shoot with out spinning"
        commands += "\n spin : spin the barrel then fire, each time you spin you fire once more, ie spin 3 times you'll fire 3 times"
        commands += "\n leave : if you not in the middle of a game leave the room"
        commands += "\n restart : set a game back to the wait mode once its finished"        
        commands += "\n room : If your in a room which room"        
        await self.bot.say("Commands are " + commands)    
    
    
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
    
    @gameR.command(pass_context = True)
    async def fire(self,ctx):
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return      
        game.fire(ctx.message.author)
     
    @gameR.command(pass_context = True)
    async def spin(self,ctx):
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return       
        game.spin(ctx.message.author)
     
    @gameR.command(pass_context = True)
    async def restart(self,ctx):
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return
        
        game.restart()
    
    
    @gameR.command(pass_context = True)
    async def afk(self,ctx):
        game = self.inGame(ctx.message.author)
        if game == None:
            await self.bot.say("Your not in a game!")
            return
        
        game.afk()
     
    @gameR.command(pass_context = True)
    async def list(self):
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
        
    @gameR.command(pass_context = True)
    async def join(self,ctx,gameId : str):
    
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
    
    @gameR.command(pass_context = True)
    async def leave(self,ctx):
    
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