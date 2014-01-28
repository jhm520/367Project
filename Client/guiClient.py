import pygame
from pygame.locals import *
import os
import sys
import argparse
from Client import *

class Gui:

    def __init__(self, host, port, name, manual):
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
        self.client = Client(host, port, name, manual)

        self.font = pygame.font.SysFont(None,16)
        self.font2 = pygame.font.SysFont(None,64)
        self.font3 = pygame.font.SysFont(None,32)

    def draw(self):
        #draw background
        self.screen.blit(self.bg, (0,0))


        
        #draw lobby
        lobbyText = self.font.render("Lobby (" + str(len(self.client.lobby)) + ")", True, (0,0,0))
        self.screen.blit(lobbyText,(490,10))
        
        if self.client.lobby:
            ypos = 30
            for player in self.client.lobby:
                playerText = self.font.render(player, True, (0,0,0))
                self.screen.blit(playerText, (500,ypos))
                ypos += 20
        
                
        pygame.display.update()

    def run(self):
        running = True
        self.clientThread = threading.Thread(target=self.client.run)
        self.clientThread.start() #yay this works!
        #self.clientThread.join()
        
        while running:
            keystate = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT or keystate[K_ESCAPE]:
                    running = False
            self.draw()
            self.clock.tick(100)
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
