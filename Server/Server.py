from Game import *
from SMsgMaker import *
from Player import *
import time
import select
import socket
import sys
import threading
import re
import os
import argparse

class Server:
        def __init__(self, playTimeout, minPlayers, lobbyTimeout):
                self.host = ''
                self.port = 36727
                self.backlog = 5
                self.bufsize = 1024
                self.server = None
                self.threads = []
                self.playTimeout = playTimeout
                self.lobbyTimeout = lobbyTimeout
                self.lobby = []  # list of player objects with sockets
                self.strikeCode = None
                self.minPlayers = minPlayers
                self.maxPlayers = 7
                self.maxConns = 35
                self.mode = ''
                self.msgMaker = SMsgMaker(self)
                self.mangleNum = 0
                self.game = None
                self.timer = None
                self.lobbyTimeoutTime = 0
                self.playTime = 0
                self.warlordTime = 0
                
        def startGame(self):
            if len(self.lobby) >= 3 and self.game is None:
                self.game = Game(self)
                self.timer = None
                self.game.setup()
        
        def strike(self, player, code):
            strik = self.msgMaker.makeStrik(player, code)
            self.sendToPlayer(strik, player)
                
            if player.strikes >= 3:
                self.kick(player)

        def kick(self, player):
            if player.atTable:
                player.status = 'd'
                player.numCards = '00'
                if self.game:
                    if player is self.game.activePlayer:
                        self.game.nextPlayer()

                    self.game.playedDeck.extend(player.hand)
                    player.hand = []
                    stabl = self.msgMaker.makeStabl()
                    self.sendToAll(stabl)
                    self.game.table.remove(player)
                    self.game.gameTable.remove(player)
                        
                        
                    
                    
                #self.game.table.remove(player)
            
            if player in self.lobby:
                self.lobby.remove(player)
                if self.lobby:
                    slobb = self.msgMaker.makeSlobb()
                    self.sendToAll(slobb)
            player.sock.close()
            for kplayer in self.socks:
                if kplayer is not self.server:
                    if kplayer.name == player.name:
                        self.socks.remove(kplayer)
            print "{0} kicked from server.".format(player.name)
            
            
        def mangleName(self, newPlayer):

            if len(str(self.mangleNum)) == 1:
                mangleNumStr = '0' + str(self.mangleNum)
            else:
                mangleNumStr = str(self.mangleNum)

            self.mangleNum += 1

            mangleName = newPlayer.name.strip() #+ mangleNumStr

            if len(mangleName) > 6:
                            mangleName = mangleName[0:6]
                            
            mangleName += mangleNumStr
            
            while len(mangleName) < 8:
                mangleName += ' '
            
            newPlayer.name = mangleName

        def addPlayerToLobby(self, player, name):

            newPlayer = player
            newPlayer.name = name
            
            for player in self.lobby:
                if newPlayer.name == player.name:
                    self.mangleName(newPlayer)
                    break
            if self.game:
                for player in self.game.table:
                    if newPlayer.name == player.name:
                        self.mangleName(newPlayer)
                        break

            
            # make sjoin string msg based on attributes of player
            sjoin = self.msgMaker.makeSjoin(newPlayer)
            self.sendToPlayer(sjoin, newPlayer)


            # append the player to the lobby
            self.lobby.append(newPlayer)
                

            # make slobb string msg based on attributes of lobby
            slobb = self.msgMaker.makeSlobb()
            self.sendToAll(slobb)

            
            if len(self.lobby) >= self.minPlayers and not self.game and self.timer is None:
                self.lobbyTimeoutTime = int(time.time())
                print "Lobby Timeout Started"
            else:
                self.lobbyTimeoutTime = 0
                
            if len(self.lobby) >= 7:
                    self.startGame()
            
            
            
            

        def open_socket(self):
                try:
                        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        self.server.bind((self.host, self.port))
                        self.server.listen(5)
                except socket.error, message:
                        if self.server:
                                self.server.close()
                        print 'Could not open socket: ', message
                        sys.exit(1)
        
        def theTimer(self):
            while self.running:
                try:
                    
                        
                    if self.lobbyTimeoutTime != 0:
                        currentTime = time.time()
                        timeElapsed = currentTime - self.lobbyTimeoutTime
                        if timeElapsed > self.lobbyTimeout and len(self.lobby) >= 3:
                            self.startGame()
                            self.lobbyTimeoutTime = 0

                    if self.game:
                        if len(self.game.table) < 3:
                            self.game.close()
                            self.game = None
                            print "Game Closed"
                            slobb = self.msgMaker.makeSlobb()
                            self.sendToAll(slobb)
                            
                        if self.playTime != 0:
                            currentTime = time.time()
                            timeElapsed = currentTime - self.playTime
                            if timeElapsed > self.playTimeout and timeElapsed < 100:
                                self.playTime = 0
                                self.game.playerTimeout(self.game.activePlayer)
                                
                        if self.warlordTime != 0:
                            currentTime = time.time()
                            timeElapsed = currentTime - self.warlordTime
                            if timeElapsed > self.playTimeout and timeElapsed < 100:
                                self.playTime = 0
                                self.game.warlordTimeout()
                except:
                    break
                        
        
        
        
        def run(self):
            
            self.open_socket()
            self.running = 1
            self.lobbyTimeoutTime = 0
            self.timerThread = threading.Thread(target=self.theTimer)
            self.timerThread.start()
            print "Server is running..."
            self.socks = [self.server, sys.stdin]

            while self.running:

                read_players, write_players, error_socks = select.select(self.socks, [], [])
                
                for player in read_players:
                        if player == self.server:  # new connection
                                new_sock, addr = player.accept()
                                print "Connected by ", addr
                                new_player = Player(new_sock)
                                self.socks.append(new_player)
                                        
                                if len(self.socks) > self.maxConns:
                                        #too many connections
                                        self.strike(new_player, '81')
                                        self.kick(new_player)
                                        
                        elif player is sys.stdin:  # this will work on linux, not windows
                                junk = sys.stdin.readline()
                                if junk:
                                    self.running = 0
                                    self.server.close()
                                    break
                        else:  # new message
                                try:
                                        msg = player.sock.recv(self.bufsize)
                                        msgs = msg.split('][')
                                        for msg in msgs:
                                            if msg == '':
                                                self.kick(player)
                                                break
                                            else:
                                                if msg[0] != '[':
                                                    msg = '['+msg
                                                if msg[-1] != ']':
                                                    msg += ']'
                                            print 'Recv: ' + msg + ' from ' + player.name
                                            self.interpMsg(player, msg)
                                except socket.error, message:
                                        print "Socket error: ", message
                                        self.kick(player)
                


        def interpMsg(self, player, msg):

                cjoinRegex = '\[cjoin\|[a-zA-Z\_](\w|\s){7}\]'
                cchatRegex = '\[cchat\|(.|\s){63}\]'
                cplayRegex = '\[cplay\|((([0-4]\d)|(5[0-2])),){3}(([0-4]\d)|(5[0-2]))]'
                chandRegex = '\[chand\]'
                cswapRegex = '\[cswap\|(([0-4]\d)|(5[0-1]))\]'

                cjoinMatch = re.match(cjoinRegex, msg)
                cchatMatch = re.match(cchatRegex, msg)
                cplayMatch = re.match(cplayRegex, msg)
                chandMatch = re.match(chandRegex, msg)
                cswapMatch = re.match(cswapRegex, msg)
                
                if cjoinMatch and player.name == 'new':
                    name = msg[7:-1]
                    self.addPlayerToLobby(player, name)

                elif cchatMatch and player.name != 'new':

                        chat = msg[7:-1]
                        schat = self.msgMaker.makeSchat(player, chat)
                        self.sendToAll(schat)
                        
                elif cplayMatch:
                    self.playTime = 0
                    if not self.game:
                        self.strike(player, '31')
                    elif player.isActive:
                        strPlay = msg[7:-1]
                        strCards = strPlay.split(',')
                        thePlay = []
                        for card in strCards:
                            thePlay.append(card)

                        self.game.play(player, thePlay)
                        self.playTime = int(time.time())
                        
                        stabl = self.msgMaker.makeStabl()
                        self.sendToAll(stabl)
                    else:
                        if player not in self.game.table:
                            self.strike(player, '31')
                        else:
                            self.strike(player, '15')
                            
                        
                elif cswapMatch and player.warlordSwap:
                                        
                    self.warlordTime = 0

                    cardStr = msg[7:-1]
                    wcard = cardStr
                    self.game.swap(wcard)
                    
                    self.playTime = time.time()
                    
                    stabl = self.msgMaker.makeStabl()
                    self.sendToAll(stabl)
                    
                elif chandMatch == 'chand' and player.atTable:

                    shand = self.msgMaker.makeShand(player.hand)
                    self.sendToPlayer(shand, player)

                else:
                        self.strikeCode = '33'
                        self.strike(player, '33')


        # send msg to all clients
        def sendToAll(self, msg):
            for player in self.socks:
                if player is not self.server and player is not sys.stdin:
                    try:
                        player.sock.send(msg)
                    except socket.error, message:
                        print "player did not receive message ", message
            print 'Sent: ' + msg + ' to all players.'
            
        def sendToTable(self, msg):
            for player in self.table.players:
                try:
                    player.sock.send(msg)
                except socket.error, message:
                    print "player did not receive message ", message
            print 'Sent: ' + msg + ' to table.'

                # send msg to client
        def sendToPlayer(self, msg, player):
            try:
                player.sock.send(msg)
                print 'Sent: ' + msg + ' to ' + player.name
            except socket.error, message:
                print "player did not receive message: ", message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get command line parameters.')
    parser.add_argument('-t', nargs='?', const=15, type=int, default=15)
    parser.add_argument('-m', nargs='?', const=3, type=int, default=3)
    parser.add_argument('-l', nargs='?', const=15, type=int, default=15)

    args = parser.parse_args()
    theServer = Server(args.t, args.m, args.l)
    theServer.run()


#=================================================================================================================
