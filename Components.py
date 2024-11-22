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
        self.actionType = {
            "start": "Start!",
            "deck_shuffle": "Deck Shuffle",
            "card_init": "Deal 5 cards to each player",
            "select_action": "Select one action type",
            "draw_from_deck": "Draw up to 3 cards from the deck",
            "show_card": "Show cards you have drawn",
            "update_hands": "Update your own cards",
            "select_player": "Please select one player",
            "draw_from_player": "Please select one card from player",
            "select_discard_card": "",
            "discard": "",
            "update_deck": "",
            "skip": "",
            "play_for_me": "",
            "next_turn": ""
        };
        self.allHandCard = {
            "Me": [],
            "Grace": [],
            "John": []
        }
        self.drawnDeckNum = 0
        self.currentPlayer = "Me"
        self.init_time = 0
        self.showCard_time = 0
        self.drawnDiscard = []   # cards you want to discard


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

    def draw(self, screen):
        # action = False
        # pos = pygame.mouse.get_pos()
        # screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # return action
