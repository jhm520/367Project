class Player:
    def __init__(self, sock=None, name='new'):
        self.sock = sock #client connection socket object
        self.name = name
        self.status = 'w'
        self.strikes = 0
        self.hand = [] #array of card objects
        self.rank = 0
        self.atTable = False
        self.isActive = False
        self.numCards = '00' #client version
        self.isWarlord = False
        self.isScumbag = False
        self.warlordSwap = False
        self.lastPlay = []
        

    def fileno(self):
        return self.sock.fileno()
    
        

