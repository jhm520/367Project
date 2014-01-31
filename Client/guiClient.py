import pygame
from pygame.locals import *
import os
import sys
import argparse
import eztext
from Client import *

class Gui:

    def __init__(self, host, port, name, manual):
        self.client = Client(host, port, name, manual)
            
        pygame.init()

        #the GUI should reference the client, but never modify it
        #self.bg = pygame.image.load(os.path.join('data', 'map.png'))

        self.screen = pygame.display.set_mode((640, 480))
    
        pygame.display.set_caption("Warlords")
        pygame.mouse.set_visible(1)

        #make icon invisible
        icon = pygame.Surface((1,1))
        icon.set_alpha(0)
        pygame.display.set_icon(icon) 
        
        self.clock = pygame.time.Clock()
        
        

        self.font = pygame.font.SysFont(None,16)
        self.font2 = pygame.font.SysFont(None,64)
        self.font3 = pygame.font.SysFont(None,32)

        self.chatTextBox = eztext.Input(x=5, y=460, font=self.font, maxlength=63, color=(0,0,0), prompt='Chat: ')
        self.playTextBox = eztext.Input(x=210, y=400, font=self.font, maxlength=20, color=(255,0,0), prompt='Input Play:')
        self.swapTextBox = eztext.Input(x=210, y=420, font=self.font, maxlength=2, color=(255,0,0), prompt='Input Card to Swap:')

    def draw(self):
        #draw background
        #self.screen.blit(self.bg, (0,0))
        self.screen.fill((0,150,0))
        pygame.draw.line(self.screen, (0,0,0), (0, 320), (640, 320), 2)
        pygame.draw.line(self.screen, (0,0,0), (480, 0), (480, 320), 2)
        pygame.draw.line(self.screen, (0,0,0), (200, 320), (200, 480), 2)


        #draw connection info
        if self.client.isConnected:
            connectText = self.font.render("Connected to {0} on port {1} as {2} in {3} mode.".format(str(self.client.host), str(self.client.port),self.client.name.strip(), self.client.mode), True, (0,0,0))
            #draw lobby
            lobbyText = self.font.render("Lobby (" + str(len(self.client.lobby)) + ")", True, (0,0,0))
            self.screen.blit(lobbyText,(490,10))
            
            if self.client.lobby:
                ypos = 30
                for player in self.client.lobby:
                    playerText = self.font.render(player, True, (0,0,0))
                    self.screen.blit(playerText, (500,ypos))
                    ypos += 20
            
            if self.client.table:
                
                #Draw gameInProgress
                gameInProgressText = self.font.render("Game currently in progress", True, (0,0,0))
                
                #draw table
                tableDrawPositions = [(100,100), (200,100), (300,100), (350, 150), (250, 200), (150, 200), (50, 150)]
                tableActiveMarker = self.font.render(">", True, (0,0,0))
                posCnt = 0

                for player in self.client.table:
                    pos = tableDrawPositions[posCnt]
                    tablePlayerText = self.font.render(player.name, True, (0,0,0))
                    tablePlayerNumCards = self.font.render(player.numCards, True, (0,0,0))
                    tablePlayerStrikes = self.font.render(player.strikes, True, (0,0,0))
                    tablePlayerStatus = self.font.render(player.status, True, (0,0,0))
                    self.screen.blit(tablePlayerText, pos)
                    self.screen.blit(tablePlayerNumCards, (pos[0], pos[1] + 15))
                    self.screen.blit(tablePlayerStrikes, (pos[0]+15, pos[1] + 15))
                    self.screen.blit(tablePlayerStatus, (pos[0]+30, pos[1]+15))
                    
                    if player.status == "a":
                        self.screen.blit(tableActiveMarker, (pos[0]-10, pos[1]))
                    if player is self.client.player:
                        tableYouMarker = self.font.render("<- You!", True, (255,0,0))
                        self.screen.blit(tableYouMarker, (pos[0]+50, pos[1]))
                    posCnt += 1


                cardDrawPositions = [(175,150), (200, 150),(225, 150), (250,150)]
                if self.client.lastPlay:
                    posCnt = 0
                    for card in self.client.lastPlay:
                        tableCardText = self.font.render(card, True, (0,0,0))
                        self.screen.blit(tableCardText, cardDrawPositions[posCnt])
                        posCnt += 1

                #draw hand
                yourHandText = self.font.render("Your Hand:", True, (0,0,0))
                self.screen.blit(yourHandText, (210, 325))
                if self.client.hand:
                    posCnt = 0
                    for card in self.client.hand:
                        handCardText = self.font.render(card, True, (0,0,0))
                        if posCnt < 13:
                            self.screen.blit(handCardText, (275 + posCnt * 25, 325))
                        else:
                            self.screen.blit(handCardText, (275 + (posCnt-13) * 25, 345))
                        posCnt += 1


                
            else:
                gameInProgressText = self.font.render("Game not in progress.", True, (0,0,0))

            self.screen.blit(gameInProgressText, (5, 20))
        else:
            connectText = self.font.render("Not connected.", True, (0,0,0))

        
        self.screen.blit(connectText,(5,5))

        if self.client.manual:
            if self.client.active:
                self.playTextBox.draw(self.screen)
        #draw chatTextBox
            elif self.client.swapping:
                #draw swap box
                self.swapTextBox.draw(self.screen)
            else:
                self.chatTextBox.draw(self.screen)
            
        

        #draw chat
        if self.client.chatLog:
            ypos = 350
            for chat in self.client.chatLog:
                name = chat[0:8]
                msg = chat[9:]
                chatText = self.font.render(">{0}: {1}".format(name, msg), True, (0,0,0))
                self.screen.blit(chatText, (5, ypos))
                ypos += 20
                
        pygame.display.update()

    def run(self):
        self.running = 1
        self.clientThread = threading.Thread(target=self.client.run)
        self.clientThread.start() #yay this works!
        #self.clientThread.join()
        
        while self.running:
            keystate = pygame.key.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or keystate[K_ESCAPE]:
                    self.client.close()
                    self.running = 0
            self.draw()
            self.clock.tick(100)
            text = None
            if self.client.manual:
            #get text input
                if self.client.active:
                    text = self.playTextBox.update(events)
                    if text:
                        if text == "pass":
                            cplay = "[cplay|52,52,52,52]"
                        else:
                            cards = text.split()
