import pygame
from pygame.locals import *
import string
import os
import sys
import time
import argparse
from Client import *


class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class Input:
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font', 'pygame.font.Font(None, 32)'],
                              ['color', '(0,0,0)'], ['restricted', '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt', '\'\''])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt; self.value = ''
        self.shifted = False
        self.pause = 0

    def set_pos(self, x, y):
        """ Set the position to x, y """
        self.x = x
        self.y = y

    def set_font(self, font):
        """ Set the font for the input """
        self.font = font

    def draw(self, surface):
        """ Draw the text input to a surface """
        text = self.font.render(self.prompt+self.value, 1, self.color)
        surface.blit(text, (self.x, self.y))

    def update(self, events):
        """Hold Backspace Thingy"""
##        pressed = pygame.key.get_pressed()
##        if self.pause == 3 and pressed[K_BACKSPACE]:
##            self.pause = 0
##            self.value = self.value[:-1]
##        elif pressed[K_BACKSPACE]:
##            self.pause += 1
##        else:
##            self.pause = 0
        """ Update the input based on passed events """
        for event in events:
            
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE: self.value = self.value[:-1]
                elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                elif event.key == K_SPACE: self.value += ' '
                elif event.key == K_RETURN:
                    val = self.value
                    self.value = ''
                    return val
                if not self.shifted:
                    if event.key == K_a and 'a' in self.restricted: self.value += 'a'
                    elif event.key == K_b and 'b' in self.restricted: self.value += 'b'
                    elif event.key == K_c and 'c' in self.restricted: self.value += 'c'
                    elif event.key == K_d and 'd' in self.restricted: self.value += 'd'
                    elif event.key == K_e and 'e' in self.restricted: self.value += 'e'
                    elif event.key == K_f and 'f' in self.restricted: self.value += 'f'
                    elif event.key == K_g and 'g' in self.restricted: self.value += 'g'
                    elif event.key == K_h and 'h' in self.restricted: self.value += 'h'
                    elif event.key == K_i and 'i' in self.restricted: self.value += 'i'
                    elif event.key == K_j and 'j' in self.restricted: self.value += 'j'
                    elif event.key == K_k and 'k' in self.restricted: self.value += 'k'
                    elif event.key == K_l and 'l' in self.restricted: self.value += 'l'
                    elif event.key == K_m and 'm' in self.restricted: self.value += 'm'
                    elif event.key == K_n and 'n' in self.restricted: self.value += 'n'
                    elif event.key == K_o and 'o' in self.restricted: self.value += 'o'
                    elif event.key == K_p and 'p' in self.restricted: self.value += 'p'
                    elif event.key == K_q and 'q' in self.restricted: self.value += 'q'
                    elif event.key == K_r and 'r' in self.restricted: self.value += 'r'
                    elif event.key == K_s and 's' in self.restricted: self.value += 's'
                    elif event.key == K_t and 't' in self.restricted: self.value += 't'
                    elif event.key == K_u and 'u' in self.restricted: self.value += 'u'
                    elif event.key == K_v and 'v' in self.restricted: self.value += 'v'
                    elif event.key == K_w and 'w' in self.restricted: self.value += 'w'
                    elif event.key == K_x and 'x' in self.restricted: self.value += 'x'
                    elif event.key == K_y and 'y' in self.restricted: self.value += 'y'
                    elif event.key == K_z and 'z' in self.restricted: self.value += 'z'
                    elif event.key == K_0 and '0' in self.restricted: self.value += '0'
                    elif event.key == K_1 and '1' in self.restricted: self.value += '1'
                    elif event.key == K_2 and '2' in self.restricted: self.value += '2'
                    elif event.key == K_3 and '3' in self.restricted: self.value += '3'
                    elif event.key == K_4 and '4' in self.restricted: self.value += '4'
                    elif event.key == K_5 and '5' in self.restricted: self.value += '5'
                    elif event.key == K_6 and '6' in self.restricted: self.value += '6'
                    elif event.key == K_7 and '7' in self.restricted: self.value += '7'
                    elif event.key == K_8 and '8' in self.restricted: self.value += '8'
                    elif event.key == K_9 and '9' in self.restricted: self.value += '9'
                    elif event.key == K_BACKQUOTE and '`' in self.restricted: self.value += '`'
                    elif event.key == K_MINUS and '-' in self.restricted: self.value += '-'
                    elif event.key == K_EQUALS and '=' in self.restricted: self.value += '='
                    elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.value += '['
                    elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.value += ']'
                    elif event.key == K_BACKSLASH and '\\' in self.restricted: self.value += '\\'
                    elif event.key == K_SEMICOLON and ';' in self.restricted: self.value += ';'
                    elif event.key == K_QUOTE and '\'' in self.restricted: self.value += '\''
                    elif event.key == K_COMMA and ',' in self.restricted: self.value += ','
                    elif event.key == K_PERIOD and '.' in self.restricted: self.value += '.'
                    elif event.key == K_SLASH and '/' in self.restricted: self.value += '/'
                elif self.shifted:
                    if event.key == K_a and 'A' in self.restricted: self.value += 'A'
                    elif event.key == K_b and 'B' in self.restricted: self.value += 'B'
                    elif event.key == K_c and 'C' in self.restricted: self.value += 'C'
                    elif event.key == K_d and 'D' in self.restricted: self.value += 'D'
                    elif event.key == K_e and 'E' in self.restricted: self.value += 'E'
                    elif event.key == K_f and 'F' in self.restricted: self.value += 'F'
                    elif event.key == K_g and 'G' in self.restricted: self.value += 'G'
                    elif event.key == K_h and 'H' in self.restricted: self.value += 'H'
                    elif event.key == K_i and 'I' in self.restricted: self.value += 'I'
                    elif event.key == K_j and 'J' in self.restricted: self.value += 'J'
                    elif event.key == K_k and 'K' in self.restricted: self.value += 'K'
                    elif event.key == K_l and 'L' in self.restricted: self.value += 'L'
                    elif event.key == K_m and 'M' in self.restricted: self.value += 'M'
                    elif event.key == K_n and 'N' in self.restricted: self.value += 'N'
                    elif event.key == K_o and 'O' in self.restricted: self.value += 'O'
                    elif event.key == K_p and 'P' in self.restricted: self.value += 'P'
                    elif event.key == K_q and 'Q' in self.restricted: self.value += 'Q'
                    elif event.key == K_r and 'R' in self.restricted: self.value += 'R'
                    elif event.key == K_s and 'S' in self.restricted: self.value += 'S'
                    elif event.key == K_t and 'T' in self.restricted: self.value += 'T'
                    elif event.key == K_u and 'U' in self.restricted: self.value += 'U'
                    elif event.key == K_v and 'V' in self.restricted: self.value += 'V'
                    elif event.key == K_w and 'W' in self.restricted: self.value += 'W'
                    elif event.key == K_x and 'X' in self.restricted: self.value += 'X'
                    elif event.key == K_y and 'Y' in self.restricted: self.value += 'Y'
                    elif event.key == K_z and 'Z' in self.restricted: self.value += 'Z'
                    elif event.key == K_0 and ')' in self.restricted: self.value += ')'
                    elif event.key == K_1 and '!' in self.restricted: self.value += '!'
                    elif event.key == K_2 and '@' in self.restricted: self.value += '@'
                    elif event.key == K_3 and '#' in self.restricted: self.value += '#'
                    elif event.key == K_4 and '$' in self.restricted: self.value += '$'
                    elif event.key == K_5 and '%' in self.restricted: self.value += '%'
                    elif event.key == K_6 and '^' in self.restricted: self.value += '^'
                    elif event.key == K_7 and '&' in self.restricted: self.value += '&'
                    elif event.key == K_8 and '*' in self.restricted: self.value += '*'
                    elif event.key == K_9 and '(' in self.restricted: self.value += '('
                    elif event.key == K_BACKQUOTE and '~' in self.restricted: self.value += '~'
                    elif event.key == K_MINUS and '_' in self.restricted: self.value += '_'
                    elif event.key == K_EQUALS and '+' in self.restricted: self.value += '+'
                    elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.value += '{'
                    elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.value += '}'
                    elif event.key == K_BACKSLASH and '|' in self.restricted: self.value += '|'
                    elif event.key == K_SEMICOLON and ':' in self.restricted: self.value += ':'
                    elif event.key == K_QUOTE and '"' in self.restricted: self.value += '"'
                    elif event.key == K_COMMA and '<' in self.restricted: self.value += '<'
                    elif event.key == K_PERIOD and '>' in self.restricted: self.value += '>'
                    elif event.key == K_SLASH and '?' in self.restricted: self.value += '?'

        if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]



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

        self.chatTextBox = Input(x=5, y=460, font=self.font, maxlength=63, color=(0,0,0), prompt='Chat: ')
        self.playTextBox = Input(x=210, y=400, font=self.font3, maxlength=20, color=(255,0,0), prompt='Input Play: ')
        self.swapTextBox = Input(x=210, y=430, font=self.font3, maxlength=2, color=(255,0,0), prompt='Input Card to Swap: ')

    def draw(self):
        #draw background
        #self.screen.blit(self.bg, (0,0))
        self.screen.fill((0,150,0))
        pygame.draw.line(self.screen, (0,0,0), (0, 320), (480, 320), 2)
        pygame.draw.line(self.screen, (0,0,0), (480, 0), (480, 480), 2)
        pygame.draw.line(self.screen, (0,0,0), (200, 320), (200, 480), 2)


        #draw connection info
        if self.client.isConnected:
            connectText = self.font.render("Connected to {0} on port {1} as {2} in {3} mode.".format(str(self.client.host), str(self.client.port),self.client.name.strip(), self.client.mode), True, (0,0,0))
            #draw lobby
            lobbyText = self.font.render("Lobby (" + str(len(self.client.lobby)) + ")", True, (0,0,0))
            self.screen.blit(lobbyText,(490,10))
            
            if self.client.lobby:
                posCnt = 0
                for player in self.client.lobby:
                    playerText = self.font.render(player, True, (0,0,0))
                    if posCnt > 21:
                        self.screen.blit(playerText, (560,30+((posCnt-22)*20)))
                    else:
                        self.screen.blit(playerText, (500,30+(posCnt*20)))
                    posCnt += 1
                    #ypos += 20
            
            if self.client.table:
                
                #Draw gameInProgress
                gameInProgressText = self.font.render("Game currently in progress", True, (0,0,0))
                
                #draw table
                tableDrawPositions = [(15,50), (125,50), (235,50), (345, 50), (15, 150), (125, 150), (235, 150)]
                tableActiveMarker = self.font.render(">", True, (0,0,0))
                posCnt = 0

                for player in self.client.table:
                    pos = tableDrawPositions[posCnt]
                    tablePlayerText = self.font.render(player.name, True, (0,0,0))
                    tablePlayerNumCards = self.font.render("-cards: " + player.numCards, True, (0,0,0))
                    tablePlayerStrikes = self.font.render("-strikes: " + player.strikes, True, (0,0,0))
                    tablePlayerStatus = self.font.render("-status: " + player.status, True, (0,0,0))
                    self.screen.blit(tablePlayerText, pos)
                    self.screen.blit(tablePlayerNumCards, (pos[0]+15, pos[1] + 45))
                    self.screen.blit(tablePlayerStrikes, (pos[0]+15, pos[1] + 30))
                    self.screen.blit(tablePlayerStatus, (pos[0]+15, pos[1]+15))
                    
                    if player.status == "a":
                        self.screen.blit(tableActiveMarker, (pos[0]-10, pos[1]))
                    if player is self.client.player:
                        tableYouMarker = self.font.render("<- You!", True, (255,0,0))
                        self.screen.blit(tableYouMarker, (pos[0]+55, pos[1]))
                    posCnt += 1

                #draw last play
                cardDrawPositions = [(225,275), (275, 275),(325, 275), (375,275)]
                if self.client.lastPlay:
                    lastPlayText = self.font3.render("Last Play:", True, (0,0,0))
                    self.screen.blit(lastPlayText, (100, 275))
                    posCnt = 0
                    for card in self.client.lastPlay:
                        tableCardText = self.font3.render(card, True, (0,0,0))
                        self.screen.blit(tableCardText, cardDrawPositions[posCnt])
                        posCnt += 1

                #draw hand
                yourHandText = self.font.render("Your Hand:", True, (0,0,0))
                self.screen.blit(yourHandText, (210, 325))
                if self.client.hand:
                    posCnt = 0
                    for card in self.client.hand:
                        handCardText = self.font.render(card, True, (0,0,0))
                        if posCnt < 8:
                            self.screen.blit(handCardText, (275 + posCnt * 25, 325))
                        elif posCnt < 16:
                            self.screen.blit(handCardText, (275 + (posCnt-8) * 25, 345))
                        else:
                            self.screen.blit(handCardText, (275 + (posCnt-16)*25, 365))
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
            ypos = 330
            for chat in self.client.chatLog:
                name = chat[0:8]
                msg = chat[9:]
                chatText = self.font.render(">{0}: {1}".format(name, msg), True, (0,0,0))
                self.screen.blit(chatText, (5, ypos))
                ypos += 16

        pygame.display.update()

