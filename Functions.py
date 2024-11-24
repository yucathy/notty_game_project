from Components import *

def reset(basic):
    basic.actionType = "start"
    basic.currentPlayer = 0
    basic.allHandCard = {
        0: [],
        1: [],
        2: []
    }
    basic.drawnDeckNum = 0
    basic.drawnDiscard = set()
    basic.selectPlayer = 0
    basic.actionNum = {
        "draw_from_player": 0,
        "show_card": 0
    }
    basic.init_time = 0
    basic.showDrawCard_time = 0
    basic.showStealCard_time = 0

def getCardListWidth(num):
    return 85 * num - 65 * (num - 1)

def getDrawnCardWidth(num):
    return 85 * num + 10 * (num - 1)

def toggleDifficulty(basic,i):
    if basic.playerList[i]["level"] == "Easy":
        basic.playerList[i]["level"] = "Hard"
    else:
        basic.playerList[i]["level"] = "Easy"

def renderSysFont(font,size,text,color,pos):
    fontObj = pygame.font.SysFont(font, size).render(text,True, color)
    fontRect = fontObj.get_rect()
    fontRect.topleft = pos
    return [fontObj,fontRect]

def renderHandCards(w,h,playerList):
    myCards = []
    leftPlayerCards = []
    rightPlayerCards = []
    # Array order: You->left player->right player
    me = playerList[0]
    leftPlayer = playerList[1]
    rightPlayer = playerList[2]
    if len(me) > 0:
        handLength = len(me["handset"])
        totalWidth = getCardListWidth(handLength)
        # my discard button
        # discardImg = pygame.image.load("./images/back.png")
        # discardButt = ButtonImage(w / 2 - totalWidth / 2 + totalWidth + 40, 630, discardImg)
        for i in range(handLength):
            mycardImg = pygame.image.load("./images/" + str(me["handset"][i]).lower().replace(" ", "") + ".png")
            imgPos = (w / 2 - totalWidth / 2 + 20 * i, 560)
            myCards.append((mycardImg, imgPos))
    if len(leftPlayer) > 0:
        handLength = len(leftPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            leftCardImg = pygame.image.load(
                "./images/" + str(leftPlayer["handset"][i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(leftCardImg, 270)
            imgPos = (25, h / 2 - totalWidth / 2 + 15 + 20 * i)
            leftPlayerCards.append((rotatedImg, imgPos))
    if len(rightPlayer) > 0:
        handLength = len(rightPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            rightCardImg = pygame.image.load(
                "./images/" + str(rightPlayer["handset"][i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(rightCardImg, 90)
            imgPos = (858, h / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 20 * i)
            rightPlayerCards.append((rotatedImg, imgPos))
    return myCards,leftPlayerCards,rightPlayerCards

def renderDrawnCard(w,h,playerList,currentPlayer):
    showCardList = []
    shownPlayer = playerList[currentPlayer]
    if currentPlayer == 0:
        myAddList = shownPlayer["add"]
        addLength = len(myAddList)
        totalWidth = getDrawnCardWidth(addLength)
        for i in range(addLength):
            showcardImg = pygame.image.load("./images/" + str(myAddList[i]).lower().replace(" ", "") + ".png")
            imgPos = (w / 2 - totalWidth / 2 + 100 * i, 430)
            showCardList.append((showcardImg, imgPos))
    return showCardList

def renderMessage():
    pass