##                            for card in cards:
##                                if card in self.client.hand:
##                                    self.client.hand.remove(card)
                            while len(cards) < 4:
                                cards.append('52')
                            cplay = "[cplay|{0},{1},{2},{3}]".format(cards[0],cards[1],cards[2],cards[3])
                        self.client.sock.send(cplay)
                        self.client.active = False
                        self.client.sock.send("[chand]")
                elif self.client.swapping:
                    text = self.swapTextBox.update(events)
                    if text:
                        cswap = '[cswap|' + text + ']'
                        self.client.sock.send(cswap)
                        self.client.swapping = False
                else:
                    text = self.chatTextBox.update(events)
                #if text is input
                    if text:
                        if self.client.isConnected:
                            cchat = self.client.makeCchat(text)
                            self.client.sock.send(cchat)
            
            
        pygame.quit()
        self.clientThread.join()
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get command line parameters.')
    parser.add_argument('-s', nargs='?', const='localhost', type=str, default='localhost')
    parser.add_argument('-p', nargs='?', const=36727, type=int, default=36727)
    parser.add_argument('-n', nargs='?', const='johnnash', type=str, default='johnnash')
    parser.add_argument('-m', action='store_true')
    

    args = parser.parse_args()

    #testGui = Gui(args.s, args.p, args.n, args.m)
    testGui = Gui(args.s, args.p, args.n, 1)
    testGui.run()
