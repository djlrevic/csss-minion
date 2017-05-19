import discord
import time
import threading
import asyncio
from random import randint

class GameLogic():

    def __init__(self,bot,channel,gameName):
        #I couldnt get static vars working so I made them local
        self.gameState_wait = 0
        self.gameState_running = 1
        self.gameState_end = 2
        self.gameStartMin = 1
        #How long to wait before starting the game after the min amount of people join
        self.readyWaitLength = 30
        self.afkTimer = 10
        self.channel = channel
        self.players = []
        self.gameState = self.gameState_wait
        self.readToStart = False
        self.bot = bot
        self.gameName = gameName
        self.newMsg = True
        self.curMsg = None
        self.future = None
        
    #Because all of thease run in a courutine I need to run in in this weird way
    #I think its basically queueing an action on the thread the bot uses for server interaction
    #But I could be wrong, either way with out asyncio call it wont work
    def sendMsg(self,txt):
        #Do we need to send a new msg? Or just edit the old one
        print("attempt to msg")
        if self.newMsg:
            #Lets hope this works
            self.future = asyncio.run_coroutine_threadsafe(self.bot.send_message(self.channel, txt), self.bot.loop)
            
            try:
                self.curMsg = self.future.result(5)
            except asyncio.TimeoutError:
                print('The coroutine took too long, cancelling the task...')
                self.future.cancel()
            except Exception as exc:
                print('The coroutine raised an exception: {!r}'.format(exc))
            else:
                print('The coroutine worked')
            
            self.newMsg = False
        else:
            #Append to the current msg
            try:
                self.curMsg = self.future.result(5)
            except asyncio.TimeoutError:
                print('The coroutine took too long, cancelling the task...')
                self.future.cancel()
            except Exception as exc:
                print('The coroutine raised an exception: {!r}'.format(exc))
            else:
                print('The coroutine worked')
            
            self.editMsg(self.curMsg,'\n'+txt)
            
            
    def setNewMsg(self):
        self.newMsg = True
 
    def editMsg(self,msg,txt):
        asyncio.run_coroutine_threadsafe(self.bot.edit_message(msg,txt), self.bot.loop)
        
    def removeMsg(self,msg):
        asyncio.run_coroutine_threadsafe(self.bot.delete_message(msg), self.bot.loop)   
    
    def isReady(self):
        return self.gameState != self.gameState_running
    
    def getNumPlayers(self):
        return len(self.players)
    
    def startGame(self):
        self.gameState = self.gameState_running
        self.sendMsg("Game " + self.gameName + " has started")
        #await self.bot.send_message(self.channel, "HENRY THE GREATEST")
        #pass      
            
    def getPlayers(self):
        playersStr = ""
        for mem in self.players:
            playersStr += " " + getName(mem)
        
        return playersStr
    
    def update(self):
        pass

    def tick(self):
        #Tick means we are waiting for a time based event, we dont want to just do time sleep because this is the main thread
        if self.gameState == self.gameState_wait and self.readToStart == True:
            self.startGame()
        elif self.gameState == self.gameState_running:
            #Dunno Do something
            pass
        else:
            pass
        
    def removePlayer(self,player):
        if player in self.players:
            if self.gameState != self.gameState_running:
                    self.players.remove(player)
                    self.sendMsg(getName(player) + " has been removed from the game")
            else:
                self.sendMsg("You cant leave " + getName(player) + " your still in the game")
                print("Cant remove a player thats in a playing game")
        else:
            self.sendMsg("Your not even in this game")
    
    def addPlayer(self,player):
        #All players are the memeber class
        if not self.gameState == self.gameState_wait:
            self.sendMsg("Cant join a running game")
        else:
            
            if player in self.players:
                self.sendMsg("Your already in this game")
                return
        
            self.players.append(player)
            self.sendMsg(getName(player) + "has joined game +" + self.gameName + "\n" + "Game has " + str(len(self.players)) + "players")
            
            
            if len(self.players) >= self.gameStartMin:            
                pass
                ###
                #thread = threading.Thread(target=wait, args=(5, self))
                #thread.start()
                ###
                #self.readToStart = True
                
