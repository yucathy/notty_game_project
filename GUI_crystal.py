from Components import *
from Functions import *

class GUI:
    def __init__(self,nottygame):
        self.nottygame = nottygame
        self.game_status = {}

    def run_game(self):
        WINDOW_WIDTH = 1000
        WINDOW_HEIGHT = 700

        pygame.init()
        pygame.display.set_caption("Notty")
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # clock = pygame.time.Clock()

        basic = BasicComponent()
        img = Image()
        sound = Sound()
        aType = ActionType()

        active = True
        musicOn = True
        # pygame.mixer.music.load(sound.back_g)
        # pygame.mixer.music.play(-1)             # continuous music
        # pygame.mixer.music.set_volume(0.3)      # volume

        self.nottygame.setup(3, ['You', 'Grace', 'John'], self.nottygame.ComputerLevel.EASY)   # name can be None.
        self.nottygame.start_game()

        # play/instruction button
        playImg = img.play.convert_alpha()
        playButt = ButtonImage(80, 100, playImg)
        instructImg = img.instruction.convert_alpha()
        instructButt = ButtonImage(80, 200, instructImg)

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

        # deal card button
        startImg = img.start.convert_alpha()
        startButt = ButtonImage(450, 20, startImg)
        # draw button
        drawImg = img.back.convert_alpha()
        drawButt = ButtonImage(460, 300, drawImg)
        completeImg_deck = img.back.convert_alpha()
        completeButt_deck = ButtonImage(520, 300, completeImg_deck)
        # steal button
        stealButtArr = []
        stealImg = img.back.convert_alpha()
        stealButt1 = ButtonImage(60, WINDOW_HEIGHT/2-stealImg.get_height()/2, stealImg)    # left player
        stealButt2 = ButtonImage(900, WINDOW_HEIGHT/2-stealImg.get_height()/2, stealImg)    # right player
        stealButtArr.append(stealButt1)
        stealButtArr.append(stealButt2)
        # discard button
        discardImg = img.back.convert_alpha()
        discardButt = ButtonImage(900, 650, discardImg)
        # skip button
        skipImg = img.back.convert_alpha()
        skipButt = ButtonImage(950, 650, skipImg)


        while active:
            # clock.tick(40)
            screen.fill((202,228,241))
            current_time = pygame.time.get_ticks()

            if not self.nottygame.render_queue.empty():
                self.game_status = self.nottygame.render_queue.get(timeout = 0.033)
            # print("self.game_status---",self.game_status)
            # print("basic.allHandCard----",len(basic.allHandCard[0]), basic.allHandCard)

            if musicOn:
                muteButt.draw(screen)
            else:
                unmuteButt.draw(screen)

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

            elif basic.play_page == "INFO":
                backButt.draw(screen)

            elif basic.play_page == "GAME":
                backButt.draw(screen)
                if startButt.clickable:
                    startButt.draw(screen)
                screen.blit(img.woman, (20, 70))
                screen.blit(img.man, (900, 70))
                # playerName0 = renderSysFont("Arial", 20, "Grace", (255, 238, 46), (40, 340))
                # playerName1 = renderSysFont("Arial", 20, "John", (255, 238, 46), (920, 330))
                # yourName = renderSysFont("Arial", 20, "You", (255, 238, 46), (450, 550))
                # screen.blits((playerName0,playerName1,yourName))

                if basic.actionType == aType.START:
                    if musicOn:
                        sound.shuffled.play()
                    basic.actionType = aType.SHUFFLE

                # deck init
                totalWidth = getCardListWidth(12)
                for i in range(12):
                    screen.blit(img.cardback, (WINDOW_WIDTH/2-totalWidth/2 + 20 * i, 270))

                # hand cards init
                if basic.actionType == aType.INIT:
                    if self.game_status["action_success"]:
                        (myCards,leftPlayerCards,rightPlayerCards) = renderHandCards(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"])
                    if basic.init_time == 0:
                        basic.init_time = current_time
                    else:
                        if current_time - basic.init_time >= 500:
                            basic.init_time = current_time
                            if len(basic.allHandCard[0]) == 0:
                                basic.allHandCard[0] = myCards
                            elif len(basic.allHandCard[1]) == 0:
                                basic.allHandCard[1] = leftPlayerCards
                            elif len(basic.allHandCard[2]) == 0:
                                basic.allHandCard[2] = rightPlayerCards
                                basic.actionType = aType.SELECT_ACTION
                tempArr = []
                for item in basic.allHandCard.values():
                    tempArr += item
                screen.blits(tempArr)

                if basic.actionType == aType.SELECT_ACTION:
                    print("basic.actionNum---",basic.actionNum)
                    if skipButt.clickable:
                        skipButt.draw(screen)
                    if basic.actionNum["draw"] == 0:
                        drawButt.draw(screen)
                    if basic.actionNum["steal"] == 0:
                        for stealButt in stealButtArr:
                            stealButt.draw(screen)

                if basic.actionType == aType.DRAW:
                    drawButt.draw(screen)
                    completeButt_deck.draw(screen)
                    if basic.currentPlayer == 0:
                        totalWidth = getDrawnCardWidth(basic.drawnDeckNum)
                        for i in range(basic.drawnDeckNum):
                            imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 100 * i, 430)
                            screen.blit(img.cardback, imgPos)

                if basic.actionType == aType.SHOW:
                    if self.game_status["action_success"]:
                        showCardList = renderDrawnCard(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"],basic.currentPlayer)
                        screen.blits(showCardList)
                        if basic.showDrawCard_time == 0:
                            basic.showDrawCard_time = current_time
                        else:
                            if current_time - basic.showDrawCard_time >= 3000:
                                basic.showDrawCard_time = current_time
                                (myCards, leftPlayerCards, rightPlayerCards) = renderHandCards(
                                    WINDOW_WIDTH, WINDOW_HEIGHT, self.game_status["players"])
                                basic.allHandCard = {0: myCards, 1: leftPlayerCards, 2: rightPlayerCards}
                                basic.actionNum["draw"] = 1
                                basic.actionType = aType.SELECT_ACTION

                if basic.actionType == aType.SELECT_PLAYER:
                    handLength = len(basic.allHandCard[basic.selectPlayer])
                    totalWidth = getCardListWidth(handLength)
                    for i in range(handLength):
                        if basic.selectPlayer == 1:
                            rotatedImg = pygame.transform.rotate(img.cardback, 270)
                            imgPos = (25, WINDOW_HEIGHT / 2 - totalWidth / 2 + 15 + 20 * i)
                            screen.blit(rotatedImg, imgPos)
                        elif basic.selectPlayer == 2:
                            rotatedImg = pygame.transform.rotate(img.cardback, 90)
                            imgPos = (858, WINDOW_HEIGHT / 2 + totalWidth / 2 + 15 - rotatedImg.get_height() - 20 * i)
                            screen.blit(rotatedImg, imgPos)
                    stealButtArr[basic.selectPlayer-1].draw(screen)

                if basic.actionType == aType.STEAL:
                    if self.game_status["action_success"]:
                        showCardList = renderDrawnCard(WINDOW_WIDTH, WINDOW_HEIGHT, self.game_status["players"], basic.currentPlayer)
                        screen.blits(showCardList)
                        if basic.showDrawCard_time == 0:
                            basic.showDrawCard_time = current_time
                        else:
                            if current_time - basic.showDrawCard_time >= 3000:
                                basic.showDrawCard_time = current_time
                                (myCards,leftPlayerCards,rightPlayerCards) = renderHandCards(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"])
                                basic.allHandCard = {0: myCards, 1: leftPlayerCards, 2: rightPlayerCards}
                                basic.actionType = aType.UPDATE
                        basic.actionNum["steal"] = 1
                        if basic.actionNum["draw"] == 0:
                            drawButt.draw(screen)

                if basic.actionType == aType.SELECT_DISCARD:
                    if basic.currentPlayer == 0:
                        discardButt.draw(screen)
                    totalWidth = getCardListWidth(len(basic.drawnDiscard))
                    drawnDiscardList = list(basic.drawnDiscard)
                    for i in range(len(drawnDiscardList)):
                        imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 20 * i, 430)
                        screen.blit(drawnDiscardList[i][0],imgPos)

                if basic.actionType == aType.DISCARD:
                    if self.game_status["action_success"]:
                        basic.drawnDiscard.clear()
                        (myCards, leftPlayerCards, rightPlayerCards) = renderHandCards(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"])
                        basic.allHandCard = {0: myCards, 1: leftPlayerCards, 2: rightPlayerCards}
                        basic.actionType = aType.UPDATE
                    else:
                        basic.drawnDiscard.clear()

                if basic.actionType == aType.SKIP:
                    print("self.game_status---", self.game_status)
                    if self.game_status['next_player'] != -1:
                        # if self.game_status['next_player'] == 0:
                        #     basic.actionType = aType.NEXT
                        next_player = self.game_status['next_player']
                        while True:
                            self.nottygame.ai_take_action(next_player)
                            if self.game_status['type'] == self.nottygame.GameActions.SKIP:
                                break



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    self.nottygame.end_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # mousePos = pygame.mouse.get_pos()
                    if event.button == 1:    # mouse left button
                        if playButt.rect.collidepoint(event.pos) and playButt.clickable:
                            if musicOn:
                                sound.click.play()
                                basic.play_page = "GAME"
                                instructButt.clickable = False
                        if instructButt.rect.collidepoint(event.pos) and instructButt.clickable:
                            if musicOn:
                                sound.click.play()
                                basic.play_page = "INFO"
                        if backButt.rect.collidepoint(event.pos) and backButt.clickable:
                            if basic.play_page == "GAME" or basic.play_page == "INFO":
                                if musicOn:
                                    sound.click.play()
                                if basic.play_page == "GAME":
                                    reset(basic)
                                basic.play_page = "HOME"
                        if ((muteButt.rect.collidepoint(event.pos) and muteButt.clickable)
                                or (unmuteButt.rect.collidepoint(event.pos)) and unmuteButt.clickable):
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
                        # deal cards
                        if startButt.rect.collidepoint(event.pos) and startButt.clickable:
                            if musicOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.DEAL)
                            startButt.clickable = False
                            basic.actionType = aType.INIT
                        # draw cards
                        if drawButt.rect.collidepoint(event.pos) and drawButt.clickable:
                            if basic.drawnDeckNum < 3:
                                if musicOn:
                                    sound.click.play()
                                basic.drawnDeckNum += 1
                                basic.actionType = aType.DRAW
                            else:
                                drawButt.clickable = False
                            for stealButt in stealButtArr:
                                stealButt.clickable = False
                        # complete draw action
                        if completeButt_deck.rect.collidepoint(event.pos) and completeButt_deck.clickable:
                            if basic.drawnDeckNum > 0:
                                if musicOn:
                                    sound.click.play()
                                self.nottygame.send_action(self.nottygame.GameActions.DRAW, basic.currentPlayer, basic.drawnDeckNum)
                                drawButt.clickable = False
                                completeButt_deck.clickable = False
                                basic.actionType = aType.SHOW
                        # select player and draw from player(steal)
                        for i in range(len(stealButtArr)):
                            if stealButtArr[i].rect.collidepoint(event.pos) and stealButtArr[i].clickable:
                                if musicOn:
                                    sound.click.play()
                                basic.selectPlayer = i+1
                                drawButt.clickable = False
                                if basic.actionType == aType.SELECT_PLAYER:
                                    self.nottygame.send_action(self.nottygame.GameActions.STEAL, basic.currentPlayer, basic.selectPlayer)
                                    stealButtArr[basic.selectPlayer-1].clickable = False
                                    basic.actionType = aType.STEAL
                                else:
                                    if basic.selectPlayer == 1:
                                        stealButtArr[1].clickable = False
                                    elif basic.selectPlayer == 2:
                                        stealButtArr[0].clickable = False
                                    basic.actionType = aType.SELECT_PLAYER
                        # my card click
                        for i in range(len(basic.allHandCard[0])):
                            item = basic.allHandCard[0][i]
                            itemWidth = 85 if i == len(basic.allHandCard[0])-1 else 20
                            itemRect = item[0].get_rect(topleft=item[1], width=itemWidth)
                            if itemRect.collidepoint(event.pos):
                                basic.drawnDiscard.add(item)
                                drawButt.clickable = False
                                for stealButt in stealButtArr:
                                    stealButt.clickable = False
                                basic.actionType = aType.SELECT_DISCARD
                        # discard my card
                        if discardButt.rect.collidepoint(event.pos) and discardButt.clickable:
                            if musicOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.DISCARD, basic.currentPlayer, basic.drawnDiscard)
                            basic.actionType = aType.DISCARD
                        # skip
                        if skipButt.rect.collidepoint(event.pos) and skipButt.clickable:
                            if musicOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.SKIP, basic.currentPlayer)
                            basic.actionType = aType.SKIP


            pygame.display.update()

