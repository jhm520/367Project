'''
Created on Jan 1, 2014

@author: John
'''

import pygame
from pygame.locals import *
import threading
import os
import sys


class Gui:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        #self.client = client #the client this gui will correspond to
        pygame.init()
        #self.bg = pygame.image.load("map.png") #load backround image
        self.bg = pygame.image.load(os.path.join('data', 'map.png'))
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Warlords")
        pygame.mouse.set_visible(1)
        
#         self.background = pygame.Surface(self.screen.get_size())
#         self.background = self.background.convert()
#         self.background.fill((250, 250, 250))


        
        self.clock = pygame.time.Clock() #clock
        
    
    def draw(self):
        #draw background
        self.screen.blit(self.bg, (0,0))
        pygame.display.flip()
        
        
        #draw everything

        

        #4 sections in the background
        
        #Lobby section
            #upper right corner
            #draw players currently in lobby
            #Draw each player's name, it can be fairly small
        
        #Chat section (chat box, lower left corner, wrap lines)
        
        #Table section
            #draw the state of the table, will take up most of the screen
        
        #Player section
            #draw the state of this player
            #draw each card in their hand sorted by rank
            #indicate if it is their turn
            #have a click interface for choosing a play
    
    def run(self):
        running = True
        while running:
            keystate = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT or keystate[K_ESCAPE]:
                    pygame.quit()
                    running = False
                    sys.exit()
            self.draw()
            self.clock.tick(100)
                
        

if __name__ == '__main__':
    testGui = Gui()
    testGui.run()
