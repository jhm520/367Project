def convertToCard (num):

    rank = int(num)/4 + 3

    suitNum = int(num)%4

    if suitNum == 0:
        suit = "C"
    elif suitNum == 1:
        suit = "D"
    elif suitNum == 2:
        suit = "H"
    elif suitNum == 3:
        suit = "S"
    
    return str(rank) + suit


print convertToCard("32")
