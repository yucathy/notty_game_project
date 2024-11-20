from enum import Enum
from gui import NottyGUI
from deck import Deck
from players import Players
import threading
import queue
import copy

class NottyGame:
    '''
    manage the game.
    '''
    class ComputerLevel(Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    class GameActions(Enum):
        DEAL = "deal"
        DRAW = "draw"         
        STEAL = "steal"       
        DISCARD = "discard"
        PLAY_FOR_ME = "play_for_me"   
        SKIP = "skip"   

    def __init__(self):
        '''initilize all the settings for the game'''
        self.action_queue = queue.Queue()
        self.render_queue = queue.Queue()
        self.game_thread = None
        self.running = False
        # self.callback = None
        self.game_status = {}

    def setup(self, player_count: int, player_name: list , computer_level: str):
        '''
        info is a list about the setup for the card game.
        - player_count
        - player_name
        - computer_level
        '''
        assert type(player_count) != 'int', "player_count type should be int."
        assert type(player_name) != 'list', "player_name type should be a list."
        assert type(computer_level) != 'str', "computer_level type should be str."

        print(player_count, player_name, computer_level)

    # def register_callback(self, func):
    #     self.callback = func

    def receive_action(self, action: GameActions, action_info = None):
        self.action_queue.put(action)

    def start_game(self):
        self.running = True
        self.game_thread = threading.Thread(target = self.process_turns)
        self.game_thread.start()
        pass

    def end_game(self):
        self.running = False
        if self.game_thread:
            self.game_thread.join()

    def update_status(self):
        self.game_status["deck"] = []
        self.game_status["players"] = [
            {"name": "realplayer", "handset": [], "add": [], "delete": [], "active": True},
            {"name": "computerplayer1", "handset": [], "add": [], "delete": [], "active": False},
        ]
        self.game_status["type"] = self.GameActions.DISCARD
        self.game_status["action_success"] = True
        self.game_status["turns_count"] = 1
        self.game_status["winner"] = None

    def process_turns(self):
        while self.running:
            try:
                # get user action
                user_action = self.action_queue.get(timeout=1)
                print(user_action)

                # take action
                if user_action == self.GameActions.DEAL:
                    pass
                elif user_action == self.GameActions.DRAW:
                    pass
                elif user_action == self.GameActions.STEAL:
                    pass
                elif user_action == self.GameActions.DISCARD:
                    pass
                elif user_action == self.GameActions.PLAY_FOR_ME:
                    pass
                elif user_action == self.GameActions.SKIP:
                    pass

                self.update_status()

                # self.callback(copy.deepcopy(self.game_status))
                self.render_queue.put(copy.deepcopy(self.game_status))

            except queue.Empty:
                continue





        



