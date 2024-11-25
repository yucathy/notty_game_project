import pygame
from Card import Card

def reset(basic):
    basic.actionType = "start"
    basic.allHandCard = {
        0: {"surfaces": [], "cards": []},
        1: {"surfaces": [], "cards": []},
        2: {"surfaces": [], "cards": []},
    }
    basic.drawnDiscard_surface = set()
    basic.drawnDiscard_card = set()
    basic.drawnDeckNum = 0
    basic.currentPlayer = 0
    basic.selectPlayer = 0
    basic.actionNum = {
        "draw": 0,
        "steal": 0
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
        for i in range(handLength):
            mycardImg = pygame.image.load("./images/" + str(me["handset"][i]).lower().replace(" ", "") + ".png")
            imgPos = (w / 2 - totalWidth / 2 + 20 * i, 560)
            myCards.append(((mycardImg, imgPos),me["handset"][i]))
    if len(leftPlayer) > 0:
        handLength = len(leftPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            leftCardImg = pygame.image.load(
                "./images/" + str(leftPlayer["handset"][i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(leftCardImg, 270)
            imgPos = (25, h / 2 - totalWidth / 2 + 15 + 20 * i)
            leftPlayerCards.append(((rotatedImg, imgPos),leftPlayer["handset"][i]))
    if len(rightPlayer) > 0:
        handLength = len(rightPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            rightCardImg = pygame.image.load(
                "./images/" + str(rightPlayer["handset"][i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(rightCardImg, 90)
            imgPos = (858, h / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 20 * i)
            rightPlayerCards.append(((rotatedImg, imgPos),rightPlayer["handset"][i]))
    return myCards,leftPlayerCards,rightPlayerCards

def updateHandCard(basic,myCards,leftPlayerCards,rightPlayerCards):
    basic.allHandCard = {
        0: {"surfaces": [item[0] for item in myCards], "cards": [item[1] for item in myCards]},
        1: {"surfaces": [item[0] for item in leftPlayerCards],
            "cards": [item[1] for item in leftPlayerCards]},
        2: {"surfaces": [item[0] for item in rightPlayerCards],
            "cards": [item[1] for item in rightPlayerCards]}
    }

def renderDrawnCard(w,h,playerList,currentPlayer):
    showCardList = []
    shownPlayer = playerList[currentPlayer]
    myAddList = shownPlayer["add"]
    addLength = len(myAddList)
    totalWidth = getDrawnCardWidth(addLength)
    if currentPlayer == 0:
        for i in range(addLength):
            showcardImg = pygame.image.load("./images/" + str(myAddList[i]).lower().replace(" ", "") + ".png")
            imgPos = (w / 2 - totalWidth / 2 + 100 * i, 430)
            showCardList.append((showcardImg, imgPos))
    elif currentPlayer == 1:
        for i in range(addLength):
            showcardImg = pygame.image.load("./images/" + str(myAddList[i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(showcardImg, 270)
            imgPos = (170, h / 2 - totalWidth / 2 + 15 + 100 * i)
            showCardList.append((rotatedImg, imgPos))
    elif currentPlayer == 2:
        for i in range(addLength):
            showcardImg = pygame.image.load("./images/" + str(myAddList[i]).lower().replace(" ", "") + ".png")
            rotatedImg = pygame.transform.rotate(showcardImg, 90)
            imgPos = (720, h / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 100 * i)
            showCardList.append((rotatedImg, imgPos))
    return showCardList

def renderSysFont(font,size,text,color,pos):
    fontObj = pygame.font.SysFont(font, size).render(text,True, color)
    fontRect = fontObj.get_rect()
    fontRect.topleft = pos
    return [fontObj,fontRect]

def renderMessage(screen,w,basic,type,turn=1,currentPlayer=0,cards=[],targetPlayer=0):
    playerName = basic.players[currentPlayer]
    targetPlayerName = basic.players[targetPlayer]
    cardStr = ",".join([str(e) for e in cards])
    actionMessage = {
        "select_action": f"Round{turn}: Select one action or skip directly",
        "show_card": f"Round{turn}: {playerName} has drawn {cardStr} from deck",
        "draw_from_player": f"Round{turn}: {playerName} has drawn {cardStr} from {targetPlayerName}",
        "discard_suc": f"Round{turn}: {playerName} has discarded {cardStr}",
        "discard_fail": "Not a valid group! Please select again",
        "skip": f"Round{turn}: {playerName} skipped"
    }
    text = actionMessage[type]
    font = pygame.font.SysFont('arial', 20)
    text_surface = font.render(text, True, (0, 0, 0))
    text_width = text_surface.get_width()
    pos = (w/2-text_width/2, 30)
    screen.blit(text_surface, pos)

def doAIAction(basic, aType, currentAIAction):
    if currentAIAction == 'draw':
        basic.actionType = aType.SHOW
    elif currentAIAction == 'steal':
        basic.actionType = aType.STEAL
    elif currentAIAction == 'discard':
        basic.actionType = aType.DISCARD
    elif currentAIAction == 'skip':
        basic.actionType = aType.SKIP




