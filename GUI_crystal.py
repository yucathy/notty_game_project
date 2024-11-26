import time

from Components import *
from Functions import *
import queue
import Card

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
        clock = pygame.time.Clock()

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
        # self.nottygame.start_game()

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
        completeImg = img.back.convert_alpha()
        completeButt = ButtonImage(520, 300, completeImg)
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
        # play for me button
        playForMeImg = img.back.convert_alpha()
        playForMeButt = ButtonImage(950, 600, playForMeImg)


        while active:
            clock.tick(30)
            screen.fill((202,228,241))
            current_time = pygame.time.get_ticks()
            if musicOn:
                muteButt.draw(screen)
            else:
                unmuteButt.draw(screen)

            if not self.nottygame.render_queue.empty():
                self.game_status = self.nottygame.render_queue.get(timeout = 0.033)
                print("self.game_status---",self.game_status)
                # print("basic.allHandCard----", basic.allHandCard)

                # AI player start doing...
                if basic.currentPlayer != 0 or basic.actionType == aType.PLAY_FOR_ME:
                    doAIAction(basic,aType,self.game_status['type'].value)

            if basic.play_page == "HOME":
                playButt.draw(screen)
                instructButt.draw(screen)
                # player and difficulty
                # if basic.playerList[0]["level"] == "Easy":
                #     fontLevel0 = renderSysFont("Arial", 50, "Easy", (255, 238, 46), (220, 300))
                # else:
                #     fontLevel0 = renderSysFont("Arial", 50, "Hard", (255, 238, 46), (220, 300))
                # if basic.playerList[1]["level"] == "Easy":
                #     fontLevel1 = renderSysFont("Arial", 50, "Easy", (255, 238, 46), (220, 400))
                # else:
                #     fontLevel1 = renderSysFont("Arial", 50, "Hard", (255, 238, 46), (220, 400))
                # screen.blits((fontName0,fontLevel0,fontLeft0,fontRight0,fontName1,fontLevel1,fontLeft1,fontRight1))

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
                        if current_time - basic.init_time >= 600:
                            basic.init_time = current_time
                            if len(basic.allHandCard[0]["surfaces"]) == 0:
                                basic.allHandCard[0]["surfaces"] = [item[0] for item in myCards]
                                basic.allHandCard[0]["cards"] = [item[1] for item in myCards]
                            elif len(basic.allHandCard[1]["surfaces"]) == 0:
                                basic.allHandCard[1]["surfaces"] = [item[0] for item in leftPlayerCards]
                                basic.allHandCard[1]["cards"] = [item[1] for item in leftPlayerCards]
                            elif len(basic.allHandCard[2]["surfaces"]) == 0:
                                basic.allHandCard[2]["surfaces"] = [item[0] for item in rightPlayerCards]
                                basic.allHandCard[2]["cards"] = [item[1] for item in rightPlayerCards]
                                basic.actionType = aType.SELECT_ACTION
                tempArr = []
                for item in basic.allHandCard.values():
                    tempArr += item["surfaces"]
                screen.blits(tempArr)

                if basic.actionType == aType.SELECT_ACTION:
                    # print("basic.actionNum---",basic.actionNum)
                    # AI player next action...
                    if basic.currentPlayer != 0 or basic.actionType == aType.PLAY_FOR_ME:
                        if self.game_status['next_player'] == -1 and self.game_status['type'].value != "skip":
                            self.nottygame.ai_take_action(next_player)
                    else:
                        renderMessage(screen,WINDOW_WIDTH,basic,aType.SELECT_ACTION,self.game_status["turns_count"])
                    if skipButt.clickable:
                        skipButt.draw(screen)
                    # if playForMeButt.clickable:
                    #     playForMeButt.draw(screen)
                    if basic.actionNum["draw"] == 0:
                        drawButt.draw(screen)
                        drawButt.clickable = True
                        completeButt.clickable = True
                    if basic.actionNum["steal"] == 0:
                        for stealButt in stealButtArr:
                            stealButt.draw(screen)
                            stealButt.clickable = True
                    basic.showDrawCard_time = 0
                    basic.showStealCard_time = 0
                    basic.showDiscard_time = 0
                    basic.showSkip_time = 0


                if basic.actionType == aType.DRAW:
                    drawButt.draw(screen)
                    completeButt.draw(screen)
                    if basic.currentPlayer == 0:
                        totalWidth = getDrawnCardWidth(basic.drawnDeckNum)
                        for i in range(basic.drawnDeckNum):
                            imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 100 * i, 430)
                            screen.blit(img.cardback, imgPos)

                if basic.actionType == aType.SHOW:
                    if self.game_status["action_success"]:
                        showCardList = renderDrawnCard(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"],basic.currentPlayer)
                        screen.blits(showCardList)
                        renderMessage(screen, WINDOW_WIDTH, basic, aType.SHOW, self.game_status["turns_count"], basic.currentPlayer,
                                      self.game_status["players"][basic.currentPlayer]["add"])
                        if basic.showDrawCard_time == 0:
                            basic.showDrawCard_time = current_time
                        else:
                            if current_time - basic.showDrawCard_time >= 3000:
                                basic.showDrawCard_time = current_time
                                (myCards, leftPlayerCards, rightPlayerCards) = renderHandCards(
                                    WINDOW_WIDTH, WINDOW_HEIGHT, self.game_status["players"])
                                updateHandCard(basic, myCards, leftPlayerCards, rightPlayerCards)
                                basic.actionNum["draw"] = 1
                                basic.actionType = aType.SELECT_ACTION

                if basic.actionType == aType.SELECT_PLAYER:
                    handLength = len(basic.allHandCard[basic.selectPlayer]["surfaces"])
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
                        if basic.currentPlayer == 0:  # You steal card
                            renderMessage(screen, WINDOW_WIDTH, basic, aType.STEAL, self.game_status["turns_count"],
                                          basic.currentPlayer,
                                          self.game_status["players"][basic.currentPlayer]["add"], basic.selectPlayer)
                        else:   # AI steal card
                            stolenPlayer = 0
                            for i in range(len(self.game_status["players"])):
                                if (not self.game_status["players"][i]["active"]) and len(self.game_status["players"][i]["delete"]) == 1:
                                    stolenPlayer = i
                            renderMessage(screen, WINDOW_WIDTH, basic, aType.STEAL, self.game_status["turns_count"],
                                          basic.currentPlayer,
                                          self.game_status["players"][basic.currentPlayer]["add"], stolenPlayer)

                        if basic.showStealCard_time == 0:
                            basic.showStealCard_time = current_time
                        else:
                            if current_time - basic.showStealCard_time >= 3000:
                                basic.showStealCard_time = current_time
                                (myCards,leftPlayerCards,rightPlayerCards) = renderHandCards(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"])
                                updateHandCard(basic, myCards, leftPlayerCards, rightPlayerCards)
                                basic.actionNum["steal"] = 1
                                basic.actionType = aType.SELECT_ACTION

                if basic.actionType == aType.SELECT_DISCARD:
                    if basic.currentPlayer == 0:
                        discardButt.draw(screen)
                    totalWidth = getCardListWidth(len(basic.drawnDiscard_surface))
                    drawnDiscardList = list(basic.drawnDiscard_surface)
                    for i in range(len(drawnDiscardList)):
                        imgPos = (WINDOW_WIDTH / 2 - totalWidth / 2 + 20 * i, 430)
                        screen.blit(drawnDiscardList[i][0],imgPos)

                if basic.actionType == aType.DISCARD:
                    basic.drawnDiscard_surface.clear()
                    basic.drawnDiscard_card.clear()
                    if self.game_status["action_success"]:
                        (myCards, leftPlayerCards, rightPlayerCards) = renderHandCards(WINDOW_WIDTH,WINDOW_HEIGHT,self.game_status["players"])
                        updateHandCard(basic,myCards, leftPlayerCards, rightPlayerCards)
                        renderMessage(screen, WINDOW_WIDTH, basic, aType.DISCARD+"_suc", self.game_status["turns_count"],basic.currentPlayer,
                                      self.game_status["players"][basic.currentPlayer]["delete"])
                    else:
                        renderMessage(screen, WINDOW_WIDTH, basic, aType.DISCARD+"_fail", self.game_status["turns_count"],basic.currentPlayer)
                    if basic.showDiscard_time == 0:
                        basic.showDiscard_time = current_time
                    else:
                        if current_time - basic.showDiscard_time >= 2000:
                            basic.showDiscard_time = current_time
                            basic.actionType = aType.SELECT_ACTION

                if basic.actionType == aType.SKIP:
                    basic.actionNum = {
                        "draw": 0,
                        "steal": 0
                    }
                    renderMessage(screen, WINDOW_WIDTH, basic, aType.SKIP, self.game_status["turns_count"], basic.currentPlayer)
                    if basic.showSkip_time == 0:
                        basic.showSkip_time = current_time
                    else:
                        if current_time - basic.showSkip_time >= 2000:
                            basic.showSkip_time = current_time
                            if self.game_status['next_player'] != -1:
                                next_player = self.game_status['next_player']
                                basic.currentPlayer = next_player
                                if next_player == 0 and basic.actionType != aType.PLAY_FOR_ME:  # return to me and enter next round
                                    basic.actionType = aType.SELECT_ACTION
                                else:
                                    # AI player start...
                                    self.nottygame.ai_take_action(next_player)

                if basic.actionType == aType.PLAY_FOR_ME:
                    next_player = self.game_status['next_player']
                    basic.currentPlayer = next_player
                    # AI player start...
                    self.nottygame.ai_take_action(next_player)



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
                                self.nottygame.start_game()
                                startButt.clickable = True
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
                                    self.nottygame.end_game()
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
                        # if fontLeft0[1].collidepoint(event.pos) or fontRight0[1].collidepoint(event.pos):
                        #     if pygame.mouse.get_pressed()[0] == 1:
                        #         if musicOn:
                        #             sound.click.play()
                        #         toggleDifficulty(basic,0)
                        # if fontLeft1[1].collidepoint(event.pos) or fontRight1[1].collidepoint(event.pos):
                        #     if pygame.mouse.get_pressed()[0] == 1:
                        #         if musicOn:
                        #             sound.click.play()
                        #         toggleDifficulty(basic, 1)
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
                        if completeButt.rect.collidepoint(event.pos) and completeButt.clickable:
                            if basic.drawnDeckNum > 0:
                                if musicOn:
                                    sound.click.play()
                                self.nottygame.send_action(self.nottygame.GameActions.DRAW, basic.currentPlayer, basic.drawnDeckNum)
                                drawButt.clickable = False
                                completeButt.clickable = False
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
                        cardsLength = len(basic.allHandCard[0]["surfaces"])
                        for i in range(cardsLength):
                            item_surface = basic.allHandCard[0]["surfaces"][i]
                            item_card = basic.allHandCard[0]["cards"][i]
                            itemWidth = 85 if i == cardsLength-1 else 20
                            itemRect = item_surface[0].get_rect(topleft=item_surface[1], width=itemWidth)
                            if itemRect.collidepoint(event.pos):
                                if basic.actionType == aType.SELECT_ACTION or basic.actionType == aType.SELECT_DISCARD:
                                    basic.drawnDiscard_surface.add(item_surface)
                                    basic.drawnDiscard_card.add(item_card)
                                    drawButt.clickable = False
                                    for stealButt in stealButtArr:
                                        stealButt.clickable = False
                                    basic.actionType = aType.SELECT_DISCARD
                        # discard my card
                        if discardButt.rect.collidepoint(event.pos) and discardButt.clickable:
                            if musicOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.DISCARD, basic.currentPlayer, basic.drawnDiscard_card)
                            basic.actionType = aType.DISCARD
                        # skip
                        if skipButt.rect.collidepoint(event.pos) and skipButt.clickable:
                            if musicOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.SKIP, basic.currentPlayer)
                            basic.drawnDeckNum = 0
                            basic.actionType = aType.SKIP
                        if playForMeButt.rect.collidepoint(event.pos) and playForMeButt.clickable:
                            if musicOn:
                                sound.click.play()
                            basic.actionType = aType.PLAY_FOR_ME


            pygame.display.update()

