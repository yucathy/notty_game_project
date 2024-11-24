import pygame

class BasicComponent(object):
    def __init__(self):
        self.play_page = "HOME"
        self.playerList = [{
            "name": "John",
            "level": "Easy"
        }, {
            "name": "Grace",
            "level": "Hard"
        }]
        self.actionType = "start"
        self.allHandCard = {         # 0: you, 1: left player, 2: right player
            0: [],
            1: [],
            2: []
        }
        self.drawnDiscard = set()    # cards you want to discard
        self.drawnDeckNum = 0        # number of cards drawn from deck
        self.currentPlayer = 0       # 0: you, 1: left player, 2: right player
        self.selectPlayer = 0        # choose a player you want to steal(player 1 or 2)
        # self.mycardClickable = True
        self.actionNum = {
            "draw": 0,
            "steal": 0
        }
        self.init_time = 0
        self.showDrawCard_time = 0
        self.showStealCard_time = 0


class ActionType(object):
    def __init__(self):
        self.START = "start"
        self.SHUFFLE = "deck_shuffle"
        self.INIT = "card_init"
        self.SELECT_ACTION = "select_action"
        self.DRAW = "draw_from_deck"
        self.SHOW = "show_card"
        self.UPDATE = "update_hands"
        self.SELECT_PLAYER = "select_player"
        self.STEAL = "draw_from_player"
        self.SELECT_DISCARD = "select_discard_card"
        self.DISCARD = "discard"
        self.SKIP = "skip"
        self.PLAY_FOR_ME = "play_for_me"
        self.NEXT = "next_turn"
        self.actionMessage = {
            self.START: "Start!",
            self.SHUFFLE: "Deck Shuffle",
            self.INIT: "Deal 5 cards to each player",
            self.SELECT_ACTION: "Select one action type",
            self.DRAW: "Draw up to 3 cards from the deck",
            self.SHOW: "Show cards you have drawn",
            self.UPDATE: "Update your own cards",
            self.SELECT_PLAYER: "Please select one player",
            self.STEAL: "Please select one card from player",
            self.SELECT_DISCARD: "",
            self.DISCARD: "",
            self.SKIP: "",
            self.PLAY_FOR_ME: "",
            self.NEXT: ""
        };


class Image(object):
    def __init__(self):
        self.mute = pygame.image.load("./images/mute.png")
        self.unmute = pygame.image.load("./images/unmute.png")
        self.back = pygame.image.load("./images/back.png")
        self.play = pygame.image.load("./images/play.png")
        self.start = pygame.image.load("./images/start.png")
        self.instruction = pygame.image.load("./images/instruction.png")
        self.woman = pygame.image.load("./images/woman.png")
        self.man = pygame.image.load("./images/man.png")
        self.cardback = pygame.image.load("./images/cardback.jpg")


class Sound(object):
    def __init__(self):
        # self.back_g = "../sounds/bg.wav"
        self.shuffled = pygame.mixer.Sound('./sounds/shuffle.wav')
        self.click = pygame.mixer.Sound('./sounds/clicked.wav')


class ButtonImage():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clickable = True
        self.visible = True

    def draw(self, screen):
        # action = False
        # pos = pygame.mouse.get_pos()
        # screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # return action
