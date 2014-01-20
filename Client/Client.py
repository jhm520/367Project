from Player import *
from socket import *
import threading
import sys
import time
import select
import argparse
import os

#change of plans, start the client by running the GUI first, which starts the client program in a seperate thread
import pygame
from pygame.locals import *

class Gui:

    def __init__(self, client=None):
        pygame.init()

        #the GUI should reference the client, but never modify it
        self.client = client
        self.bg = pygame.image.load(os.path.join('data', 'map.png'))

        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Warlords")
        pygame.mouse.set_visible(1)

        #make icon invisible
        icon = pygame.Surface((1,1));
        icon.set_alpha(0);
        pygame.display.set_icon(icon)
         
        self.clock = pygame.time.Clock()

    def draw(self):

        self.screen.blit(self.bg, (0,0))
        pygame.display.update()
        

##    def run(self):
##
##        running = True
##        while running:
##            keystate = pygame.key.get_pressed()
##            for event in pygame.event.get():
##                if event.type == QUIT or keystate[K_ESCAPE]:
##                    pygame.quit()
##                    running = False
##                    sys.exit()
##            self.draw()
##            self.clock.tick(100)


class Client:
    def __init__(self, host, port, name, manual):
        self.host = host
        self.port = port
        self.name = name
        self.sock = None
        self.bufsize = 512
        self.timeout = 15
        self.isConnected = False
        self.lobby = []
        self.table = []
        self.lastPlay = []
        self.firstRound = None
        self.player = None
        self.hand = []
        self.manual = manual
        self.socks = []
        self.strikes = 0
        self.msgQueue = []
        self.wcard = None
        self.scard = None
        self.active = False
        self.swapping = False

        #initialize GUI
        self.gui = Gui(self)

        
    def connect(self):
                try:
                        self.sock = socket(AF_INET, SOCK_STREAM)
                        self.sock.connect((self.host,self.port))
                        self.sock.settimeout(15)
                        self.isConected = True
                        print ("Connected to ", self.sock.getpeername())
                except error, (value,message):
                #except error:
                        if self.sock:
                                self.sock.close()
                        print ("Could not open socket: ", message)
                        sys.exit(1)

    def makeCplay(self):

        handStr = ""
        for card in self.hand:
            handStr += card + ','
        print "Your hand:", handStr
        if self.manual == False:
            #last play rank
            lastRank = None
            #last play quantity
            lastPlayCards = []
            
            for card in self.lastPlay:
                if card != '52':
                    lastPlayCards.append(card)
                    if lastRank == None:
                        lastRank = int(card)/4


            if self.firstRound == 1:
                cplay = '[cplay|00,52,52,52]'
                self.hand.remove('00')           
                return cplay

            if lastRank is None:
                theCard = self.hand.pop()
                cplay = '[cplay|' + theCard + ",52,52,52]"
                return cplay
             
            badRanks = []
            thePlayCards = []
            theRank = None
            done = False
            
            while not done:
                for card in self.hand:
                    if theRank is None and int(card)/4 >= lastRank and int(card)/4 not in badRanks:
                        theRank = int(card)/4

                    if int(card)/4 == theRank:
                        if card not in thePlayCards:
                            thePlayCards.append(card)
                    
                    if len(thePlayCards) >= len(lastPlayCards):
                        done = True
                        break
                    
                    if card is self.hand[-1]:
                        if theRank is None:
                            done = True
                            break
                        else:    
                            badRanks.append(int(card)/4)
                            theRank = None
                            thePlayCards = []
 

            for card in thePlayCards:
                self.hand.remove(card)
            
            while len(thePlayCards) < 4:
                thePlayCards.append('52')

            
            cplay = '[cplay|' + thePlayCards[0] + ',' + thePlayCards[1] + ',' + thePlayCards[2] + ',' + thePlayCards[3] + ']'

            return cplay
        
        else:
            self.active = True
            print "It is your turn"
            handStr = ""
            for card in self.hand:
                handStr += card + ','
            print "Your hand:", handStr
            lastPlayStr = ""
            for card in self.lastPlay:
                lastPlayStr += card + ","
            print "LastPlay", lastPlayStr
            print "Input card numbers ex. '52,52,52,52': "
            #cplay = "[cplay|"+cplaycards+"]"
            #return cplay
        
        
    
    def getPlayer(self,name):
        for player in self.table:
            if player.name == name:
                return player
    
    def updateLobby(self, msg):
        self.lobby = []
        msgNames = msg[10:-1]
        names = msgNames.split(',')
        
        for name in names:
            name = name[0:8]
            self.lobby.append(name)
    
    def updateTable(self, msg):
        #generate image of table
        self.table = []
        msg = msg[1:-1]
        majorfields = msg.split('|')
        tablePlayerStr = majorfields[1]
        lastPlayStr = majorfields[2]
        firstRoundStr = majorfields[3]
        
        playerfields = tablePlayerStr.split(',')
        for playerStr in playerfields:
            minorfields = playerStr.split(':')
            nameStr = minorfields[1]
            newPlayer = Player()
            newPlayer.name = nameStr
            newPlayer.status = minorfields[0][0]
            newPlayer.strikes = minorfields[0][1]
            newPlayer.numCards = minorfields[2]
            if newPlayer.name == self.name:
                self.player = newPlayer
        
        lastPlayCardStrs = lastPlayStr.split(',')
        self.lastPlay = []
        for card in lastPlayCardStrs:
            self.lastPlay.append(card)
        
        self.firstRound = int(firstRoundStr)
            
            
            
            
        if self.player:
            if self.player.status == 'a':
                cplay = self.makeCplay()
                time.sleep(.1)
                self.sock.send(cplay)
                print "Sent:", cplay
                
                
    def updateHand(self, msg):
        self.hand = []
        msg = msg[1:-1]           
        majorfields = msg.split('|')
        handStr = majorfields[1]
        
        cardStrs = handStr.split(',')
        
        for card in cardStrs:
            self.hand.append(card)
        
        
            
    def makeCswap(self):
        if self.manual:
            handStr = ""
            for card in self.hand:
                handStr += card + ','
            print "Your hand:", handStr
            print "Input Warlord swap card number: "
            self.swapping = True
            
        else:
            wcard = self.hand.pop(0)
        
        cswap = '[cswap|' + wcard + ']'
        
        return cswap
    
    def makeCchat(self, msg):
        cchat = '[cchat|'
        
        while len(msg) < 63:
            msg += ' '
        
        cchat += msg + ']'
        
        return cchat
    
    def interpMsg(self, msg):
        
        msgRaw = msg
        msgHeader = msg[1:6]
        msgBody = msg[7:-1]
        
        
        if msgHeader == 'slobb':
            
            
            self.updateLobby(msg)
        
        elif msgHeader == 'stabl':
            self.updateTable(msg)
        
        elif msgHeader == 'shand':
            self.updateHand(msg)
            
        elif msgHeader == 'swapw':
            print "Received card from scumbag", msgBody

            self.hand.append(msgBody)

            if self.manual == False:
                cswap = self.makeCswap()
                time.sleep(.1)
                self.sock.send(cswap)
                print "Sent:", cswap
        
        elif msgHeader == 'schat':
            pass
            
        elif msgHeader == 'swaps':
            swapCards = msgBody.split('|')  
            recvCard = swapCards[0]
            giveCard = swapCards[1]
            
            print "Received card from warlord", recvCard
            print "Gave card to warlord:", giveCard

        
        elif msgHeader == 'sjoin':
            self.name = msgBody
        
        elif msgHeader == 'strik':
            self.strikes += 1
        
        else:
            print "Recieved unknown command"
            sys.exit()
            
            
    def input(self):
        while 1:
            read = raw_input("Input Message")
            if read:
                cchat = self.makeCchat(read)
                time.sleep(.1)
                self.sock.send(cchat)
                    
    def run(self):
        while len(self.name) != 8:
            self.name += ' '

        cjoin = '[cjoin|' + self.name + ']'
        self.connect()
        time.sleep(.1)
        self.sock.sendall(cjoin)
        #self.socks = [self.sock, sys.stdin]
        self.socks = [self.sock]

        
        
        
        while 1:
