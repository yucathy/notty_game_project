from Components import *
from Functions import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Notty")
# clock = pygame.time.Clock()

basic = BasicComponent()
img = Image()
sound = Sound()

musicOn = True
# pygame.mixer.music.load(sound.back_g)
# pygame.mixer.music.play(-1)             # continuous bg music
# pygame.mixer.music.set_volume(0.3)      # music volume

active = True  # While game is ON this variable is True



# play/instruction button
playImg = img.play.convert_alpha()
playButt = ButtonImage(80, 100, playImg)
instructImg = img.instruction.convert_alpha()
instructButt = ButtonImage(80, 200, instructImg)
# play_button = Button(screen, "Play！")


# back button
backImg = img.back.convert_alpha()
backButt = ButtonImage(10, 10, backImg)


# music button
muteImg = img.mute.convert_alpha()
muteButt = ButtonImage(960, 10, muteImg)
unmuteImg = img.unmute.convert_alpha()
unmuteButt = ButtonImage(960, 10, unmuteImg)


# player name and difficulty
fontName0 = renderSysFont("Arial", 50, "John", (255, 238, 46), (40, 300))
fontLevel0 = renderSysFont("Arial", 50, "Easy", (255, 238, 46), (220, 300))
fontLeft0 = renderSysFont("Arial", 50, "<", (255, 238, 46), (190, 300))
fontRight0 = renderSysFont("Arial", 50, ">", (255, 238, 46), (330, 300))
fontName1 = renderSysFont("Arial", 50, "Grace", (255, 238, 46), (40, 400))
fontLevel1 = renderSysFont("Arial", 50, "Hard", (255, 238, 46), (220, 400))
fontLeft1 = renderSysFont("Arial", 50, "<", (255, 238, 46), (190, 400))
fontRight1 = renderSysFont("Arial", 50, ">", (255, 238, 46), (330, 400))

# 待替换按钮
# 开始游戏
startImg = img.start.convert_alpha()
startButt = ButtonImage(450, 20, startImg)
# 抽牌按钮
drawImg_deck = img.back.convert_alpha()
drawButt_deck = ButtonImage(460, 300, drawImg_deck)
completeImg_deck = img.back.convert_alpha()
completeButt_deck = ButtonImage(520, 300, completeImg_deck)
drawImg_player1 = img.back.convert_alpha()
drawButt_player1 = ButtonImage(60, WINDOW_HEIGHT/2-drawImg_player1.get_height()/2, drawImg_player1)  # left player
drawImg_player2 = img.back.convert_alpha()
drawButt_player2 = ButtonImage(900, WINDOW_HEIGHT/2-drawImg_player2.get_height()/2, drawImg_player2)  # right player
discardImg_player1 = img.back.convert_alpha()
discardButt_player1 = ButtonImage(0,0,discardImg_player1)



