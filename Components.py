import pygame

class BasicComponent(object):
    def __init__(self):
        self.play_page = "HOME"
        self.players = ["You","Grace","John"]
        self.actionType = "start"
        self.currentPlayer = 0  # 0: you, 1: left player, 2: right player
        self.selectPlayer = 0  # choose a player you want to steal(player 1 or 2)
        self.allHandCard = {         # 0: you, 1: left player, 2: right player
            0: {"surfaces": [], "cards": []},
            1: {"surfaces": [], "cards": []},
            2: {"surfaces": [], "cards": []},
        }
        self.drawnDiscard_surface = set()    # cards you want to discard
        self.drawnDiscard_card = set()
        self.drawnDeckNum = 0   # number of cards drawn from deck
        self.actionNum = {
            "draw": 0,
            "steal": 0
        }
        self.currentAIAction = ""
        self.init_time = 0
        self.showDrawCard_time = 0
        self.showStealCard_time = 0
        self.showDiscard_time = 0
        self.showSkip_time = 0


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