#             if self.msgQueue:
#                 self.interpMsg(self.msgQueue.pop(0))

            #Draw everything
            self.gui.draw()
            
            
            read_socks, write_socks, error_socks = select.select(self.socks, [], [])
            for sock in read_socks:
                if sock is self.sock:
                    msg = self.sock.recv(self.bufsize)
                    msgs = msg.split('][')
                    for msg in msgs:
                        if msg == '':
                            break
                        else:
                            if msg[0] != '[':
                                msg = '['+msg
                            if msg[-1] != ']':
                                msg += ']'
                            print "Recv:", msg
                            self.interpMsg(msg)
                elif sock is sys.stdin:
                    if self.manual:
                        if self.active:
                            cplaycards = sys.stdin.readline()
                            cplay = "[cplay|"+cplaycards+"]"
                            self.sock.send(cplay)
                            self.active = False
                        elif self.swapping:
                            swapcard = sys.stdin.readline()
                            self.hand.remove(swapcard)
                            cswap = "[cswap|" + swapcard + "]"
                            self.sock.send(cswap)
                            self.swapping = False
                        else:
                            msg = sys.stdin.readline()
                            if msg == "exit\n":
                                self.sock.close()
                                sys.exit()
                            else:
                                
                                cchat = self.makeCchat(msg)
                                self.sock.send(cchat)
                    else:
                        self.sock.close()
                        sys.exit()
                        
            
            if self.strikes >= 3:
                break
            
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get command line parameters.')
    parser.add_argument('-s', nargs='?', const='localhost', type=str, default='localhost')
    parser.add_argument('-p', nargs='?', const=36727, type=int, default=36727)
    parser.add_argument('-n', nargs='?', const='john', type=str, default='john')
    parser.add_argument('-m', action='store_true')
    

    args = parser.parse_args()

    theClient = Client(args.s, args.p, args.n, args.m)
    theClient.run()
                
