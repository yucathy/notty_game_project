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
        self.hasWin = False
        self.winMusic = True
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
        self.bgHome = pygame.image.load("newimages/bg-home.jpg")
        self.bgGame = pygame.image.load("newimages/bg-game.jpg")
        self.play = pygame.image.load("newimages/start.png")
        self.rule = pygame.image.load("newimages/help.png")
        self.mute = pygame.image.load("newimages/mute.png")
        self.unmute = pygame.image.load("newimages/unmute.png")
        self.music = pygame.image.load("newimages/music.png")
        self.nomusic = pygame.image.load("newimages/nomusic.png")
        self.back = pygame.image.load("newimages/back.png")
        self.start = pygame.image.load("newimages/play.png")
        self.you = pygame.image.load("newimages/woman1.png")
        self.woman = pygame.image.load("newimages/woman.png")
        self.woman_black = pygame.image.load("newimages/woman_black.png")
        self.woman_color = pygame.image.load("newimages/woman_color.png")
        self.man = pygame.image.load("newimages/man.png")
        self.man_black = pygame.image.load("newimages/man_black.png")
        self.man_color = pygame.image.load("newimages/man_color.png")
        self.cardback = pygame.image.load("newimages/cardback.jpg")
        self.draw = pygame.image.load("newimages/draw.png")
        self.draw_yellow = pygame.image.load("newimages/draw_yellow.png")
        self.complete = pygame.image.load("newimages/confirm.png")
        self.discard = pygame.image.load("newimages/discard.png")
        self.skip = pygame.image.load("newimages/skip.png")
        self.playforme = pygame.image.load("newimages/playforme.png")
        self.hint = pygame.image.load("newimages/hint.png")
        self.restart = pygame.image.load("newimages/restart.png")
        self.home = pygame.image.load("newimages/home.png")
        self.home1 = pygame.image.load("newimages/home1.png")
        self.victory = pygame.image.load("newimages/victory.png")
        self.you_font = pygame.image.load("newimages/you.png")
        self.vs = pygame.image.load("newimages/VS.png")
        self.level = pygame.image.load("newimages/level.png")
        self.easy = pygame.image.load("newimages/easy.png")
        self.easy_small = pygame.image.load("newimages/easy_small.png")
        self.medium = pygame.image.load("newimages/medium.png")
        self.medium_small = pygame.image.load("newimages/medium_small.png")
        self.hard = pygame.image.load("newimages/hard.png")
        self.hard_small = pygame.image.load("newimages/hard_small.png")
        self.arrow_left = pygame.image.load("newimages/arrow_left.png")
        self.arrow_right = pygame.image.load("newimages/arrow_right.png")
        self.rulepage = pygame.image.load("newimages/rulepage.png")
        self.border = pygame.image.load("newimages/border.png")


class Sound(object):
    def __init__(self):
        self.shuffled = pygame.mixer.Sound('./sounds/shuffle.wav')
        self.click = pygame.mixer.Sound('./sounds/clicked.wav')
        self.winner = pygame.mixer.Sound('./sounds/winner.mp3')
        self.bgmusic = "./sounds/bgmusic.mp3"


class ButtonImage():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clickable = False

    def draw(self, screen):
        self.clickable = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
