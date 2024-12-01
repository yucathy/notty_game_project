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
        clock = pygame.time.Clock()

        basic = BasicComponent()
        img = Image()
        sound = Sound()
        aType = ActionType()

        active = True
        musicOn = True
        soundOn = True
        pygame.mixer.music.load(sound.bgmusic)
        pygame.mixer.music.play(-1)             # continuous music
        pygame.mixer.music.set_volume(0.5)      # volume

        # play/instruction button
        playImg = img.play.convert_alpha()
        playButt = ButtonImage(420, 200, playImg)
        ruleImg = img.rule.convert_alpha()
        ruleButt = ButtonImage(620, 200, ruleImg)
        # back button
        backImg = img.back.convert_alpha()
        backButt = ButtonImage(10, 10, backImg)
        # music and sound button
        muteImg = img.mute.convert_alpha()
        muteButt = ButtonImage(960, 10, muteImg)
        unmuteImg = img.unmute.convert_alpha()
        unmuteButt = ButtonImage(960, 10, unmuteImg)
        musicImg = img.music.convert_alpha()
        musicButt = ButtonImage(920, 12, musicImg)
        unmusicImg = img.nomusic.convert_alpha()
        unmusicButt = ButtonImage(920, 12, unmusicImg)

        # computer player name
        playTitle = img.you_font
        playTitle1 = img.vs
        playName1 = img.woman_color
        playName1_black = img.woman_black
        playName1_rect = playName1.get_rect()
        playName1_rect.topleft = (600,330)
        playName2 = img.man_color
        playName2_black = img.man_black
        playName2_rect = playName2.get_rect()
        playName2_rect.topleft = (700, 330)

        # difficulty
        levelTitle = img.level
        levelObj = {0: [img.easy,(645,470)], 1: [img.medium,(627,470)], 2: [img.hard,(645,470)]}
        levelObj_small = {0: [img.easy_small, (850, 15)], 1: [img.medium_small, (820, 15)], 2: [img.hard_small, (850, 15)]}
        arrowLeft = img.arrow_left
        arrowLeft_rect = arrowLeft.get_rect()
        arrowLeft_rect.topleft = (575, 470)
        arrowRight = img.arrow_right
        arrowRight_rect = arrowRight.get_rect()
        arrowRight_rect.topleft = (770, 470)

        # deal card button
        startImg = img.start.convert_alpha()
        startButt = ButtonImage(437, 30, startImg)
        # draw button
        drawImg = img.draw_yellow.convert_alpha()
        drawButt = ButtonImage(450, 305, drawImg)
        completeImg = img.complete.convert_alpha()
        completeButt = ButtonImage(510, 305, completeImg)
        # steal button
        stealImg = img.draw.convert_alpha()
        stealButt1 = ButtonImage(60, WINDOW_HEIGHT/2-stealImg.get_height()/2, stealImg)    # left player
        stealButt2 = ButtonImage(890, WINDOW_HEIGHT/2-stealImg.get_height()/2, stealImg)    # right player
        stealButtArr = [stealButt1,stealButt2]
        # discard button
        discardImg = img.discard.convert_alpha()
        discardButt = ButtonImage(940, 640, discardImg)
        # skip button
        skipImg = img.skip.convert_alpha()
        skipButt = ButtonImage(940, 640, skipImg)
        # play for me button
        playForMeImg = img.playforme.convert_alpha()
        playForMeButt = ButtonImage(940, 580, playForMeImg)
        # try again button
        restartImg = img.restart.convert_alpha()
        restartButt = ButtonImage(390, 470, restartImg)
        # home button
        homeImg = img.home.convert_alpha()
        homeButt = ButtonImage(510, 470, homeImg)
        homeImg_info = img.home1.convert_alpha()
        homeButt_info = ButtonImage(730, 80, homeImg_info)

        checkButtons = {
            "home": [playButt, ruleButt, muteButt, unmuteButt, musicButt, unmusicButt],
            "info": [homeButt_info],
            "start": [startButt, backButt, muteButt, unmuteButt, musicButt, unmusicButt],
            "complete_draw": [skipButt, backButt, muteButt, unmuteButt, musicButt, unmusicButt],
            "select_discard": [discardButt, backButt, muteButt, unmuteButt, musicButt, unmusicButt],
            "win": [restartButt, homeButt, backButt]
        }
        allButtons = {playButt, ruleButt, backButt, muteButt, unmuteButt, musicButt, unmusicButt, startButt, drawButt, completeButt, stealButt1, stealButt2, discardButt, skipButt, playForMeButt, restartButt, homeButt, homeButt_info}


        while active:
            clock.tick(30)
            # screen.fill((202,228,241))
            current_time = pygame.time.get_ticks()

            if not self.nottygame.render_queue.empty():
                self.game_status = self.nottygame.render_queue.get(timeout = 0.033)
                print("self.game_status---",self.game_status)
                # print("basic.allHandCard----", basic.allHandCard)
                if basic.isAI:
                    doAIAction(basic, aType, self.game_status['type'].value)

            if basic.play_page == "HOME":
                screen.blit(img.bgHome,(0,0))
                playButt.draw(screen)
                ruleButt.draw(screen)
                checkButtClickable(checkButtons,allButtons,"home")
                # screen.blits((fontSelect,fontName1,fontName2,fontLevel,fontLevelArr[basic.currentDifficulty],fontLeft,fontRight))
                # player
                screen.blit(playTitle, (420, 355))
                screen.blit(playTitle1, (510, 355))
                if "Grace" in basic.vs_players:
                    screen.blit(playName1, playName1_rect)
                else:
                    screen.blit(playName1_black, playName1_rect)
                if "John" in basic.vs_players:
                    screen.blit(playName2, playName2_rect)
                else:
                    screen.blit(playName2_black, playName2_rect)
                # difficulty
                screen.blit(levelTitle,(425,470))
                screen.blit(levelObj[basic.currentDifficulty][0], levelObj[basic.currentDifficulty][1])
                screen.blit(arrowLeft,arrowLeft_rect)
                screen.blit(arrowRight, arrowRight_rect)

            elif basic.play_page == "INFO":
                screen.blit(img.rulepage, (0, 0))
                homeButt_info.draw(screen)
                checkButtClickable(checkButtons,allButtons,"info")

            elif basic.play_page == "GAME":
                screen.blit(img.bgGame, (0, 0))
                screen.blit(levelObj_small[basic.currentDifficulty][0], levelObj_small[basic.currentDifficulty][1])
                backButt.draw(screen)
                if soundOn:
                    muteButt.draw(screen)
                else:
                    unmuteButt.draw(screen)
                if musicOn:
                    musicButt.draw(screen)
                else:
                    unmusicButt.draw(screen)
                if startButt.clickable:
                    startButt.draw(screen)

                # name and profile picture
                screen.blit(img.you, (180, 610))
                player0 = createSysFont("Arial", 20, "You", (0, 0, 0), (192, 585))
                if len(basic.vs_players) == 2:
                    if basic.vs_players[1] == "Grace":
                        screen.blit(img.woman, (50, 75))
                        player1 = createSysFont("Arial", 20, "Grace", (0, 0, 0), (53, 50))
                        screen.blits((player0,player1))
                    else:
                        screen.blit(img.man, (50, 75))
                        player2 = createSysFont("Arial", 20, "John", (0, 0, 0), (58, 50))
                        screen.blits((player0,player2))
                elif len(basic.vs_players) == 3:
                    if basic.vs_players[1] == "Grace":
                        screen.blit(img.woman, (50, 75))
                        screen.blit(img.man, (890, 75))
                        player1 = createSysFont("Arial", 20, "Grace", (0, 0, 0), (53, 50))
                        player2 = createSysFont("Arial", 20, "John", (0, 0, 0), (900, 50))
                    else:
                        screen.blit(img.woman, (890, 75))
                        screen.blit(img.man, (50, 75))
                        player1 = createSysFont("Arial", 20, "Grace", (0, 0, 0), (895, 50))
                        player2 = createSysFont("Arial", 20, "John", (0, 0, 0), (58, 50))
                    screen.blits((player0,player1,player2))

                # current player hint
                # if basic.actionType != aType.START or basic.actionType != aType.SHUFFLE:
                #     renderCurrentPlayerHint(screen,img,basic.currentPlayer)


                if basic.actionType == aType.START:
                    if soundOn:
                        sound.shuffled.play()
                    checkButtClickable(checkButtons,allButtons,"start")
                    basic.actionType = aType.SHUFFLE

                # deck init
                if len(self.game_status) > 0:
                    fontCardNum = createSysFont("Arial", 20, f"Remaining cards: {len(self.game_status['deck'])}",
                                           (0, 0, 0), (300, 240), True)
                    screen.blit(fontCardNum[0],fontCardNum[1])
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
                    if basic.isAI:
                        next_player = self.game_status['next_player']
                        if next_player == -1 and self.game_status['type'].value != "skip":
                            self.nottygame.ai_take_action(basic.currentPlayer)
                    else:
                        renderMessage(screen, WINDOW_WIDTH, basic, aType.SELECT_ACTION, basic.currentRound)
                        skipButt.draw(screen)
                        discardButt.clickable = False
                        if basic.actionNum["draw"] == 0:
                            if len(basic.allHandCard[0]["surfaces"]) < 20:
                                drawButt.draw(screen)
                                drawButt.clickable = completeButt.clickable = True
                        if basic.actionNum["steal"] == 0:
                            if len(basic.allHandCard[0]["surfaces"]) < 20:
                                stealButt1.draw(screen)
                                stealButt1.clickable = True
                                if len(basic.vs_players) == 3:
                                    stealButt2.draw(screen)
                                    stealButt2.clickable = True
                        if basic.actionNum["draw"] == 0 and basic.actionNum["steal"] == 0:
                            playForMeButt.draw(screen)
                    basic.showDrawCard_time = basic.showStealCard_time = basic.showDiscard_time = basic.showSkip_time = 0

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
                    if basic.currentPlayer == 0 and len(basic.drawnDiscard_surface) > 0:
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
                        if basic.isAI:
                            renderMessage(screen, WINDOW_WIDTH, basic, aType.DISCARD + "_fail_ai", self.game_status["turns_count"], basic.currentPlayer)
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
                            next_player = self.game_status['next_player']
                            if next_player != -1:
                                basic.currentPlayer = next_player
                                if next_player == 0:  # return to me and enter next round
                                    basic.isAI = False
                                    basic.currentRound = self.game_status["turns_count"] + 1
                                    basic.actionType = aType.SELECT_ACTION
                                else:
                                    # AI player start...
                                    self.nottygame.ai_take_action(basic.currentPlayer)

                if basic.actionType == aType.PLAY_FOR_ME:
                    # AI player start...
                    self.nottygame.ai_take_action(basic.currentPlayer)

                # winner congratulations
                if (not basic.hasWin) and (len(self.game_status) > 0) and (self.game_status['winner'] is not None):
                    print("self.game_status---win---", self.game_status)
                    basic.actionType = aType.SHUFFLE
                    checkButtClickable(checkButtons, allButtons, "win")
                    screen.blit(img.victory, (WINDOW_WIDTH / 2 - img.victory.get_width() / 2,
                                              WINDOW_HEIGHT / 2 - img.victory.get_height() / 2 - 10))
                    fontCongratulation = createSysFont("Arial", 40, "Congratulations!", (0, 0, 0), (400, 345), True)
                    fontWinner = createSysFont("Arial", 30, f"{self.game_status['winner']} win the game!",
                                               (0, 0, 0), (350, 410), True)
                    screen.blits((fontCongratulation, fontWinner))
                    restartButt.draw(screen)
                    homeButt.draw(screen)
                    if soundOn and basic.winMusic:
                        pygame.mixer.music.stop()
                        sound.winner.set_volume(0.3)
                        sound.winner.play()
                        basic.winMusic = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    self.nottygame.end_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # mousePos = pygame.mouse.get_pos()
                    if event.button == 1:    # mouse left button
                        if playButt.rect.collidepoint(event.pos) and playButt.clickable:
                            if soundOn:
                                sound.click.play()
                            if len(basic.vs_players) >= 2:
                                basic.play_page = "GAME"
                                if basic.currentDifficulty == 0:
                                    aiLevel = self.nottygame.ComputerLevel.EASY
                                elif basic.currentDifficulty == 1:
                                    aiLevel = self.nottygame.ComputerLevel.MEDIUM
                                else:
                                    aiLevel = self.nottygame.ComputerLevel.HARD
                                self.nottygame.setup(len(basic.vs_players),basic.vs_players,aiLevel)
                                self.nottygame.start_game()
                        if ruleButt.rect.collidepoint(event.pos) and ruleButt.clickable:
                            if soundOn:
                                sound.click.play()
                                basic.play_page = "INFO"
                        if ((backButt.rect.collidepoint(event.pos) and backButt.clickable)
                                or (homeButt_info.rect.collidepoint(event.pos) and homeButt_info.clickable)):
                            if basic.play_page == "GAME" or basic.play_page == "INFO":
                                if soundOn:
                                    sound.click.play()
                                if basic.play_page == "GAME":
                                    reset(basic)
                                    self.nottygame.end_game()
                                basic.play_page = "HOME"
                        if ((muteButt.rect.collidepoint(event.pos) and muteButt.clickable)
                                or (unmuteButt.rect.collidepoint(event.pos)) and unmuteButt.clickable):
                            if soundOn:
                                sound.click.play()
                                soundOn = False
                            else:
                                soundOn = True
                        if ((musicButt.rect.collidepoint(event.pos) and musicButt.clickable)
                                or (unmusicButt.rect.collidepoint(event.pos)) and unmusicButt.clickable):
                            if soundOn:
                                sound.click.play()
                            if musicOn:
                                pygame.mixer.music.pause()
                                musicOn = False
                            else:
                                pygame.mixer.music.unpause()
                                musicOn = True
                        # select VS player
                        if playName1_rect.collidepoint(event.pos) or playName1_rect.collidepoint(event.pos):
                            if soundOn:
                                sound.click.play()
                            if "Grace" in basic.vs_players:
                                basic.vs_players.remove("Grace")
                            else:
                                basic.vs_players.append("Grace")
                            print(basic.vs_players)
                        if playName2_rect.collidepoint(event.pos) or playName2_rect.collidepoint(event.pos):
                            if soundOn:
                                sound.click.play()
                            if "John" in basic.vs_players:
                                basic.vs_players.remove("John")
                            else:
                                basic.vs_players.append("John")
                            print(basic.vs_players)
                        # toggle difficulty
                        if arrowLeft_rect.collidepoint(event.pos):
                            if soundOn:
                                sound.click.play()
                            toggleDifficulty(basic,basic.currentDifficulty,"left")
                        if arrowRight_rect.collidepoint(event.pos):
                            if soundOn:
                                sound.click.play()
                            toggleDifficulty(basic,basic.currentDifficulty,"right")
                        # deal cards
                        if startButt.rect.collidepoint(event.pos) and startButt.clickable:
                            if soundOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.DEAL)
                            startButt.clickable = False
                            basic.actionType = aType.INIT
                        # draw cards
                        if drawButt.rect.collidepoint(event.pos) and drawButt.clickable:
                            if len(basic.allHandCard[0]["surfaces"]) + basic.drawnDeckNum < 20:
                                if basic.drawnDeckNum < 3:
                                    if soundOn:
                                        sound.click.play()
                                    basic.drawnDeckNum += 1
                                    basic.actionType = aType.DRAW
                                else:
                                    drawButt.clickable = False
                                for stealButt in stealButtArr:
                                    stealButt.clickable = False
                                discardButt.clickable = skipButt.clickable = playForMeButt.clickable = False
                        # complete draw action
                        if completeButt.rect.collidepoint(event.pos) and completeButt.clickable:
                            if basic.drawnDeckNum > 0:
                                if soundOn:
                                    sound.click.play()
                                self.nottygame.send_action(self.nottygame.GameActions.DRAW, basic.currentPlayer, basic.drawnDeckNum)
                                checkButtClickable(checkButtons,allButtons,"complete_draw")
                                basic.actionType = aType.SHOW
                        # select player and draw from player(steal)
                        for i in range(len(stealButtArr)):
                            if stealButtArr[i].rect.collidepoint(event.pos) and stealButtArr[i].clickable:
                                if soundOn:
                                    sound.click.play()
                                basic.selectPlayer = i+1
                                drawButt.clickable = discardButt.clickable = skipButt.clickable = playForMeButt.clickable = False
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
                        if not basic.hasWin:
                            myCardsLength = len(basic.allHandCard[0]["surfaces"])
                            for i in range(myCardsLength):
                                item_surface = basic.allHandCard[0]["surfaces"][i]
                                item_card = basic.allHandCard[0]["cards"][i]
                                itemWidth = 85 if i == myCardsLength-1 else 20
                                itemRect = item_surface[0].get_rect(topleft=item_surface[1], width=itemWidth)
                                if itemRect.collidepoint(event.pos):
                                    if basic.actionType == aType.SELECT_ACTION or basic.actionType == aType.SELECT_DISCARD:
                                        basic.drawnDiscard_surface.add(item_surface)
                                        basic.drawnDiscard_card.add(item_card)
                                        checkButtClickable(checkButtons,allButtons,"select_discard")
                                        basic.actionType = aType.SELECT_DISCARD
                        # discard my card
                        if discardButt.rect.collidepoint(event.pos) and discardButt.clickable:
                            if soundOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.DISCARD, basic.currentPlayer, basic.drawnDiscard_card)
                            basic.actionType = aType.DISCARD
                        # skip
                        if skipButt.rect.collidepoint(event.pos) and skipButt.clickable:
                            if soundOn:
                                sound.click.play()
                            self.nottygame.send_action(self.nottygame.GameActions.SKIP, basic.currentPlayer)
                            basic.drawnDeckNum = 0
                            basic.isAI = True
                            basic.actionType = aType.SKIP
                        # play for me
                        if playForMeButt.rect.collidepoint(event.pos) and playForMeButt.clickable:
                            if soundOn:
                                sound.click.play()
                            basic.isAI = True
                            basic.actionType = aType.PLAY_FOR_ME
                        if restartButt.rect.collidepoint(event.pos) and restartButt.clickable:
                            if soundOn:
                                sound.click.play()
                            reset(basic)
                            basic.hasWin = True
                            self.nottygame.end_game()
                            self.nottygame.start_game()
                            pygame.mixer.music.play(-1)
                        if homeButt.rect.collidepoint(event.pos) and homeButt.clickable:
                            if soundOn:
                                sound.click.play()
                            reset(basic)
                            basic.hasWin = True
                            self.nottygame.end_game()
                            pygame.mixer.music.play(-1)
                            basic.play_page = "HOME"


            pygame.display.update()