class RouletteLogic(GameLogic):
    def __init__(self,bot,channel,gameName):
        super().__init__(bot,channel,gameName)
        #Who's Turn it is
        self.timesSpun = []
        self.turn = 0
        self.playerToGo = None
        self.sendMsg("Starting waiting room of Roulette")
        self.bulletPos = randint(0,5)
    
    #Overide the add and remove so I can add/remove to/from the spin counter
    
    def addPlayer(self,player):
        #All players are the memeber class
        if not self.gameState == self.gameState_wait:
            self.sendMsg("Cant join a running game")
        else:
            if player in self.players:
                self.sendMsg("Your already in this game")
                return
        
        self.players.append(player)
        self.timesSpun.append(0)
        self.sendMsg(getName(player) + "has joined game +" + self.gameName + "\n" + "Game has " + str(len(self.players)) + "players")
    
        
    def removePlayer(self,player):
        if player in self.players:
            if self.gameState != self.gameState_running:
                #Remove the the index of times spun by looking for the index of player pos
                del self.timesSpun[self.players.index(player)]
                self.players.remove(player)
                self.sendMsg(getName(player) + " has been removed from the game")
            else:
                self.sendMsg("You cant leave " + getName(player) + " your still in the game")
                print("Cant remove a player thats in a playing game")
        else:
            self.sendMsg("Your not even in this game")
    
    def afk(self):
        pass
    
    def update(self):
        pass

    def startGame(self):
        super().startGame()
        self.turn = randint(0,len(self.players) - 1)
        self.playerToGo = self.players[self.turn]
        self.sendMsg(getName(self.playerToGo)  + " has first go")
        
        pass
        
    def killPlayer(self,player):
        #Cant mute, so lets just kick them ;)
        #self.bot.kick(player)
        self.sendMsg("This is the part were your kicked but for testing I wont ")
    
    def doSpin(self):
        self.timesSpun[self.turn]+=1
        spinAmount = self.timesSpun[self.turn]
        self.sendMsg("The barrel spins and the player will fire " + str(spinAmount) + " times")
        self.bulletPos = randint(0,5)
        
        curSpin = 0
        
        #Spin untill we have done the required amount or we die
        while curSpin < spinAmount and self.gameState != self.gameState_end:
            self.doFire()
            curSpin+=1
    
    def doFire(self):
        if self.bulletPos == 0:
            #Boom
            self.sendMsg("BOOM")
            self.sendMsg(getName(self.players[self.turn]) + " blew their brains out ")
            self.killPlayer(self.players[self.turn])
            self.gameState = self.gameState_end
            pass
        else:
            self.sendMsg("CLICK")
            self.bulletPos -= 1
            
            
    def nextPlayer(self):
        if self.turn == 0:
            self.turn = len(self.players) - 1
        else:
            self.turn -= 1
        
        self.sendMsg("Its " + getName(self.players[self.turn]) + " turn now")
        self.playerToGo = self.players[self.turn]
    
    def fire(self,player):
        if player != self.playerToGo:
            self.sendMsg("Its not your turn!")
        elif self.gameState == self.gameState_running:
            self.doFire()
            #Check to see if the game ended
            if not self.gameState == self.gameState_end:
                self.nextPlayer()
        else:
            self.sendMsg("Game hasnt started yet or is over")
        pass
    
    def spin(self,player):
        if player != self.playerToGo:
            self.sendMsg("Its not your turn!")
        elif self.gameState == self.gameState_running:
            self.doSpin()
            
            #Check if they killed them selves
            if not self.gameState == self.gameState_end:
                self.nextPlayer()
        else:
            self.sendMsg("Game hasnt started yet!")
        
    
    def start(self):
        if len(self.players) < self.gameStartMin:
            self.sendMsg("Not enought players yet needs " + str(self.gameStartMin))
        elif self.gameState != self.gameState_wait:
            self.sendMsg("You cant start the game now silly")
        else:
            self.readToStart = True
            self.startGame()
        
    
    def restart(self):
        if self.gameState != self.gameState_end:
            self.sendMsg("Game is still running you ass")
        else:
            for i in range(len(self.timesSpun)):
                self.timesSpun[i] = 0
                
            self.gameState = self.gameState_wait
            self.bulletPos = randint(0,5)
            self.sendMsg("Game has reset, start when your ready")                      
    
    
def getName(player):
    if player.nick == None:
        return player.name
    else:
        return player.nick

def wait(timeToSleep,toWake):
    time.sleep(timeToSleep)
    toWake.tick()