while active:
    screen.fill((202,228,241))
    current_time = pygame.time.get_ticks()
    # clock.tick(40)

    if basic.play_page == "HOME":
        playButt.draw(screen)
        instructButt.draw(screen)

        # player and difficulty
        if basic.playerList[0]["level"] == "Easy":
            fontLevel0 = renderSysFont("Arial", 50, "Easy", (255, 238, 46), (220, 300))
        else:
            fontLevel0 = renderSysFont("Arial", 50, "Hard", (255, 238, 46), (220, 300))
        if basic.playerList[1]["level"] == "Easy":
            fontLevel1 = renderSysFont("Arial", 50, "Easy", (255, 238, 46), (220, 400))
        else:
            fontLevel1 = renderSysFont("Arial", 50, "Hard", (255, 238, 46), (220, 400))
        screen.blits((fontName0,fontLevel0,fontLeft0,fontRight0,fontName1,fontLevel1,fontLeft1,fontRight1))

        if musicOn:
            muteButt.draw(screen)
        else:
            unmuteButt.draw(screen)

    elif basic.play_page == "INFO":
        backButt.draw(screen)

    elif basic.play_page == "GAME":
        backButt.draw(screen)
        startButt.draw(screen)
        screen.blit(img.woman, (20, 70))
        screen.blit(img.man, (900, 70))

        # playerName0 = renderSysFont("Arial", 20, "Grace", (255, 238, 46), (40, 340))
        # playerName1 = renderSysFont("Arial", 20, "John", (255, 238, 46), (920, 330))
        # yourName = renderSysFont("Arial", 20, "You", (255, 238, 46), (450, 550))
        # screen.blits((playerName0,playerName1,yourName))

        if basic.actionType == "start":
            if musicOn:
                sound.shuffled.play()
            basic.actionType = "deck_shuffle"

        # deck init
        totalWidth = getCardListWidth(12)
        for i in range(12):
            screen.blit(img.cardback, (WINDOW_WIDTH/2-totalWidth/2 + 20 * i, 270))

        # hand cards init
        if basic.actionType == "card_init":
            myCards = []
            leftPlayerCards = []
            rightPlayerCards = []
            for player in getData()["players"]:
                if player["name"] == "Me":
                    totalWidth = getCardListWidth(len(player["hand"]))
                    discardButt_player1 = ButtonImage(WINDOW_WIDTH/2-totalWidth/2 + totalWidth + 40, 630, discardImg_player1)
                    for i in range(len(player["hand"])):
                        mycardImg = pygame.image.load("../images/" + player["hand"][i].replace(" ","") + ".png")
                        imgPos = (WINDOW_WIDTH/2-totalWidth/2 + 20 * i, 560)
                        myCards.append((mycardImg, imgPos))
                if player["name"] == "Grace":
                    totalWidth = getCardListWidth(len(player["hand"]))
                    for i in range(len(player["hand"])):
                        leftCardImg = pygame.image.load("../images/" + player["hand"][i].replace(" ","") + ".png")
                        rotatedImg = pygame.transform.rotate(leftCardImg, 270)
                        imgPos = (25, WINDOW_HEIGHT/2 - totalWidth/2 + 30 + 20 * i)
                        leftPlayerCards.append((rotatedImg, imgPos))
                if player["name"] == "John":
                    totalWidth = getCardListWidth(len(player["hand"]))
                    for i in range(len(player["hand"])):
                        rightCardImg = pygame.image.load("../images/" + player["hand"][i].replace(" ", "") + ".png")
                        rotatedImg = pygame.transform.rotate(rightCardImg, 90)
                        imgPos = (858, WINDOW_HEIGHT/2 + totalWidth/2 + 30 - rightCardImg.get_width() - 20 * i)
                        rightPlayerCards.append((rotatedImg, imgPos))

            if basic.init_time == 0:
                basic.init_time = current_time
            else:
                if current_time - basic.init_time >= 500:
                    basic.init_time = current_time
                    if len(basic.allHandCard["Me"]) == 0:
                        basic.allHandCard["Me"] = myCards
                    elif len(basic.allHandCard["Grace"]) == 0:
                        basic.allHandCard["Grace"] = leftPlayerCards
                    elif len(basic.allHandCard["John"]) == 0:
                        basic.allHandCard["John"] = rightPlayerCards
                        basic.actionType = "select_action"

        tempArr = []
        for item in basic.allHandCard.values():
            tempArr += item
        # screen.blits(e for item in handCardInit for e in item)
        screen.blits(tempArr)

        # for item in basic.allHandCard["Me"]:
        #     print(item[0].get_rect(topleft = item[1]))



        if basic.actionType == "select_action":
            drawButt_deck.draw(screen)
            drawButt_player1.draw(screen)
            drawButt_player2.draw(screen)

        if basic.actionType == "draw_from_deck":
            drawButt_deck.draw(screen)
            completeButt_deck.draw(screen)
            if basic.currentPlayer == "Me":
                totalWidth = getDrawnCardWidth(basic.drawnDeckNum)
                for i in range(basic.drawnDeckNum):
                    imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 100 * i, 430)
                    screen.blit(img.cardback, imgPos)

        if basic.actionType == "show_card":
            for player in getData()["players"]:
                if player["name"] == "Me":
                    totalWidth = getDrawnCardWidth(len(player["add"]))
                    for i in range(len(player["add"])):
                        showcardImg = pygame.image.load("../images/" + player["add"][i].replace(" ", "") + ".png")
                        imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 100 * i, 430)
                        screen.blit(showcardImg, imgPos)
            if basic.showCard_time == 0:
                basic.showCard_time = current_time
            else:
                if current_time - basic.showCard_time >= 2000:
                    basic.showCard_time = current_time
                    basic.actionType = "update_hands"

        if basic.actionType == "select_player":
            totalWidth = getCardListWidth(len(basic.allHandCard["Grace"]))
            for i in range(len(basic.allHandCard["Grace"])):
                rotatedImg = pygame.transform.rotate(img.cardback, 270)
                imgPos = (25, WINDOW_HEIGHT / 2 - totalWidth / 2 + 30 + 20 * i)
                screen.blit(rotatedImg, imgPos)
            drawButt_player2.draw(screen)

        if basic.actionType == "draw_from_player":
            if basic.currentPlayer == "Me":
                showcardImg = pygame.image.load("../images/blue2.png")
                imgPos = (WINDOW_WIDTH / 2 - showcardImg.get_width() / 2, 430)
                screen.blit(showcardImg, imgPos)
                if basic.showCard_time == 0:
                    basic.showCard_time = current_time
                else:
                    if current_time - basic.showCard_time >= 2000:
                        basic.showCard_time = current_time
                        basic.actionType = "update_hands"

        if basic.actionType == "select_discard_card":
            if basic.currentPlayer == "Me":
                discardButt_player1.draw(screen)
            totalWidth = getCardListWidth(len(basic.drawnDiscard))
            for i in range(len(basic.drawnDiscard)):
                imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 20 * i, 430)
                screen.blit(basic.drawnDiscard[i][0],imgPos)





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # mousePos = pygame.mouse.get_pos()
            if event.button == 1:    # mouse left button
                if playButt.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                        basic.play_page = "GAME"
                if instructButt.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                        basic.play_page = "INFO"
                if backButt.rect.collidepoint(event.pos):
                    if basic.play_page == "GAME" or basic.play_page == "INFO":
                        if musicOn:
                            sound.click.play()
                        if basic.play_page == "GAME":
                            reset(basic)
                        basic.play_page = "HOME"
                if muteButt.rect.collidepoint(event.pos) or unmuteButt.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                        pygame.mixer.music.pause()
                        musicOn = False
                    else:
                        pygame.mixer.music.unpause()
                        musicOn = True
                if fontLeft0[1].collidepoint(event.pos) or fontRight0[1].collidepoint(event.pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        if musicOn:
                            sound.click.play()
                        toggleDifficulty(basic,0)
                if fontLeft1[1].collidepoint(event.pos) or fontRight1[1].collidepoint(event.pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        if musicOn:
                            sound.click.play()
                        toggleDifficulty(basic, 1)
                if startButt.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                    basic.actionType = "card_init"
                if drawButt_deck.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                    basic.drawnDeckNum += 1
                    basic.actionType = "draw_from_deck"
                if completeButt_deck.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                    basic.actionType = "show_card"
                if drawButt_player1.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                    if basic.actionType == "select_player":
                        basic.actionType = "draw_from_player"
                    else:
                        basic.actionType = "select_player"
                if discardButt_player1.rect.collidepoint(event.pos):
                    if musicOn:
                        sound.click.play()
                    basic.drawnDiscard = []
                # my card click
                for i in range(len(basic.allHandCard["Me"])):
                    item = basic.allHandCard["Me"][i]
                    itemWidth = 85 if i == len(basic.allHandCard["Me"])-1 else 20
                    itemRect = item[0].get_rect(topleft=item[1], width= itemWidth)
                    if itemRect.collidepoint(event.pos):
                        basic.drawnDiscard.append(item)
                        basic.actionType = "select_discard_card"




    pygame.display.update()

