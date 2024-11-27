import pygame

class BasicComponent(object):
    def __init__(self):
        self.play_page = "HOME"
        self.vs_players = ["You","Grace"]
        self.difficulty = {0: "easy", 1: "medium", 2: "hard"}
        self.currentDifficulty = 0
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
        self.currentRound = 1   # current round number
        self.isAI = False
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
        self.bgHome = pygame.image.load("images/bg-home.jpg")
        self.bgGame = pygame.image.load("images/bg-game.jpg")
        self.play = pygame.image.load("images/start.png")
        self.rule = pygame.image.load("images/rule.png")
        self.mute = pygame.image.load("images/mute.png")
        self.unmute = pygame.image.load("images/unmute.png")
        self.back = pygame.image.load("images/back.png")
        self.start = pygame.image.load("images/start.png")
        self.you = pygame.image.load("images/woman1.png")
        self.woman = pygame.image.load("images/woman.png")
        self.man = pygame.image.load("images/man.png")
        self.hint = pygame.image.load("images/hint.png")
        self.cardback = pygame.image.load("images/cardback.jpg")


class Sound(object):
    def __init__(self):
        self.bgmusic = "./sounds/bgmusic.mp3"
        self.shuffled = pygame.mixer.Sound('./sounds/shuffle.wav')
        self.click = pygame.mixer.Sound('./sounds/clicked.wav')


class ButtonImage():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clickable = False

    def draw(self, screen):
        self.clickable = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
