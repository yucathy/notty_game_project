from enum import Enum
from Card import Card
from deck import Deck
from players import Players, AIPlayer
import threading
import queue
import copy
import random
import string

class NottyGame:
    '''
    manage the game.
    '''

    max_draw_times_per_turn = 3
    max_steal_times_per_turn = 1
    user_id = 0

    class ComputerLevel(Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    class GameActions(Enum):
        DEAL = "deal"
        DRAW = "draw"         
        STEAL = "steal"       
        DISCARD = "discard" 
        SKIP = "skip"   

    def __init__(self):
        '''initilize all the settings for the game'''
        self.action_queue = queue.Queue()
        self.render_queue = queue.Queue()
        self.game_thread = None
        self.winner = None
        self.running = False
        self.game_status = {}
        self.players = []
        self.turn_count = 0
        self.draw_times = 0
        self.old_turn_count = 0
        self.steal_times = 0
        
        self.deck = Deck()
        self.ai_actions_pool = [action for action in self.GameActions \
                        if action != self.GameActions.DEAL]
        
    def __initialize_state(self):
        '''keep players' setting when play again.'''
        self.action_queue = queue.Queue()
        self.render_queue = queue.Queue()
        self.game_thread = None
        self.winner = None
        self.running = False
        self.game_status = {}
        self.turn_count = 0
        self.draw_times = 0
        self.old_turn_count = 0
        self.steal_times = 0
        self.deck = Deck()
        self.ai_actions_pool = [action for action in self.GameActions \
                        if action != self.GameActions.DEAL]
        
        for player in self.players:
            player.initialize_state()
        
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

        self.players.clear()
        for i in range(player_count):
            self.players.append(AIPlayer(player_name[i]))

        # print(player_count, player_name, computer_level)

    def create_card(self, colour: str, number: int) -> Card:
        return Card(colour, number)

    def send_action(self, action: GameActions, action_user_id: int = None, action_info = None):
        self.action_queue.put([action, action_user_id, action_info])

    def start_game(self):
        self.running = True
        self.game_thread = threading.Thread(target = self.__process_turns)
        self.game_thread.start()

    def end_game(self):
        self.running = False
        if self.game_thread:
            self.game_thread.join()
        self.__initialize_state()

    def update_status(self, user_action, action_success, active_status, next_player):
        self.game_status["deck"] = self.deck.cards
        self.game_status["type"] = user_action
        self.game_status["action_success"] = action_success
        self.game_status["turns_count"] = self.turn_count
        self.game_status["winner"] = self.winner
        player_list = []
        for player, active in zip(self.players, active_status):
            player_list.append({"name": player.name, "handset": player.hand, \
                                "add": player.add, "delete": player.delete, "active": active})

        self.game_status["players"] = player_list
        self.game_status['next_player'] = next_player

    def __process_turns(self):
        while self.running:
            try:
                # get user action
                user_action_with_info = self.action_queue.get(timeout=1)
                # print(user_action_with_info)
                user_action = user_action_with_info[0]
                action_user_id = user_action_with_info[1]
                user_info = user_action_with_info[2]

                action_success = True
                active_status = [False for _ in range(len(self.players))]
                next_player = -1

                # take action
                if user_action == self.GameActions.DEAL:
                    for player in self.players:
                        player.draw_cards(self.deck, 5)

                    self.turn_count += 1
                    self.old_turn_count = self.turn_count
                    
                elif user_action == self.GameActions.DRAW:
                    if self.turn_count == self.old_turn_count:
                        self.draw_times += 1
                    if self.draw_times <= self.max_draw_times_per_turn:
                        current_player = self.players[action_user_id]
                        if not current_player.draw_cards(self.deck, user_info):
                            action_success = False
                        active_status[action_user_id] = True
                    else:
                        action_success = False
                    
                elif user_action == self.GameActions.STEAL:
                    if self.turn_count == self.old_turn_count:
                        self.steal_times += 1
                    if self.steal_times <= self.max_steal_times_per_turn and \
                        type(user_info) == int:
                        current_player = self.players[action_user_id]
                        stealed_player = self.players[user_info]
                        if not current_player.take_random_card(stealed_player):
                            action_success = False
                        active_status[action_user_id] = True
                    else:
                        action_success = False

                elif user_action == self.GameActions.DISCARD:
                    if type(user_info) == list:
                        current_player = self.players[action_user_id]
                        if(current_player.discard_group(user_info, self.deck)):
                            active_status[action_user_id] = True
                            if self.players[action_user_id].has_empty_hand():
                                self.winner = self.players[action_user_id].name
                        else:
                            action_success = False
                    else:
                        action_success = False
                    
                elif user_action == self.GameActions.SKIP:
                    active_status[action_user_id] = True
                    for player in self.players:
                        player.clear_temp_list()
                    if action_user_id + 1 < len(self.players):
                        next_player = action_user_id + 1
                        self.draw_times = 0
                        self.steal_times = 0
                    else:
                        self.turn_count += 1
                        next_player = self.user_id

                    self.ai_actions_pool = [action for action in self.GameActions \
                    if action != self.GameActions.DEAL]
                        
                self.update_status(user_action, action_success, active_status, next_player)

                # self.callback(copy.deepcopy(self.game_status))
                self.render_queue.put(copy.deepcopy(self.game_status))

            except queue.Empty:
                # update the reender with empty dict
                # self.render_queue.put({}) 
                continue


    def ai_take_action(self, current_ai_id):

        random_action = random.choice(self.ai_actions_pool)
        if random_action != self.GameActions.DISCARD:
            self.ai_actions_pool.remove(random_action)
        print(self.ai_actions_pool)
        print(f"Randomly selected action: {random_action}")

        if random_action == self.GameActions.DRAW:
            draw_card_number = random.randint(1, self.max_draw_times_per_turn)
            self.send_action(random_action, current_ai_id, draw_card_number)
        elif random_action == self.GameActions.STEAL:
            candidate_idx = [idx for idx in range(len(self.players)) if idx != current_ai_id \
                         and len(self.players[idx].hand) > 1]
            if candidate_idx:
                target_idx = random.choice(candidate_idx)
                print(target_idx)
                self.send_action(random_action, current_ai_id, target_idx)
        elif random_action == self.GameActions.DISCARD:
            discarded_cards = self.players[current_ai_id].find_largest_valid_group()
            if discarded_cards:
                self.send_action(random_action, current_ai_id, discarded_cards)
            else:
                if len(self.ai_actions_pool) == 2:
                    self.ai_actions_pool.remove(random_action)
        elif random_action == self.GameActions.SKIP:
            self.send_action(random_action, current_ai_id)





                
            

                    
                


            



        


        



