import threading
from random import shuffle
import sys
import time



class Game:
    def __init__(self, server):
        self.table = [] #list of players
        self.gameTable = [] #list of players who still have cards
        
        self.warlord = None
        self.scumbag = None
        self.firstRound = 1
        self.server = server
        self.lastPlay = []
        self.lastPlayer = None
        self.timeout = None
        self.scard = None
        self.wcard = None
        self.activePlayer = None #the active player "self.table[activePlayerCnt]"
        self.activePlayerCnt = 0 #index of player whos turn it is

    
    
    
    
    def playerTimeout(self, player):
        if self.server.game:
            if player:
                self.server.strike(player, '20')
                self.nextPlayer()
                player.status = 'p'
                self.playTime = 0
                stabl = self.server.msgMaker.makeStabl()
                self.server.sendToAll(stabl)

    
    #called at the end of the timer
    def warlordTimeout(self):
        #self.timeout = None
        if self.server.game:
            self.server.strike(self.warlord, '20')

    
    #deal cards
    def dealCards(self):
        #make the deck
        self.deck = []
        for i in range(0, 52):
            if len(str(i)) == 1:
                card = '0' + str(i)
            else:
                card = str(i)
            #self.deck.append(Card(str(i)))
            self.deck.append(card)
        
        #shuffle the deck
        shuffle(self.deck)
        
        #deal cards
        for i in range(52):
            for player in self.table:
                if not self.deck:
                    break
                player.hand.append(self.deck.pop())
        
        for player in self.table:
            if player is not self.scumbag:
                shand = self.server.msgMaker.makeShand(player.hand)
                self.server.sendToPlayer(shand, player)

    
    def setup(self):
        self.gameTable = []
        
        while len(self.table) < 7 and len(self.server.lobby) > 0:
            thePlayer = self.server.lobby.pop(0)
            thePlayer.atTable = True
            self.table.append(thePlayer)
            
        self.dealCards()


        for player in self.table:
            self.gameTable.append(player)
        
        if self.firstRound:
            threeClubs = '00'
            for player in self.table:
                if threeClubs in player.hand:
                    player.status = 'a'
                    self.activePlayer = player
                    self.activePlayer.isActive = True
            
            self.lastPlay = ['52','52','52','52']
            self.playedDeck = []
            self.socialRank = 1


            self.server.playTime = time.time()
            
            stabl = self.server.msgMaker.makeStabl()
            self.server.sendToAll(stabl)
            
            
            
        else:
            
            #not starting round, take warlord out and place at front of list
            self.table.remove(self.warlord)
            self.table.insert(0, self.warlord)
            
            self.scumbag = self.table[-1]
            self.scumbag.isScumbag = True
            
            #take scumbag out and place at back of the list
            self.table.remove(self.scumbag)
            self.table.append(self.scumbag)
            
            #find high card in scumbag's hand
            highCard = None
            for card in self.scumbag.hand:
                if highCard is None:
                    highCard = card
                elif int(card) > int(highCard):
                    highCard = card
            
            
            self.scard = highCard
            self.scumbag.hand.remove(self.scard)


            self.warlord.hand.append(self.scard)
            
            swapw = self.server.msgMaker.makeSwapw(self.scard)
            self.server.sendToPlayer(swapw, self.warlord)
            self.warlord.warlordSwap = True
            
            print "Waiting for warlord to send cswap"
            
            self.server.warlordTime = time.time()
            
        
    def close(self):
        self.activePlayer = None
        self.warlord = None
        self.scumbag = None
        self.firstRound = 1
        self.lastPlay = []
        self.lastPlayer = None
        self.timeout = None
        self.scard = None
        self.wcard = None
        self.activePlayerCnt = 0
        for player in self.table:
            player.status = 'w'
            player.hand = []
            player.rank = 0
            player.atTable = False
            player.isActive = False
            player.numCards = '00'
            player.isWarlord = False
            player.isScumbag = False
            player.warlordSwap = False
            player.lastPlay = []
            self.server.lobby.append(player)
        self.table = []
        
                
    def nextPlayer(self):
        self.activePlayer.isActive = False
        self.activePlayer.status = 'w'
        
        while self.activePlayer.isActive == False:
            if self.activePlayerCnt >= len(self.table) - 1:
                self.activePlayerCnt = 0
            else:
                self.activePlayerCnt += 1

            if self.table[self.activePlayerCnt].hand:
                self.activePlayer = self.table[self.activePlayerCnt]
                self.activePlayer.isActive = True
                self.activePlayer.status = 'a'
                if self.activePlayer is self.lastPlayer:
                    self.lastPlay = ['52','52','52','52']
                    print "Last Play Reset"
                    

        self.playTime = time.time()
        print "Waiting for " + self.activePlayer.name + " to play"
    
    def playCards(self, player, thePlay, thePlayCards):
        self.lastPlay = thePlay
        self.lastPlayer = player
        self.playedDeck.extend(thePlayCards)
        
        
        for card in thePlayCards:
            player.hand.remove(card)

        
        #if player has played all their cards
        if not player.hand:
            self.lastPlayer = None
            self.lastPlay = ['52','52','52','52']
            player.rank = self.socialRank
            print player.name + " rank " + str(player.rank)
            self.socialRank += 1
            self.gameTable.remove(player)
        
        #player was first to play all his cards, is warlord
            if player.rank == 1:
                player.isWarlord = True
                self.warlord = player
                print self.warlord.name + " is warlord"


        



        #if there is one player left in the game, this last player is the scumbag, game is over, reset the table
            if len(self.gameTable) == 1:
                self.scumbag = self.gameTable[0]
                
                self.scumbag.isScumbag = True
                self.scumbag.status = 'w'
                self.scumbag.isActive = False
                self.gameTable.remove(self.scumbag)
                #self.playedDeck.extend(thePlayCards)
                self.scumbag.hand = []
                print self.scumbag.name + " is scumbag"
                self.table.remove(self.scumbag)
                self.table.append(self.scumbag)
                #reset table
                for kplayer in self.table:
                    kplayer.isActive = False
                    kplayer.status = "w"
                #self.activePlayer = None
                self.firstRound = 0
                self.lastPlayer = None
                self.setup()
                
        if self.scumbag is None:
            self.nextPlayer()

    def setScumbag(self):
        self.scumbag = self.gameTable[0]
        self.scumbag.isScumbag = True
        self.scumbag.status = 'w'
        self.scumbag.isActive = False
        self.gameTable.remove(self.scumbag)
        #self.playedDeck.extend(thePlayCards)
        self.scumbag.hand = []
        print self.scumbag.name + " is scumbag"
        self.table.remove(self.scumbag)
        self.table.append(self.scumbag)
        #reset table
        for kplayer in self.table:
            kplayer.isActive = False
            kplayer.status = "w"
        #self.activePlayer = None
        self.firstRound = 0
        self.lastPlayer = None
        self.setup()
        
        
    
    def play(self, player, thePlay):
        

        self.playTime = 0
        print self.activePlayer.name + "played"
        
        theRank = None
        thePlayCards = []
        
        
        #make sure cards have same rank, and all in the player's hand
        for card in thePlay:
            if card == '52':
                continue
            else:
                thePlayCards.append(card)
                if theRank is None:
                    theRank = int(card)/4
                

                if int(card)/4 != theRank:
                    #self.server.strikeCode = '11'
                    self.server.strike(player, '11')
                    return
                
                if card not in player.hand:
                    self.server.strike(player, '14')
                    return
                
        lastPlay = self.lastPlay
        lastPlayCards = []
        lastRank = None
        
        for card in lastPlay:
            if card == '52':
                continue
            else:
                lastPlayCards.append(card)
                if lastRank is None:
                    lastRank = int(card)/4
        
        #if its the first hand of the game, check to see if the play has the 3 of clubs
        if self.firstRound and not self.playedDeck:
            if '00' in thePlay:
                self.playCards(player, thePlay, thePlayCards)
                self.firstRound = 0
            else:
                self.server.strike(player, '16')
                return

        #if the play was all 52s, it was a pass
        elif theRank is None:
            if lastRank is None:
                self.server.strike(player, '18')
                return
            else:
                self.nextPlayer()
                player.status = 'p'
            
        
        #If the player played a 2, the player remains active
        elif theRank == 12:
            self.playCards(player, thePlay, thePlayCards)
            
        
        else:
            if len(thePlayCards) >= len(lastPlayCards):
                if theRank >= lastRank:
                    self.playCards(player, thePlay, thePlayCards)
                    if theRank == lastRank:
                        print "Player ", self.activePlayer.name, "skipped."
                        skippedPlayer = self.activePlayer
                        self.nextPlayer()
                        if skippedPlayer is not self.activePlayer:
                            skippedPlayer.status = 'p'
                    
                else:
                    #face value too low
                    self.server.strike(player, '12')
                    return
                    
            else:
                #too few cards sent
                self.server.strike(player, '13')
                return


       
                
                
    def swap(self, wcard):
        if wcard not in self.warlord.hand:
            self.server.strike(self.warlord, '70')
            return

        
        print "Warlord" + self.warlord.name + " swapped card"
            
        self.wcard = wcard
        
        #remove card from warlord's hand and place in scumbag's hand
        self.warlord.hand.remove(wcard)
        self.scumbag.hand.append(wcard)
        
        
        #send warlord his new hand
        shand = self.server.msgMaker.makeShand(self.warlord.hand)
        self.server.sendToPlayer(shand, self.warlord)
        
        #send scumbag his new hand
        shand = self.server.msgMaker.makeShand(self.scumbag.hand)
        self.server.sendToPlayer(shand, self.scumbag)
        
        #send scumbag swaps msg
        swaps = self.server.msgMaker.makeSwaps(self.scard, self.wcard)
        self.server.sendToPlayer(swaps, self.scumbag)
        
        #make the current warlord the active player
        self.activePlayer = self.warlord
        self.warlord.isActive = True
        self.warlord.status = 'a'
        self.activePlayerCnt = self.table.index(self.warlord)
        
        #reset the social order
        self.wcard = None
        self.scard = None
        
        self.scumbag.isScumbag = False
        self.scumbag = None
        
        self.warlord.warlordSwap = False
        self.warlord.isWarlord = False
        self.warlord = None
        
        
        for player in self.table:
            player.rank = 0
        
        self.lastPlay = ['52','52','52','52']
        self.playedDeck = []
        self.socialRank = 1
        
        
        
        
            
            
        
