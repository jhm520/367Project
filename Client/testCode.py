def rank(card):
    rankNum = int(card)/4+3

    if rankNum == 10:
        return "T"
    elif rankNum == 11:
        return "J"
    elif rankNum == 12:
        return "Q"
    elif rankNum == 13:
        return "K"
    elif rankNum == 14:
        return "A"
    elif rankNum == 15:
        return "2"
    elif rankNum < 10:
        return str(rankNum)
    else:
        return " "


card = "52"

print "{0}({1})".format(card,rank(card))
