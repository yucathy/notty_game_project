import pygame

def reset(basic):
    basic.totalCardNum = 80
    basic.actionType = "start"
    basic.currentPlayer = 0  # 0: you, 1: left player, 2: right player
    basic.selectPlayer = 0  # choose a player you want to steal(player 1 or 2)
    basic.allHandCard = {  # 0: you, 1: left player, 2: right player
        0: {"surfaces": [], "cards": []},
        1: {"surfaces": [], "cards": []},
        2: {"surfaces": [], "cards": []},
    }
    basic.drawnDiscard_surface = set()  # cards you want to discard
    basic.drawnDiscard_card = set()
    basic.drawnDeckNum = 0  # number of cards drawn from deck
    basic.actionNum = {
        "draw": 0,
        "steal": 0
    }
    basic.currentRound = 1  # current round number
    basic.isAI = False
    basic.winMusic = True
    basic.showHomeHint = False
    basic.init_time = 0
    basic.showDrawCard_time = 0
    basic.showStealCard_time = 0
    basic.showDiscard_time = 0
    basic.showSkip_time = 0

def getCardListWidth(num):
    return 85 * num - 65 * (num - 1)

def getDrawnCardWidth(num):
    return 85 * num + 10 * (num - 1)

def toggleDifficulty(basic,i,direction):
    if direction == "left":
        if i == 0:
            basic.currentDifficulty = 2
        else:
            basic.currentDifficulty = i - 1
    elif direction == "right":
        if i == 2:
            basic.currentDifficulty = 0
        else:
            basic.currentDifficulty = i + 1

def createSysFont(font,size,text,color,pos,isCenter=False):
    fontObj = pygame.font.SysFont(font, size).render(text,True, color)
    fontRect = fontObj.get_rect()
    if isCenter:
        pos_e = (1000/2-fontObj.get_width()/2,pos[1])
    else:
        pos_e = pos
    fontRect.topleft = pos_e
    return fontObj,fontRect

