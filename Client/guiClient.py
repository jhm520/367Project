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
        self.bg = pygame.image.load(os.path.join('data', 'map.png'))

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

        self.textBox = eztext.Input(x=5, y = 325, font=self.font, maxlength=63, color=(0,0,0), prompt='Chat: ')

    def draw(self):
        #draw background
        self.screen.blit(self.bg, (0,0))


        #draw connection info
        if self.client.isConnected:
            connectText = self.font.render("Connected to {0} on port {1} as {2} in {3} mode.".format(str(self.client.host), str(self.client.port),self.client.name, self.client.mode), True, (0,0,0))
        else:
            connectText = self.font.render("Not connected.", True, (0,0,0))

        self.screen.blit(connectText,(5,10))
        
        #draw lobby
        lobbyText = self.font.render("Lobby (" + str(len(self.client.lobby)) + ")", True, (0,0,0))
        self.screen.blit(lobbyText,(490,10))
        
        if self.client.lobby:
            ypos = 30
            for player in self.client.lobby:
                playerText = self.font.render(player, True, (0,0,0))
                self.screen.blit(playerText, (500,ypos))
                ypos += 20


        #draw textBox
        self.textBox.draw(self.screen)

        #draw chat
        if self.client.chatLog:
            ypos = 350
            for chat in self.client.chatLog:
                chatText = self.font.render("> " + chat, True, (0,0,0))
                self.screen.blit(chatText, (5, ypos))
                ypos += 20
                
        pygame.display.update()

    def run(self):
        running = True
        self.clientThread = threading.Thread(target=self.client.run)
        self.clientThread.start() #yay this works!
        #self.clientThread.join()
        
        while running:
            keystate = pygame.key.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or keystate[K_ESCAPE]:
                    running = False
            self.draw()
            self.clock.tick(100)

            #get text input
            text = None
            text = self.textBox.update(events)

            #if text is input
            if text:
                print text
                if self.client.isConnected:
                    cchat = self.client.makeCchat(text)
                    self.client.sock.send(cchat)
                
        pygame.quit()
        self.clientThread.join()
        sys.exit()
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get command line parameters.')
    parser.add_argument('-s', nargs='?', const='localhost', type=str, default='localhost')
    parser.add_argument('-p', nargs='?', const=36727, type=int, default=36727)
    parser.add_argument('-n', nargs='?', const='john', type=str, default='john')
    parser.add_argument('-m', action='store_true')
    

    args = parser.parse_args()

    testGui = Gui(args.s, args.p, args.n, args.m)
    testGui.run()
