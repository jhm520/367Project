text = "11 12"

cards = text.split()
while len(cards) < 4:
    cards.append('52')
cplay = "[cplay|{0},{1},{2},{3}]".format(cards[0],cards[1],cards[2],cards[3])

print cplay

cards = ["02", "11", "32", "01", "07"]

cards.sort()

for card in cards:
    print card