##        #TESTING ONLY (Draw everything)
##        #draw lobby
##        lobbyText = self.font.render("Lobby (" + str(len(self.client.lobby)) + ")", True, (0,0,0))
##        self.screen.blit(lobbyText,(490,10))
##        
##        playerText = self.font.render("johnnash", True, (0,0,0))
##        for i in range(35):
##            if i > 21:
##                self.screen.blit(playerText, (560,30+((i-22)*20)))
##            else:
##                self.screen.blit(playerText, (500,30+(i*20)))
##        #Draw gameInProgress
##        gameInProgressText = self.font.render("Game currently in progress", True, (0,0,0))
##        self.screen.blit(gameInProgressText, (5, 20))
##        #draw table
##        tableDrawPositions = [(15,50), (125,50), (235,50), (345, 50), (15, 150), (125, 150), (235, 150)]
##        tableActiveMarker = self.font.render(">", True, (0,0,0))
##        posCnt = 0
##
##        for pos in tableDrawPositions:
##            #pos = tableDrawPositions[posCnt]
##            tablePlayerText = self.font.render("johnnash", True, (0,0,0))
##            tablePlayerNumCards = self.font.render("-Cards: 00", True, (0,0,0))
##            tablePlayerStrikes = self.font.render("-Strikes: 0", True, (0,0,0))
##            tablePlayerStatus = self.font.render("-Status: a", True, (0,0,0))
##            self.screen.blit(tablePlayerText, pos)
##            self.screen.blit(tablePlayerNumCards, (pos[0]+15, pos[1] + 45))
##            self.screen.blit(tablePlayerStrikes, (pos[0]+15, pos[1] + 30))
##            self.screen.blit(tablePlayerStatus, (pos[0]+15, pos[1]+15))
##            
##            #if player.status == "a":
##            self.screen.blit(tableActiveMarker, (pos[0]-10, pos[1]))
##            #if player is self.client.player:
##            tableYouMarker = self.font.render("<- You!", True, (255,0,0))
##            self.screen.blit(tableYouMarker, (pos[0]+55, pos[1]))
##            #posCnt += 1
##
##
##        cardDrawPositions = [(225,275), (275, 275),(325, 275), (375,275)]
##        #if self.client.lastPlay:
##            #posCnt = 0
##        lastPlayText = self.font3.render("Last Play:", True, (0,0,0))
##        self.screen.blit(lastPlayText, (100, 275))
##        for pos in cardDrawPositions:
##            tableCardText = self.font3.render("52", True, (0,0,0))
##            self.screen.blit(tableCardText, pos)
##            posCnt += 1
##
##        #draw hand
##        yourHandText = self.font.render("Your Hand:", True, (0,0,0))
##        self.screen.blit(yourHandText, (210, 325))
##        #if self.client.hand:
##        posCnt = 0
##        for i in range(17):
##            handCardText = self.font.render("22", True, (0,0,0))
##            if posCnt < 8:
##                self.screen.blit(handCardText, (275 + posCnt * 25, 325))
##            elif posCnt < 16:
##                self.screen.blit(handCardText, (275 + (posCnt-8) * 25, 345))
##            else:
##                self.screen.blit(handCardText, (275 + (posCnt-16)*25, 365))
##            posCnt += 1
##
##        #draw text boxes
##        self.playTextBox.draw(self.screen)
##        self.swapTextBox.draw(self.screen)
##        self.chatTextBox.draw(self.screen)
##
##        
##                
##        pygame.display.update()

    def run(self):
        self.running = 1
        self.clientThread = threading.Thread(target=self.client.run)
        self.clientThread.start()

        
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
    testGui = Gui(args.s, args.p, args.n, args.m)
    testGui.run()