def renderHandCards(w,h,playerList):
    myCards = []
    leftPlayerCards = []
    rightPlayerCards = []
    # Array order: You->left player->right player
    me = playerList[0]
    leftPlayer = playerList[1]
    rightPlayer = playerList[2] if len(playerList) > 2 else []
    if len(me) > 0:
        handLength = len(me["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            mycardImg = pygame.image.load("./newimages/" + str(me["handset"][i]).lower().replace(" ", "") + ".jpg")
            imgPos = (w / 2 - totalWidth / 2 + 20 * i, 565)
            myCards.append(((mycardImg, imgPos),me["handset"][i]))
        # totalWidth = getCardListWidth(20)
        # for i in range(20):
        #     mycardImg = pygame.image.load("./newimages/" + str(me["handset"][0]).lower().replace(" ", "") + ".jpg")
        #     imgPos = (w / 2 - totalWidth / 2 + 20 * i, 565)
        #     myCards.append(((mycardImg, imgPos), me["handset"][0]))
    if len(leftPlayer) > 0:
        handLength = len(leftPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            leftCardImg = pygame.image.load(
                "./newimages/" + str(leftPlayer["handset"][i]).lower().replace(" ", "") + ".jpg")
            rotatedImg = pygame.transform.rotate(leftCardImg, 270)
            imgPos = (20, h / 2 - totalWidth / 2 + 15 + 20 * i)
            leftPlayerCards.append(((rotatedImg, imgPos),leftPlayer["handset"][i]))
        # totalWidth = getCardListWidth(20)
        # for i in range(20):
        #     leftCardImg = pygame.image.load(
        #         "./newimages/" + str(leftPlayer["handset"][0]).lower().replace(" ", "") + ".jpg")
        #     rotatedImg = pygame.transform.rotate(leftCardImg, 270)
        #     imgPos = (20, h / 2 - totalWidth / 2 + 20 + 20 * i)
        #     leftPlayerCards.append(((rotatedImg, imgPos), leftPlayer["handset"][0]))
    if len(rightPlayer) > 0:
        handLength = len(rightPlayer["handset"])
        totalWidth = getCardListWidth(handLength)
        for i in range(handLength):
            rightCardImg = pygame.image.load(
                "./newimages/" + str(rightPlayer["handset"][i]).lower().replace(" ", "") + ".jpg")
            rotatedImg = pygame.transform.rotate(rightCardImg, 90)
            imgPos = (863, h / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 20 * i)
            rightPlayerCards.append(((rotatedImg, imgPos),rightPlayer["handset"][i]))
        # totalWidth = getCardListWidth(20)
        # for i in range(20):
        #     rightCardImg = pygame.image.load(
        #         "./newimages/" + str(rightPlayer["handset"][0]).lower().replace(" ", "") + ".jpg")
        #     rotatedImg = pygame.transform.rotate(rightCardImg, 90)
        #     imgPos = (863, h / 2 + totalWidth / 2 + 20 - rotatedImg.get_height() - 20 * i)
        #     rightPlayerCards.append(((rotatedImg, imgPos), rightPlayer["handset"][0]))
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
            showcardImg = pygame.image.load("./newimages/" + str(myAddList[i]).lower().replace(" ", "") + ".jpg")
            imgPos = (w / 2 - totalWidth / 2 + 100 * i, 430)
            showCardList.append((showcardImg, imgPos))
    elif currentPlayer == 1:
        for i in range(addLength):
            showcardImg = pygame.image.load("./newimages/" + str(myAddList[i]).lower().replace(" ", "") + ".jpg")
            rotatedImg = pygame.transform.rotate(showcardImg, 270)
            imgPos = (170, h / 2 - totalWidth / 2 + 15 + 100 * i)
            showCardList.append((rotatedImg, imgPos))
    elif currentPlayer == 2:
        for i in range(addLength):
            showcardImg = pygame.image.load("./newimages/" + str(myAddList[i]).lower().replace(" ", "") + ".jpg")
            rotatedImg = pygame.transform.rotate(showcardImg, 90)
            imgPos = (720, h / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 100 * i)
            showCardList.append((rotatedImg, imgPos))
    return showCardList

def renderMessage(screen,w,basic,type,turn=1,currentPlayer=0,cards=[],targetPlayer=0):
    playerName = basic.vs_players[currentPlayer]
    targetPlayerName = basic.vs_players[targetPlayer]
    is_or_are = "are" if currentPlayer==0 else "is"
    has_or_have = "have" if currentPlayer==0 else "has"
    cardStr = ",".join([str(e) for e in cards])
    actionMessage = {
        "select_action": f"Round{turn}: Select one action or skip directly",
        "show_card": f"Round{turn}: {playerName} {has_or_have} drawn {cardStr} from deck",
        "draw_from_player": f"Round{turn}: {playerName} {has_or_have} drawn {cardStr} from {targetPlayerName}",
        "discard_suc": f"Round{turn}: {playerName} {has_or_have} discarded {cardStr}",
        "discard_fail": f"Round{turn}: Not a valid group! Please select again",
        "discard_fail_ai": f"Round{turn}: {playerName} {is_or_are} trying to discard cards...",
        "skip": f"Round{turn}: {playerName} skipped"
    }
    text = actionMessage[type]
    font = pygame.font.SysFont('arial', 20)
    text_surface = font.render(text, True, (0, 0, 0))
    text_width = text_surface.get_width()
    pos = (w/2-text_width/2, 35)
    screen.blit(text_surface, pos)

def renderAIHint(screen,currentPlayer,messageId):
    aiHintImg = pygame.image.load("./newimages/aiHint_" + str(currentPlayer) + "_" + str(messageId) + ".png")
    if currentPlayer == 1:
        pos = (140, 70)
    elif currentPlayer == 2:
        pos = (740, 70)
    screen.blit(aiHintImg, pos)

def renderCurrentPlayerHint(screen,img,currentPlayer):
    pos = {
        0: (187,540),
        1: (5,80),
        2: (945,80),
    }
    screen.blit(img.hint,pos[currentPlayer])

def renderRules(screen):
    rulesText = "123"
    fontObj = pygame.font.SysFont("Arial", 20).render(rulesText, True, (0,0,0))
    fontRect = fontObj.get_rect()
    fontRect.topleft = (30,30)
    screen.blit(fontObj,fontRect)

def doAIAction(basic, aType, currentAction):
    if currentAction == 'draw':
        basic.actionType = aType.SHOW
    elif currentAction == 'steal':
        basic.actionType = aType.STEAL
    elif currentAction == 'discard':
        basic.actionType = aType.DISCARD
    elif currentAction == 'skip':
        basic.actionType = aType.SKIP

def checkButtClickable(checkButtons,allButtons,type):
    notButtons = allButtons.difference(checkButtons[type])
    for butt in checkButtons[type]:
       butt.clickable = True
    for butt in notButtons:
       butt.clickable = False




