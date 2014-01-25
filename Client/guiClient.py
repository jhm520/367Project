import pygame
from pygame.locals import *
import os
import sys

class Gui:

    def __init__(self):
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

    def draw(self):

        self.screen.blit(self.bg, (0,0))
        pygame.display.update()

    def run(self):
        running = True;
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
