import pygame

def renderSysFont(font,size,text,color,pos):
    fontObj = pygame.font.SysFont(font, size).render(text,True, color)
    fontRect = fontObj.get_rect()
    fontRect.topleft = pos
    return [fontObj,fontRect]

def reset(basic):
    basic.actionType = "start"
    basic.allHandCard = {
        "Me": [],
        "Grace": [],
        "John": []
    }
    basic.drawnDeckNum = 0
    basic.currentPlayer = "Me"
    basic.init_time = 0
    basic.showCard_time = 0
    basic.drawnDiscard = []

def toggleDifficulty(basic,i):
    if basic.playerList[i]["level"] == "Easy":
        basic.playerList[i]["level"] = "Hard"
    else:
        basic.playerList[i]["level"] = "Easy"

def getCardListWidth(num):
    return 85 * num - 65 * (num - 1)

def getDrawnCardWidth(num):
    return 85 * num + 10 * (num - 1)


def getData():
    data = {
        "deck": [],
        "players": [{
            "name": "Me",
            "hand": ["red 3", "blue 5", "yellow 6", "green 7", "red 8", "blue 9", "green 2", "yellow 7"],
            "add": ["green 9", "red 7", "green 3"],
            "delete": [],
            "active": True
        },{
            "name": "Grace",
            "hand": ["red 6", "green 7", "blue 5", "yellow 2"],
            "add": [],
            "delete": [],
            "active": True
        },{
            "name": "John",
            "hand": ["red 9", "blue 1", "yellow 3", "yellow 5", "green 8"],
            "add": [],
            "delete": [],
            "active": True
        }],
        "type": "",
        "action_success": True,
        "turns_count": 0,
        "winner": ""
    }
    return data
