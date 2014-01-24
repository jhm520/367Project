class SMsgMaker:
    def __init__(self, server):
        self.server = server
#===========================================================================================
    
    def makeSjoin(self, player):
        sjoin = '[sjoin|' + player.name + ']'

        return sjoin
    
#===========================================================================================
    
    def makeSlobb(self):
        slobb = '[slobb|'
        if len(self.server.lobby) > 9:
            slobb += str(len(self.server.lobby)) + '|'
        else:
            slobb += '0' + str(len(self.server.lobby)) + '|'
        for player in self.server.lobby:
            slobb += player.name
            if player != self.server.lobby[-1]:
                slobb += ','
                
        slobb += ']'

        return slobb
    
#===========================================================================================
    
    def makeShand(self, cards):
        shand = '[shand|'
        for card in cards:
            #shand += card.strNumber
            shand += card
            if card != cards[-1]:
                shand += ','
        shand += ']'

        return shand
    
#===========================================================================================

    def makeStabl(self):
        stabl = '[stabl|'
        for player in self.server.game.table:
            stabl += player.status + str(player.strikes) + ':' + player.name + ':'
            if len(str(len(player.hand))) == 2:
                stabl += str(len(player.hand))
            else:
                stabl += '0' + str(len(player.hand))
            if player != self.server.game.table[-1]:
                stabl += ','
            else:
                if len(self.server.game.table) != 7:
                    stabl += ','
        emptyNum = 7-len(self.server.game.table)
        for i in range(emptyNum):
            stabl += 'e0:        :00'
            if i != emptyNum - 1:
                stabl += ','
        stabl += '|'
#         stabl += self.server.game.lastPlay[0].strNumber + ','
#         stabl += self.server.game.lastPlay[1].strNumber + ','
#         stabl += self.server.game.lastPlay[2].strNumber + ','
#         stabl += self.server.game.lastPlay[3].strNumber + '|'
        stabl += self.server.game.lastPlay[0] + ','
        stabl += self.server.game.lastPlay[1] + ','
        stabl += self.server.game.lastPlay[2] + ','
        stabl += self.server.game.lastPlay[3] + '|'
        stabl += str(self.server.game.firstRound) + ']'
        
        return stabl

#===========================================================================================
    def makeSchat(self, player, msg):
        schat = "[schat|" + player.name + "|"

        while len(msg) < 63:
            msg += ' '
            
        schat += msg + ']'

        return schat

    def makeStrik(self, player, code):
        player.strikes += 1
        strik = '[strik|'+code+'|'+str(player.strikes)+']'
        return strik
	
    def makeSwapw(self, highCard):
        #msg = '[swapw|' + highCard.strNumber + ']'
        msg = '[swapw|' + highCard + ']'
        return msg
	
    def makeSwaps(self, scard, wcard):
        #msg = '[swaps|' + scard.strNumber + '|' + wcard.strNumber + ']'
        msg = '[swaps|' + scard + '|' + wcard + ']'
        return msg


